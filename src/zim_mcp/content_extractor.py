"""
Content extraction and formatting for ZIM entries

Author: mobilemutex
"""

import logging
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import libzim.reader # pyright: ignore[reportMissingModuleSource]
from .config import ZimServerConfig
from .zim_manager import ZimManager
from .utils import clean_html_content, truncate_text, extract_text_preview


@dataclass
class ExtractedContentInfo:
    """Extracted content from a ZIM entry"""
    path: str
    title: str
    content: str
    content_type: str
    content_length: int
    preview: str
    is_redirect: bool = False
    redirect_target: str = ""
    metadata: Dict[str, Any] = None


class ContentExtractor:
    """Extract and format content from ZIM entries"""
    
    def __init__(self, config: ZimServerConfig, zim_manager: ZimManager):
        self.config = config
        self.zim_manager = zim_manager
        self.logger = logging.getLogger("mcp_zim_server.content_extractor")
    
    def extract_entry_content(self, zim_file: str, entry_path: str, 
                            format_type: str = "text") -> Optional[ExtractedContentInfo]:
        """Extract content from a ZIM entry"""
        try:
            entry = self.zim_manager.get_entry_by_path(zim_file, entry_path)
            if entry is None:
                return None
            
            return self._extract_from_entry(entry, format_type)
            
        except (OSError, ValueError, RuntimeError) as e:
            self.logger.error("Error extracting content from %s in %s: %s", entry_path, zim_file, e)
            return None
    
    def extract_entry_content_by_title(self, zim_file: str, title: str, 
                                     format_type: str = "text") -> Optional[ExtractedContentInfo]:
        """Extract content from a ZIM entry by title"""
        try:
            entry = self.zim_manager.get_entry_by_title(zim_file, title)
            if entry is None:
                return None
            
            return self._extract_from_entry(entry, format_type)
            
        except (OSError, ValueError, RuntimeError) as e:
            self.logger.error("Error extracting content by title '%s' in %s: %s", title, zim_file, e)
            return None
    
    def _extract_from_entry(self, entry: libzim.reader.Entry, 
                           format_type: str = "text") -> ExtractedContentInfo:
        """Extract content from a ZIM entry object"""
        try:
            # Get the item
            item = entry.get_item()
            content_bytes = bytes(item.content)
            
            # Handle redirects
            if entry.is_redirect:
                return ExtractedContentInfo(
                    path=entry.path,
                    title=entry.title,
                    content="[This is a redirect]",
                    content_type="redirect",
                    content_length=0,
                    preview="[Redirect]",
                    is_redirect=True,
                    redirect_target=entry.redirect_entry.path if hasattr(entry, 'redirect_entry') else "",
                    metadata={}
                )
            
            # Decode content
            content = self._decode_content(content_bytes)
            
            # Format content based on requested type
            formatted_content = self._format_content(content, format_type)
            
            # Create preview
            preview = extract_text_preview(formatted_content, 200)
            
            # Truncate if too long
            if len(formatted_content) > self.config.max_content_length:
                formatted_content = truncate_text(formatted_content, self.config.max_content_length)
            
            return ExtractedContentInfo(
                path=entry.path,
                title=entry.title,
                content=formatted_content,
                content_type=format_type,
                content_length=len(content_bytes),
                preview=preview,
                is_redirect=False,
                metadata=self._extract_metadata(content)
            )
            
        except (OSError, ValueError, RuntimeError) as e:
            self.logger.error("Error extracting from entry %s: %s", entry.path, e)
            raise
    
    def _decode_content(self, content_bytes: bytes) -> str:
        """Decode content bytes to string"""
        try:
            # Try UTF-8 first
            return content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            try:
                # Try Latin-1 as fallback
                return content_bytes.decode('latin-1')
            except UnicodeDecodeError:
                # Last resort: replace errors
                return content_bytes.decode('utf-8', errors='replace')
    
    def _format_content(self, content: str, format_type: str) -> str:
        """Format content based on requested type"""
        if format_type == "text":
            return clean_html_content(content)
        elif format_type == "html":
            return content
        elif format_type == "raw":
            return content
        else:
            # Default to text
            return clean_html_content(content)
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from content"""
        metadata = {}
        
        # Extract basic HTML metadata if present
        if '<' in content and '>' in content:
            # Extract title from HTML
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                metadata['html_title'] = title_match.group(1).strip()
            
            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', 
                                 content, re.IGNORECASE)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()
            
            # Count images
            img_count = len(re.findall(r'<img[^>]*>', content, re.IGNORECASE))
            if img_count > 0:
                metadata['image_count'] = img_count
            
            # Count links
            link_count = len(re.findall(r'<a[^>]*href=[^>]*>', content, re.IGNORECASE))
            if link_count > 0:
                metadata['link_count'] = link_count
        
        return metadata
    
    def extract_multiple_contents(self, zim_file: str, entry_paths: List[str], 
                                format_type: str = "text") -> List[ExtractedContentInfo]:
        """Extract content from multiple entries"""
        results = []
        
        for entry_path in entry_paths:
            try:
                content = self.extract_entry_content(zim_file, entry_path, format_type)
                if content:
                    results.append(content)
            except (OSError, ValueError, RuntimeError) as e:
                self.logger.warning("Error extracting content from %s: %s", entry_path, e)
                continue
        
        return results
    
    def extract_search_results_content(self, search_results: List[Any], 
                                     format_type: str = "text") -> List[ExtractedContentInfo]:
        """Extract content from search results"""
        results = []
        
        for search_result in search_results:
            try:
                content = self.extract_entry_content(
                    search_result.zim_file, 
                    search_result.path, 
                    format_type
                )
                if content:
                    # Add search-specific metadata
                    if hasattr(search_result, 'score'):
                        content.metadata = content.metadata or {}
                        content.metadata['search_score'] = search_result.score
                    results.append(content)
            except (OSError, ValueError, RuntimeError) as e:
                self.logger.warning("Error extracting search result content: %s", e)
                continue
        
        return results
    
    def get_content_summary(self, content: str, max_length: int = 500) -> str:
        """Get a summary of content"""
        # Clean HTML if present
        if '<' in content and '>' in content:
            content = clean_html_content(content)
        
        # Extract first paragraph or sentences
        sentences = re.split(r'[.!?]+', content)
        summary = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(summary + sentence) > max_length:
                break
            
            summary += sentence + ". "
        
        return summary.strip()
    
    def extract_table_of_contents(self, content: str) -> List[Dict[str, str]]:
        """Extract table of contents from HTML content"""
        toc = []
        
        # Look for heading tags
        heading_pattern = r'<h([1-6])[^>]*(?:id=["\']([^"\']*)["\'])?[^>]*>(.*?)</h[1-6]>'
        matches = re.findall(heading_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for level, heading_id, heading_text in matches:
            clean_text = clean_html_content(heading_text).strip()
            if clean_text:
                toc.append({
                    'level': int(level),
                    'id': heading_id or '',
                    'text': clean_text
                })
        
        return toc
    
    def extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract links from HTML content"""
        links = []
        
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>'
        matches = re.findall(link_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for href, link_text in matches:
            clean_text = clean_html_content(link_text).strip()
            if clean_text and href:
                links.append({
                    'href': href,
                    'text': clean_text
                })
        
        return links

