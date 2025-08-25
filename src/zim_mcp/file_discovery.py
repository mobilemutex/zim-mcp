"""
ZIM file discovery and management

Author: mobilemutex
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import os
import time
from .config import ZimServerConfig
from .utils import format_file_size


class FileDiscovery:
    """Discover and manage ZIM files in directories"""
    
    def __init__(self, config: ZimServerConfig):
        self.config = config
        self.logger = logging.getLogger("mcp_zim_server.file_discovery")
        
        # Cache for file discovery results
        self._last_scan_time: Optional[float] = None
        self._scan_cache_duration = 300  # 5 minutes
    
    def discover_files(self, directory: Optional[Path] = None, 
                      force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Discover ZIM files in a directory"""
        try:
            scan_directory = directory or self.config.zim_files_directory
            
            # Check if we need to refresh
            current_time = time.time()
            if (not force_refresh and 
                self._last_scan_time and 
                current_time - self._last_scan_time < self._scan_cache_duration):
                self.logger.debug("Using cached file discovery results")
                return self._get_cached_results(scan_directory)
            
            self.logger.info("Discovering ZIM files in %s", scan_directory)
            
            if not scan_directory.exists():
                self.logger.warning("Directory does not exist: %s", scan_directory)
                return []
            
            files = []
            
            # Scan for .zim files
            for file_path in scan_directory.rglob("*.zim"):
                try:
                    file_info = self._get_file_info(file_path)
                    files.append(file_info)
                except (OSError, ValueError) as e:
                    self.logger.warning("Error processing file %s: %s", file_path, e)
                    continue
            
            # Sort by filename
            files.sort(key=lambda x: x['filename'])
            
            self._last_scan_time = current_time
            self.logger.info("Discovered %d ZIM files", len(files))
            
            return files
            
        except (OSError, ValueError) as e:
            self.logger.error("Error discovering files: %s", e)
            return []
    
    def _get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get basic information about a file"""
        try:
            stat = file_path.stat()
            
            return {
                'filename': file_path.name,
                'filepath': str(file_path),
                'size': stat.st_size,
                'size_formatted': format_file_size(stat.st_size),
                'modified_time': stat.st_mtime,
                'modified_time_formatted': time.strftime(
                    '%Y-%m-%d %H:%M:%S', 
                    time.localtime(stat.st_mtime)
                ),
                'is_readable': os.access(file_path, os.R_OK),
                'relative_path': str(file_path.relative_to(self.config.zim_files_directory))
            }
            
        except (OSError, ValueError) as e:
            self.logger.error("Error getting file info for %s: %s", file_path, e)
            raise
    
    def _get_cached_results(self, directory: Path) -> List[Dict[str, Any]]:
        """Get cached discovery results (placeholder for now)"""
        # In a real implementation, you'd store and retrieve cached results
        # For now, just return empty list to force fresh scan
        return []
    
    def validate_file_access(self, filename: str) -> bool:
        """Validate that a file can be accessed"""
        try:
            file_path = self.config.zim_files_directory / filename
            
            # Check if file exists
            if not file_path.exists():
                return False
            
            # Check if file is readable
            if not os.access(file_path, os.R_OK):
                return False
            
            # Check if it's actually a file (not directory)
            if not file_path.is_file():
                return False
            
            # Check file extension
            if not file_path.suffix.lower() == '.zim':
                return False
            
            return True
            
        except (OSError, ValueError) as e:
            self.logger.error("Error validating file access for %s: %s", filename, e)
            return False
    
    def get_file_stats(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get detailed statistics for a file"""
        try:
            file_path = self.config.zim_files_directory / filename
            
            if not self.validate_file_access(filename):
                return None
            
            stat = file_path.stat()
            
            return {
                'filename': filename,
                'size': stat.st_size,
                'size_formatted': format_file_size(stat.st_size),
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime,
                'accessed_time': stat.st_atime,
                'created_time_formatted': time.strftime(
                    '%Y-%m-%d %H:%M:%S', 
                    time.localtime(stat.st_ctime)
                ),
                'modified_time_formatted': time.strftime(
                    '%Y-%m-%d %H:%M:%S', 
                    time.localtime(stat.st_mtime)
                ),
                'accessed_time_formatted': time.strftime(
                    '%Y-%m-%d %H:%M:%S', 
                    time.localtime(stat.st_atime)
                ),
                'permissions': oct(stat.st_mode)[-3:],
                'is_readable': os.access(file_path, os.R_OK),
                'is_writable': os.access(file_path, os.W_OK)
            }
            
        except (OSError, ValueError) as e:
            self.logger.error("Error getting file stats for %s: %s", filename, e)
            return None
    
    def find_files_by_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """Find files matching a pattern"""
        try:
            files = self.discover_files()
            
            # Simple pattern matching (case-insensitive)
            pattern_lower = pattern.lower()
            matching_files = []
            
            for file_info in files:
                filename_lower = file_info['filename'].lower()
                if pattern_lower in filename_lower:
                    matching_files.append(file_info)
            
            return matching_files
            
        except (OSError, ValueError) as e:
            self.logger.error("Error finding files by pattern '%s': %s", pattern, e)
            return []
    
    def get_directory_stats(self) -> Dict[str, Any]:
        """Get statistics about the ZIM files directory"""
        try:
            directory = self.config.zim_files_directory
            
            if not directory.exists():
                return {
                    'directory_exists': False,
                    'error': f"Directory does not exist: {directory}"
                }
            
            files = self.discover_files()
            
            total_size = sum(f['size'] for f in files)
            
            return {
                'directory_exists': True,
                'directory_path': str(directory),
                'total_files': len(files),
                'total_size': total_size,
                'total_size_formatted': format_file_size(total_size),
                'last_scan_time': self._last_scan_time,
                'last_scan_time_formatted': (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._last_scan_time))
                    if self._last_scan_time else None
                )
            }
            
        except (OSError, ValueError) as e:
            self.logger.error("Error getting directory stats: %s", e)
            return {
                'directory_exists': False,
                'error': str(e)
            }

