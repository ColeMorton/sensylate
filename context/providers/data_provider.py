"""
Data Context Provider for File Operations and Data Management

This provider handles all data-related operations including file I/O, caching,
backup management, and output organization. It abstracts file system concerns
from commands, enabling commands to work with logical data operations rather
than physical file paths.
"""

import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

from ..base_context import DataContext


logger = logging.getLogger(__name__)


@dataclass
class FileMetadata:
    """Metadata about managed files"""
    path: Path
    size: int
    created: datetime
    modified: datetime
    checksum: Optional[str] = None


class DataOperationError(Exception):
    """Raised when data operations fail"""
    pass


class DataContextProvider:
    """
    Data management provider for Sensylate commands.

    This provider centralizes all file operations and data management,
    providing a clean abstraction for commands to work with data without
    coupling to specific file paths or storage mechanisms.

    Features:
    - Logical path management (category-based organization)
    - Automatic backup and versioning
    - Caching for expensive operations
    - File integrity and validation
    - Cleanup and maintenance

    Usage:
        provider = DataContextProvider(data_context)
        output_path = provider.get_output_path("fundamental_analysis", "discovery")
        provider.save_json_output(data, output_path, "AAPL_20250706_discovery.json")
    """

    def __init__(self, data_context: DataContext):
        self.context = data_context
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        """Ensure required directory structure exists"""
        directories = [
            self.context.base_output_path,
            self.context.base_output_path / ".cache",
            self.context.base_output_path / ".backups",
            self.context.base_output_path / ".temp"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_output_path(self, category: str, subcategory: str = None) -> Path:
        """
        Get organized output path for category and subcategory.

        Args:
            category: Main category (e.g., "fundamental_analysis")
            subcategory: Subcategory (e.g., "discovery", "validation")

        Returns:
            Path object for the category/subcategory
        """
        if subcategory:
            path = self.context.base_output_path / category / subcategory
        else:
            path = self.context.base_output_path / category

        path.mkdir(parents=True, exist_ok=True)
        return path

    def generate_filename(
        self,
        base_name: str,
        extension: str = "json",
        timestamp: datetime = None,
        suffix: str = None
    ) -> str:
        """
        Generate standardized filename with timestamp.

        Args:
            base_name: Base name (e.g., ticker symbol)
            extension: File extension without dot
            timestamp: Optional timestamp (defaults to now)
            suffix: Optional suffix (e.g., "discovery", "validation")

        Returns:
            Standardized filename
        """
        if timestamp is None:
            timestamp = datetime.now()

        date_str = timestamp.strftime("%Y%m%d")

        if suffix:
            filename = f"{base_name}_{date_str}_{suffix}.{extension}"
        else:
            filename = f"{base_name}_{date_str}.{extension}"

        return filename

    def save_json_output(
        self,
        data: Dict[str, Any],
        output_path: Path,
        filename: str,
        create_backup: bool = None
    ) -> Path:
        """
        Save JSON data to output path with optional backup.

        Args:
            data: Data to save as JSON
            output_path: Directory to save in
            filename: Filename to use
            create_backup: Create backup if file exists (defaults to context setting)

        Returns:
            Path to saved file
        """
        file_path = output_path / filename

        # Create backup if file exists and backup is enabled
        if create_backup is None:
            create_backup = self.context.backup_enabled

        if create_backup and file_path.exists():
            backup_path = self._create_backup(file_path)
            logger.info(f"Created backup: {backup_path}")

        # Save data
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            # Set file permissions
            file_path.chmod(self.context.file_permissions)

            logger.info(f"Saved JSON output: {file_path}")
            return file_path

        except (IOError, json.JSONEncodeError) as e:
            raise DataOperationError(f"Failed to save JSON to {file_path}: {e}")

    def load_json_input(self, file_path: Path) -> Dict[str, Any]:
        """
        Load JSON data from file.

        Args:
            file_path: Path to JSON file

        Returns:
            Loaded JSON data

        Raises:
            DataOperationError: If file cannot be loaded
        """
        try:
            with open(file_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            raise DataOperationError(f"Failed to load JSON from {file_path}: {e}")

    def save_markdown_output(
        self,
        content: str,
        output_path: Path,
        filename: str,
        create_backup: bool = None
    ) -> Path:
        """
        Save markdown content to output path.

        Args:
            content: Markdown content to save
            output_path: Directory to save in
            filename: Filename to use
            create_backup: Create backup if file exists

        Returns:
            Path to saved file
        """
        file_path = output_path / filename

        # Create backup if needed
        if create_backup is None:
            create_backup = self.context.backup_enabled

        if create_backup and file_path.exists():
            backup_path = self._create_backup(file_path)
            logger.info(f"Created backup: {backup_path}")

        # Save content
        try:
            with open(file_path, 'w') as f:
                f.write(content)

            file_path.chmod(self.context.file_permissions)

            logger.info(f"Saved markdown output: {file_path}")
            return file_path

        except IOError as e:
            raise DataOperationError(f"Failed to save markdown to {file_path}: {e}")

    def _create_backup(self, original_path: Path) -> Path:
        """Create backup of existing file"""
        backup_path = self.context.get_backup_path(original_path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(original_path, backup_path)
            return backup_path
        except IOError as e:
            logger.warning(f"Failed to create backup of {original_path}: {e}")
            raise DataOperationError(f"Backup creation failed: {e}")

    def cache_data(self, key: str, data: Any, ttl_seconds: int = 3600) -> Path:
        """
        Cache data with TTL.

        Args:
            key: Cache key
            data: Data to cache
            ttl_seconds: Time to live in seconds

        Returns:
            Path to cached file
        """
        if not self.context.cache_enabled:
            raise DataOperationError("Caching is disabled")

        cache_path = self.context.get_cache_path(key)
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        cache_data = {
            "data": data,
            "cached_at": datetime.now().isoformat(),
            "ttl_seconds": ttl_seconds,
            "expires_at": (datetime.now().timestamp() + ttl_seconds)
        }

        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)

            logger.debug(f"Cached data with key: {key}")
            return cache_path

        except (IOError, json.JSONEncodeError) as e:
            raise DataOperationError(f"Failed to cache data: {e}")

    def get_cached_data(self, key: str) -> Optional[Any]:
        """
        Get cached data if still valid.

        Args:
            key: Cache key

        Returns:
            Cached data if valid, None otherwise
        """
        if not self.context.cache_enabled:
            return None

        cache_path = self.context.get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path) as f:
                cache_data = json.load(f)

            # Check if expired
            expires_at = cache_data.get("expires_at", 0)
            if datetime.now().timestamp() > expires_at:
                logger.debug(f"Cache expired for key: {key}")
                cache_path.unlink(missing_ok=True)
                return None

            logger.debug(f"Cache hit for key: {key}")
            return cache_data["data"]

        except (json.JSONDecodeError, IOError, KeyError):
            logger.warning(f"Invalid cache file for key: {key}")
            cache_path.unlink(missing_ok=True)
            return None

    def clear_cache(self, pattern: str = None):
        """
        Clear cache files.

        Args:
            pattern: Optional pattern to match (glob style)
        """
        cache_dir = self.context.base_output_path / ".cache"

        if pattern:
            files_to_remove = cache_dir.glob(pattern)
        else:
            files_to_remove = cache_dir.glob("*.json")

        removed_count = 0
        for cache_file in files_to_remove:
            try:
                cache_file.unlink()
                removed_count += 1
            except IOError:
                logger.warning(f"Failed to remove cache file: {cache_file}")

        logger.info(f"Cleared {removed_count} cache files")

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        if not self.context.temp_cleanup:
            return

        temp_dir = self.context.base_output_path / ".temp"
        if not temp_dir.exists():
            return

        removed_count = 0
        for temp_file in temp_dir.glob("*"):
            try:
                if temp_file.is_file():
                    temp_file.unlink()
                    removed_count += 1
                elif temp_file.is_dir():
                    shutil.rmtree(temp_file)
                    removed_count += 1
            except (IOError, OSError):
                logger.warning(f"Failed to remove temp file: {temp_file}")

        logger.info(f"Cleaned up {removed_count} temporary files")

    def get_file_metadata(self, file_path: Path) -> FileMetadata:
        """Get metadata for file"""
        if not file_path.exists():
            raise DataOperationError(f"File does not exist: {file_path}")

        stat = file_path.stat()

        return FileMetadata(
            path=file_path,
            size=stat.st_size,
            created=datetime.fromtimestamp(stat.st_ctime),
            modified=datetime.fromtimestamp(stat.st_mtime)
        )

    def list_category_files(self, category: str, subcategory: str = None) -> List[FileMetadata]:
        """
        List files in category with metadata.

        Args:
            category: Category name
            subcategory: Optional subcategory

        Returns:
            List of FileMetadata objects
        """
        category_path = self.get_output_path(category, subcategory)

        files = []
        for file_path in category_path.glob("*"):
            if file_path.is_file():
                try:
                    metadata = self.get_file_metadata(file_path)
                    files.append(metadata)
                except DataOperationError:
                    continue

        # Sort by modification time (newest first)
        return sorted(files, key=lambda f: f.modified, reverse=True)

    def get_storage_summary(self) -> Dict[str, Any]:
        """Get storage usage summary"""
        base_path = self.context.base_output_path

        def get_dir_size(path: Path) -> int:
            """Get total size of directory"""
            total = 0
            try:
                for item in path.rglob("*"):
                    if item.is_file():
                        total += item.stat().st_size
            except (OSError, IOError):
                pass
            return total

        return {
            "base_path": str(base_path),
            "total_size_bytes": get_dir_size(base_path),
            "cache_size_bytes": get_dir_size(base_path / ".cache"),
            "backup_size_bytes": get_dir_size(base_path / ".backups"),
            "temp_size_bytes": get_dir_size(base_path / ".temp"),
            "categories": {
                cat.name: get_dir_size(cat)
                for cat in base_path.iterdir()
                if cat.is_dir() and not cat.name.startswith(".")
            },
            "last_updated": datetime.now().isoformat()
        }
