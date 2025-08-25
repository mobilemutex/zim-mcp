"""
Utility functions for MCP ZIM Server

Author: mobilemutex
"""

import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union
import hashlib
import re


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Set up logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("mcp_zim_server")


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger = logging.getLogger("mcp_zim_server")
        logger.debug("%s took %.3f seconds", func.__name__, end_time - start_time)
        return result
    return wrapper


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks"""
    # Remove any path separators and dangerous characters
    sanitized = re.sub(r'[^\w\-_\.]', '_', filename)
    # Remove leading dots to prevent hidden files
    sanitized = sanitized.lstrip('.')
    return sanitized


def validate_zim_file_path(file_path: Union[str, Path], base_directory: Path) -> Path:
    """Validate that a ZIM file path is within the allowed directory"""
    file_path = Path(file_path)
    
    # If it's just a filename, join with base directory
    if not file_path.is_absolute():
        file_path = base_directory / file_path
    
    # Resolve to absolute path
    resolved_path = file_path.resolve()
    base_resolved = base_directory.resolve()
    
    # Check if the path is within the base directory
    try:
        resolved_path.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(f"File path {resolved_path} is outside allowed directory {base_resolved}") from exc
    
    return resolved_path


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_html_content(html_content: str) -> str:
    """Basic HTML tag removal for text extraction"""
    # Remove HTML tags using regex (basic implementation)
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    # Clean up extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


def generate_cache_key(*args) -> str:
    """Generate a cache key from arguments"""
    key_string = "|".join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()


def safe_get_dict_value(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with default"""
    return dictionary.get(key, default)


class LRUCache:
    """Simple LRU cache implementation"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
        self.access_order: List[str] = []
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in cache"""
        if key in self.cache:
            # Update existing
            self.cache[key] = value
            self.access_order.remove(key)
            self.access_order.append(key)
        else:
            # Add new
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                oldest_key = self.access_order.pop(0)
                del self.cache[oldest_key]
            
            self.cache[key] = value
            self.access_order.append(key)
    
    def clear(self) -> None:
        """Clear cache"""
        self.cache.clear()
        self.access_order.clear()
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self.cache)


def validate_search_query(query: str) -> str:
    """Validate and clean search query"""
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")
    
    # Clean the query
    cleaned_query = query.strip()
    
    # Basic length validation
    if len(cleaned_query) > 1000:
        raise ValueError("Search query too long (max 1000 characters)")
    
    return cleaned_query


def extract_text_preview(content: str, max_length: int = 200) -> str:
    """Extract a preview of text content"""
    # Clean HTML if present
    if '<' in content and '>' in content:
        content = clean_html_content(content)
    
    # Truncate to preview length
    preview = truncate_text(content, max_length)
    
    return preview

