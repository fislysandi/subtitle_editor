"""
Pure Python download manager - no Blender dependencies.
Follows functional programming principles with immutable state.
"""

import os
import threading
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum

try:
    from huggingface_hub import snapshot_download
    from huggingface_hub.errors import RepositoryNotFoundError

    HAS_HF = True
except ImportError:
    HAS_HF = False
    snapshot_download = None
    RepositoryNotFoundError = Exception


class DownloadStatus(Enum):
    """Immutable state representation for download status."""

    PENDING = "pending"
    CHECKING = "checking"
    DOWNLOADING = "downloading"
    COMPLETE = "complete"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class DownloadProgress:
    """
    Immutable progress state.
    Frozen dataclass ensures immutability (functional approach).
    """

    status: DownloadStatus
    bytes_downloaded: int
    bytes_total: int
    current_file: str
    message: str

    @property
    def percentage(self) -> float:
        """Pure function - same input always same output."""
        if self.bytes_total == 0:
            return 0.0
        return self.bytes_downloaded / self.bytes_total


class DownloadManager:
    """
    Manages model downloads with functional approach.
    No side effects - all state changes explicit.
    """

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self._cancel_event = threading.Event()
        self._current_progress = DownloadProgress(
            status=DownloadStatus.PENDING,
            bytes_downloaded=0,
            bytes_total=0,
            current_file="",
            message="Ready",
        )
        self._lock = threading.Lock()

    def get_progress(self) -> DownloadProgress:
        """Pure read - returns immutable state."""
        with self._lock:
            return self._current_progress

    def is_cancelled(self) -> bool:
        """Pure function check."""
        return self._cancel_event.is_set()

    def cancel(self) -> None:
        """Signal cancellation - thread-safe."""
        self._cancel_event.set()
        self._update_progress(
            status=DownloadStatus.CANCELLED, message="Download cancelled"
        )

    def _update_progress(self, **kwargs) -> None:
        """
        Internal: Update progress state immutably.
        Creates new DownloadProgress instead of modifying.
        """
        with self._lock:
            current = self._current_progress
            new_state = DownloadProgress(
                status=kwargs.get("status", current.status),
                bytes_downloaded=kwargs.get(
                    "bytes_downloaded", current.bytes_downloaded
                ),
                bytes_total=kwargs.get("bytes_total", current.bytes_total),
                current_file=kwargs.get("current_file", current.current_file),
                message=kwargs.get("message", current.message),
            )
            self._current_progress = new_state

    def _get_repo_id(self, model_name: str) -> str:
        """Pure function - model name to repo ID mapping."""
        repo_map: Dict[str, str] = {
            "tiny": "Systran/faster-whisper-tiny",
            "tiny.en": "Systran/faster-whisper-tiny.en",
            "base": "Systran/faster-whisper-base",
            "base.en": "Systran/faster-whisper-base.en",
            "small": "Systran/faster-whisper-small",
            "small.en": "Systran/faster-whisper-small.en",
            "medium": "Systran/faster-whisper-medium",
            "medium.en": "Systran/faster-whisper-medium.en",
            "large-v1": "Systran/faster-whisper-large-v1",
            "large-v2": "Systran/faster-whisper-large-v2",
            "large-v3": "Systran/faster-whisper-large-v3",
            "large": "Systran/faster-whisper-large-v3",
            "distil-small.en": "Systran/faster-distil-whisper-small.en",
            "distil-medium.en": "Systran/faster-distil-whisper-medium.en",
            "distil-large-v2": "Systran/faster-distil-whisper-large-v2",
            "distil-large-v3": "Systran/faster-distil-whisper-large-v3",
            "distil-large-v3.5": "distil-whisper/distil-large-v3.5-ct2",
            "large-v3-turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
            "turbo": "mobiuslabsgmbh/faster-whisper-large-v3-turbo",
        }
        return repo_map.get(model_name, f"Systran/faster-whisper-{model_name}")

    def _is_cached(self, model_name: str) -> bool:
        """Pure function - check if model exists in cache."""
        repo_id = self._get_repo_id(model_name)
        cache_path = self.cache_dir / f"models--{repo_id.replace('/', '--')}"
        return cache_path.exists()

    def _get_error_result(self, message: str) -> DownloadProgress:
        """Pure function - creates error progress state."""
        return DownloadProgress(
            status=DownloadStatus.ERROR,
            bytes_downloaded=0,
            bytes_total=0,
            current_file="",
            message=message,
        )

    def _get_cached_result(self, model_name: str) -> DownloadProgress:
        """Pure function - creates cached progress state."""
        return DownloadProgress(
            status=DownloadStatus.COMPLETE,
            bytes_downloaded=0,
            bytes_total=0,
            current_file="",
            message=f"Model {model_name} already cached",
        )

    def _get_success_result(self, model_name: str) -> DownloadProgress:
        """Pure function - creates success progress state."""
        return DownloadProgress(
            status=DownloadStatus.COMPLETE,
            bytes_downloaded=100,
            bytes_total=100,
            current_file="",
            message=f"Model {model_name} downloaded successfully!",
        )

    def _perform_download(self, repo_id: str, token: Optional[str]) -> None:
        """Execute the actual download using huggingface_hub."""
        snapshot_download(
            repo_id=repo_id,
            cache_dir=self.cache_dir,
            token=token,
            local_files_only=False,
            resume_download=True,
            tqdm_class=None,
        )

    def _handle_download_error(self, error: Exception) -> DownloadProgress:
        """Handle download errors and cancellation."""
        if self._cancel_event.is_set():
            return self._current_progress
        return self._get_error_result(f"Error: {str(error)}")

    def download(
        self, model_name: str, token: Optional[str] = None
    ) -> DownloadProgress:
        """
        Download a model. Blocks until complete or cancelled.
        Returns final progress state.
        """
        if not HAS_HF:
            return self._get_error_result("huggingface_hub not installed")

        if self._is_cached(model_name):
            return self._get_cached_result(model_name)

        self._update_progress(
            status=DownloadStatus.CHECKING,
            message=f"Preparing to download {model_name}...",
        )

        repo_id = self._get_repo_id(model_name)

        try:
            self._perform_download(repo_id, token)

            if self._cancel_event.is_set():
                return self._current_progress

            return self._get_success_result(model_name)

        except Exception as e:
            return self._handle_download_error(e)


def create_download_manager(cache_dir: str) -> DownloadManager:
    """
    Factory function - creates DownloadManager with dependency injection.
    Pure function - same input always same output.
    """
    return DownloadManager(cache_dir)
