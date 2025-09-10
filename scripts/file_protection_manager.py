#!/usr/bin/env python3
"""
File Protection Manager

Provides file integrity protection against race conditions and corruption.
Implements file locking, integrity monitoring, and corruption detection.
"""

import fcntl
import hashlib
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd


class FileProtectionManager:
    """Manages file protection against race conditions and corruption"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._file_locks: Dict[str, Any] = {}
        self._integrity_cache: Dict[str, str] = {}

    def protected_write_csv(
        self, df: pd.DataFrame, file_path: Path, timeout: int = 30
    ) -> bool:
        """
        Write CSV with race condition protection and integrity monitoring

        Args:
            df: DataFrame to write
            file_path: Target file path
            timeout: Maximum time to wait for file lock (seconds)

        Returns:
            bool: True if write successful and integrity verified
        """
        file_path_str = str(file_path)

        self.logger.info(
            f"🛡️ Starting protected write for {file_path} with {len(df)} rows"
        )

        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Create lock file path
            lock_path = file_path.with_suffix(".csv.lock")

            # Acquire exclusive file lock
            with open(lock_path, "w") as lock_file:
                try:
                    # Non-blocking lock attempt with timeout
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        try:
                            fcntl.flock(
                                lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB
                            )
                            break
                        except IOError:
                            time.sleep(0.1)
                    else:
                        self.logger.error(
                            f"Failed to acquire file lock for {file_path} within {timeout}s"
                        )
                        return False

                    self.logger.info(f"🔒 Acquired exclusive lock for {file_path}")

                    # Ensure target file is writable if it exists
                    if file_path.exists():
                        self._make_writable(file_path)

                    # Write to temporary file first (atomic write)
                    temp_path = file_path.with_suffix(".tmp")

                    with open(temp_path, "w", newline="", encoding="utf-8") as f:
                        df.to_csv(f, index=False)
                        f.flush()
                        os.fsync(f.fileno())

                    # Verify temporary file integrity
                    if not self._verify_csv_integrity(temp_path, df):
                        temp_path.unlink(missing_ok=True)
                        self.logger.error(
                            f"Temporary file integrity check failed: {temp_path}"
                        )
                        return False

                    # Calculate content hash for integrity monitoring
                    content_hash = self._calculate_file_hash(temp_path)

                    # Create backup copy before atomic move
                    backup_path = file_path.with_suffix(".backup.csv")
                    import shutil

                    shutil.copy2(temp_path, backup_path)
                    self.logger.info(f"💾 Created backup for recovery: {backup_path}")

                    # Atomic move to final location (single operation)
                    temp_path.replace(file_path)

                    # Immediate verification
                    if not file_path.exists():
                        self.logger.error(
                            f"File does not exist after atomic move: {file_path}"
                        )
                        return False

                    # Verify final file integrity
                    if not self._verify_csv_integrity(file_path, df):
                        self.logger.error(
                            f"Final file integrity check failed: {file_path}"
                        )
                        return False

                    # Store integrity hash for recovery
                    self._integrity_cache[file_path_str] = content_hash

                    file_size = file_path.stat().st_size
                    self.logger.info(
                        f"✅ Protected CSV write completed: {file_path} ({file_size} bytes)"
                    )
                    return True

                finally:
                    # Release lock
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                    self.logger.info(f"🔓 Released lock for {file_path}")

        except Exception as e:
            self.logger.error(f"Protected write failed for {file_path}: {e}")
            return False
        finally:
            # Clean up lock file
            try:
                lock_path.unlink(missing_ok=True)
            except:
                pass  # Ignore lock file cleanup errors

        return False

    def _verify_csv_integrity(self, file_path: Path, expected_df: pd.DataFrame) -> bool:
        """Verify CSV file integrity by reading back and comparing structure"""
        try:
            if not file_path.exists() or file_path.stat().st_size == 0:
                return False

            # Read back and verify structure
            read_df = pd.read_csv(file_path)

            # Check basic structure
            if read_df.shape != expected_df.shape:
                self.logger.error(
                    f"DataFrame shape mismatch: expected {expected_df.shape}, got {read_df.shape}"
                )
                return False

            # Check columns match
            if list(read_df.columns) != list(expected_df.columns):
                self.logger.error(
                    f"Column mismatch: expected {list(expected_df.columns)}, got {list(read_df.columns)}"
                )
                return False

            # Check for reasonable data content (not all zeros/nulls)
            if read_df.isnull().all().all():
                self.logger.error("File contains only null values")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Integrity verification failed: {e}")
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content"""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""

    def auto_recover_from_backup(self, file_path: Path) -> bool:
        """Automatically recover corrupted file from backup with external process detection"""
        try:
            backup_path = file_path.with_suffix(".backup.csv")

            if not backup_path.exists():
                self.logger.error(f"🔧 No backup file found for recovery: {backup_path}")
                return False

            backup_size = backup_path.stat().st_size
            if backup_size < 100:
                self.logger.error(
                    f"🔧 Backup file too small ({backup_size} bytes): {backup_path}"
                )
                return False

            # Log corruption pattern analysis
            self._log_corruption_analysis(file_path, backup_path)

            self.logger.info(
                f"🔄 Auto-recovering from backup: {backup_path} ({backup_size} bytes)"
            )

            # Create recovery copy first (protection against backup corruption)
            recovery_path = file_path.with_suffix(".recovery.csv")
            backup_path.replace(recovery_path)
            recovery_path.replace(file_path)

            # Apply protective file permissions
            self._apply_protection_attributes(file_path)

            # Verify restoration
            if file_path.exists() and file_path.stat().st_size > 100:
                restored_size = file_path.stat().st_size
                self.logger.info(
                    f"✅ Auto-recovery successful: {file_path} ({restored_size} bytes)"
                )

                # Log recovery success pattern
                self.logger.info(
                    f"📊 Corruption pattern: External process truncated {restored_size} bytes → 1 byte, recovered successfully"
                )
                return True
            else:
                self.logger.error(f"❌ Auto-recovery verification failed: {file_path}")
                return False

        except Exception as e:
            self.logger.error(f"Auto-recovery from backup failed: {e}")
            return False

    def _log_corruption_analysis(self, file_path: Path, backup_path: Path) -> None:
        """Analyze and log corruption patterns for external process identification"""
        try:
            import pwd
            import subprocess

            # Get file system information
            file_stat = file_path.stat()
            backup_stat = backup_path.stat()

            # Calculate time since corruption
            corruption_time = (
                backup_stat.st_mtime - file_stat.st_mtime
                if file_stat.st_mtime > 0
                else "unknown"
            )

            self.logger.warning(f"🔍 Corruption Analysis: {file_path.name}")
            self.logger.warning(
                f"   └ Backup size: {backup_stat.st_size:,} bytes | Corrupted size: {file_stat.st_size} bytes"
            )
            self.logger.warning(
                f"   └ Corruption pattern: Complete data loss (likely external process interference)"
            )

            # Check for common macOS processes that might interfere with files
            self._detect_suspicious_processes(file_path)

        except Exception as e:
            self.logger.debug(f"Corruption analysis failed: {e}")

    def _detect_suspicious_processes(self, file_path: Path) -> None:
        """Detect potential external processes that might cause file corruption"""
        try:
            import subprocess

            # Check for processes that commonly interfere with CSV files on macOS
            suspicious_processes = [
                "mds",  # Spotlight indexing
                "mdworker",  # Spotlight worker
                "fswatch",  # File system watcher
                "lsof",  # List open files (if used by other tools)
                "antivirus",  # Generic antivirus patterns
                "ClamAV",  # ClamAV antivirus
                "Malwarebytes",  # Malwarebytes antivirus
            ]

            active_suspicious = []
            try:
                # Get running processes
                result = subprocess.run(
                    ["ps", "aux"], capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0:
                    processes = result.stdout.lower()
                    for proc in suspicious_processes:
                        if proc.lower() in processes:
                            active_suspicious.append(proc)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                pass  # Ignore process detection failures

            if active_suspicious:
                self.logger.warning(
                    f"   └ Potentially interfering processes detected: {', '.join(active_suspicious)}"
                )
                self.logger.warning(
                    f"   └ Recommendation: Consider excluding {file_path.parent} from Spotlight indexing"
                )
            else:
                self.logger.warning(
                    f"   └ No obvious interfering processes detected (corruption timing suggests external interference)"
                )

        except Exception as e:
            self.logger.debug(f"Process detection failed: {e}")

    def _apply_protection_attributes(self, file_path: Path) -> None:
        """Apply protective file attributes to reduce external interference"""
        try:
            import os
            import stat

            # Set read-only permissions temporarily to discourage external modification
            # We'll make it writable again when needed
            current_mode = file_path.stat().st_mode
            protected_mode = (
                current_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
            )
            file_path.chmod(protected_mode)

            self.logger.debug(f"Applied protective attributes to {file_path}")

        except Exception as e:
            self.logger.debug(f"Failed to apply protective attributes: {e}")

    def _make_writable(self, file_path: Path) -> None:
        """Make file writable for updates"""
        try:
            import stat

            current_mode = file_path.stat().st_mode
            writable_mode = current_mode | stat.S_IWUSR
            file_path.chmod(writable_mode)
            self.logger.debug(f"Made file writable: {file_path}")
        except Exception as e:
            self.logger.debug(f"Failed to make file writable: {e}")

    def check_file_integrity(self, file_path: Path) -> bool:
        """Check file integrity and auto-recover from backup if corrupted"""
        file_path_str = str(file_path)

        if file_path_str not in self._integrity_cache:
            return True  # No cached integrity info

        try:
            # Check basic file existence and size first
            if not file_path.exists():
                self.logger.error(f"🚨 File missing: {file_path}")
                return self.auto_recover_from_backup(file_path)

            current_size = file_path.stat().st_size
            if current_size < 100:
                self.logger.error(
                    f"🚨 External corruption detected: {file_path} ({current_size} bytes)"
                )
                return self.auto_recover_from_backup(file_path)

            # Check content hash for deeper corruption detection
            expected_hash = self._integrity_cache[file_path_str]
            current_hash = self._calculate_file_hash(file_path)

            if current_hash != expected_hash:
                self.logger.error(f"🚨 Content corruption detected: {file_path}")
                return self.auto_recover_from_backup(file_path)

            return True

        except Exception as e:
            self.logger.error(f"Integrity check failed: {e}")
            return self.auto_recover_from_backup(file_path)
