#!/usr/bin/env python3
"""
File Operation Manager

Centralized file I/O management with atomic operations, file locking, and corruption prevention.
Resolves race conditions and file corruption issues in the data pipeline.

Features:
- File-level locking to prevent concurrent writes
- Atomic operations using temporary files + atomic move
- Write verification with content validation
- Rollback capability for failed operations
- Comprehensive logging for debugging
"""

import fcntl
import logging
import os
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from errors import ProcessingError
from result_types import ProcessingResult


class FileOperationManager:
    """
    Centralized file operation manager with atomic writes and corruption prevention.
    
    Provides thread-safe, atomic file operations to prevent the race conditions
    and file corruption issues that occur when multiple processes write to the same files.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize file operation manager with optional logger"""
        self.logger = logger or logging.getLogger(__name__)
        self._active_locks: Dict[str, Any] = {}

    @contextmanager
    def acquire_file_lock(self, file_path: Union[str, Path], timeout: float = 30.0):
        """
        Acquire an exclusive lock on a file to prevent concurrent writes.
        
        Args:
            file_path: Path to file to lock
            timeout: Maximum time to wait for lock acquisition
            
        Raises:
            ProcessingError: If lock cannot be acquired within timeout
        """
        file_path = Path(file_path)
        lock_path = file_path.with_suffix(file_path.suffix + '.lock')
        
        try:
            # Ensure parent directory exists
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open lock file and acquire exclusive lock
            lock_file = open(lock_path, 'w')
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self._active_locks[str(file_path)] = lock_file
                    self.logger.debug(f"🔒 Acquired file lock for {file_path}")
                    break
                except OSError:
                    time.sleep(0.1)  # Wait 100ms before retry
            else:
                lock_file.close()
                raise ProcessingError(f"Failed to acquire file lock for {file_path} within {timeout}s")
            
            try:
                yield
            finally:
                # Release lock and cleanup
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                self._active_locks.pop(str(file_path), None)
                
                # Remove lock file
                try:
                    lock_path.unlink()
                except FileNotFoundError:
                    pass
                
                self.logger.debug(f"🔓 Released file lock for {file_path}")
                
        except Exception as e:
            # Cleanup on error
            if str(file_path) in self._active_locks:
                try:
                    self._active_locks[str(file_path)].close()
                except:
                    pass
                self._active_locks.pop(str(file_path), None)
            raise ProcessingError(f"File locking error for {file_path}: {e}")

    def atomic_csv_write(
        self, 
        file_path: Union[str, Path], 
        dataframe: pd.DataFrame,
        backup_original: bool = True,
        verify_content: bool = True
    ) -> ProcessingResult:
        """
        Atomically write a DataFrame to CSV with verification and rollback capability.
        
        Args:
            file_path: Target file path
            dataframe: DataFrame to write
            backup_original: Whether to backup existing file before overwrite
            verify_content: Whether to verify written content
            
        Returns:
            ProcessingResult with success status and details
        """
        file_path = Path(file_path)
        temp_path = file_path.with_suffix('.tmp')
        backup_path = file_path.with_suffix('.backup') if backup_original else None
        
        try:
            with self.acquire_file_lock(file_path):
                self.logger.info(f"🔧 Starting atomic CSV write for {file_path}")
                
                # Backup existing file if requested
                if backup_original and file_path.exists():
                    shutil.copy2(file_path, backup_path)
                    self.logger.debug(f"📁 Backed up original file to {backup_path}")
                
                # Ensure parent directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write to temporary file with explicit flushing
                with open(temp_path, 'w', newline='', encoding='utf-8') as f:
                    dataframe.to_csv(f, index=False)
                    f.flush()
                    os.fsync(f.fileno())
                
                self.logger.debug(f"✏️ Written {len(dataframe)} rows to temporary file")
                
                # Verify written content if requested
                if verify_content:
                    verification_result = self._verify_csv_content(temp_path, dataframe)
                    if not verification_result.success:
                        raise ProcessingError(f"Content verification failed: {verification_result.error}")
                
                # Atomic move: this is the critical operation
                shutil.move(str(temp_path), str(file_path))
                self.logger.debug(f"🔄 Atomically moved temporary file to final location")
                
                # Multiple verification points with delays to catch corruption timing
                import time
                
                # Immediate verification
                if file_path.exists():
                    immediate_size = file_path.stat().st_size
                    self.logger.info(f"📍 Immediate post-move verification: {file_path} ({immediate_size} bytes)")
                    
                    # Brief delay and re-check
                    time.sleep(0.1)
                    if file_path.exists():
                        after_delay_size = file_path.stat().st_size
                        self.logger.info(f"📍 After 100ms delay verification: {file_path} ({after_delay_size} bytes)")
                        
                        if immediate_size != after_delay_size:
                            self.logger.error(f"🚨 FILE CORRUPTION DETECTED: Size changed from {immediate_size} to {after_delay_size} bytes in 100ms!")
                        
                        # Second delay and final check
                        time.sleep(0.2)
                        if file_path.exists():
                            final_size = file_path.stat().st_size
                            self.logger.info(f"📍 Final verification: {file_path} ({final_size} bytes)")
                            
                            if after_delay_size != final_size:
                                self.logger.error(f"🚨 CONTINUED FILE CORRUPTION: Size changed from {after_delay_size} to {final_size} bytes in additional 200ms!")
                            
                            self.logger.info(f"✅ Atomic CSV write completed: {file_path} ({final_size} bytes)")
                            
                            # Cleanup backup on success
                            if backup_path and backup_path.exists():
                                backup_path.unlink()
                                self.logger.debug(f"🗑️ Cleaned up backup file")
                            
                            return ProcessingResult(
                                success=True,
                                operation=f"atomic_csv_write_{file_path.name}",
                                content=f"Successfully wrote {len(dataframe)} rows",
                                metadata={"file_size": final_size, "row_count": len(dataframe)}
                            )
                        else:
                            raise ProcessingError("File disappeared during final verification")
                    else:
                        raise ProcessingError("File disappeared during delay verification")
                else:
                    raise ProcessingError("File does not exist after atomic move")
                    
        except Exception as e:
            self.logger.error(f"❌ Atomic CSV write failed for {file_path}: {e}")
            
            # Cleanup temporary file
            if temp_path.exists():
                try:
                    temp_path.unlink()
                    self.logger.debug("🗑️ Cleaned up temporary file")
                except:
                    pass
            
            # Rollback from backup if available
            if backup_path and backup_path.exists():
                try:
                    shutil.move(str(backup_path), str(file_path))
                    self.logger.info(f"🔄 Rolled back from backup file")
                except Exception as rollback_error:
                    self.logger.error(f"❌ Rollback failed: {rollback_error}")
            
            return ProcessingResult(
                success=False,
                operation=f"atomic_csv_write_{file_path.name}",
                error=str(e)
            )

    def _verify_csv_content(self, file_path: Path, expected_dataframe: pd.DataFrame) -> ProcessingResult:
        """
        Verify that written CSV content matches expected DataFrame.
        
        Args:
            file_path: Path to CSV file to verify
            expected_dataframe: Expected DataFrame content
            
        Returns:
            ProcessingResult with verification status
        """
        try:
            # Check file exists and has reasonable size
            if not file_path.exists():
                return ProcessingResult(
                    success=False,
                    operation="verify_csv_content",
                    error="File does not exist"
                )
            
            file_size = file_path.stat().st_size
            if file_size < 50:  # Very small files are suspicious
                return ProcessingResult(
                    success=False,
                    operation="verify_csv_content",
                    error=f"File too small ({file_size} bytes)"
                )
            
            # Read back and verify basic structure
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                second_line = f.readline().strip()
            
            # Verify header
            expected_header = ','.join(expected_dataframe.columns)
            if first_line != expected_header:
                return ProcessingResult(
                    success=False,
                    operation="verify_csv_content",
                    error=f"Header mismatch. Expected: {expected_header}, Got: {first_line}"
                )
            
            # Verify we have data rows
            if not second_line or len(second_line.split(',')) != len(expected_dataframe.columns):
                return ProcessingResult(
                    success=False,
                    operation="verify_csv_content",
                    error="No valid data rows or column count mismatch"
                )
            
            self.logger.debug(f"✅ Content verification passed for {file_path}")
            return ProcessingResult(
                success=True,
                operation="verify_csv_content",
                content="Content verification passed"
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                operation="verify_csv_content",
                error=f"Verification error: {e}"
            )

    def safe_file_copy(self, source: Union[str, Path], destination: Union[str, Path]) -> ProcessingResult:
        """
        Safely copy a file with atomic operation and verification.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            ProcessingResult with copy status
        """
        source = Path(source)
        destination = Path(destination)
        
        try:
            with self.acquire_file_lock(destination):
                if not source.exists():
                    return ProcessingResult(
                        success=False,
                        operation="safe_file_copy",
                        error=f"Source file does not exist: {source}"
                    )
                
                # Ensure destination directory exists
                destination.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy with verification
                shutil.copy2(str(source), str(destination))
                
                # Verify copy
                if destination.exists() and destination.stat().st_size > 0:
                    self.logger.info(f"✅ Successfully copied {source} to {destination}")
                    return ProcessingResult(
                        success=True,
                        operation="safe_file_copy",
                        content=f"Copied {source.name}",
                        metadata={"file_size": destination.stat().st_size}
                    )
                else:
                    return ProcessingResult(
                        success=False,
                        operation="safe_file_copy",
                        error="Copy verification failed"
                    )
                    
        except Exception as e:
            return ProcessingResult(
                success=False,
                operation="safe_file_copy",
                error=f"Copy failed: {e}"
            )

    def cleanup_locks(self):
        """Clean up any remaining file locks (call on shutdown)"""
        for file_path, lock_file in list(self._active_locks.items()):
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                self.logger.debug(f"🧹 Cleaned up lock for {file_path}")
            except:
                pass
        self._active_locks.clear()