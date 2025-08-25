# Request/Response Structure

## Discovering Available ZIM Files

### `list_zim_files`

**Request:**
```json
{
  "tool": "list_zim_files",
  "params": {}
}
```

**Response (Example):**
```json
{
  "status": "success",
  "count": 2,
  "files": [
    {
      "filename": "wikipedia_en_all_maxi_2023-10.zim",
      "title": "Wikipedia (English)",
      "description": "The complete English Wikipedia",
      "size": "95.3 GB",
      "article_count": 6700000,
      "media_count": 9000000,
      "language": "en",
      "creator": "Kiwix",
      "date": "2023-10-01",
      "has_fulltext_index": true,
      "has_title_index": true
    },
    {
      "filename": "gutenberg_en_all_2023-04.zim",
      "title": "Project Gutenberg",
      "description": "A collection of public domain books",
      "size": "50.1 GB",
      "article_count": 60000,
      "media_count": 10000,
      "language": "en",
      "creator": "Kiwix",
      "date": "2023-04-15",
      "has_fulltext_index": true,
      "has_title_index": true
    }
  ]
}
```

## Searching for Content

### `search_zim_files`

**Request:**
```json
{
  "tool": "search_zim_files",
  "params": {
    "query": "Albert Einstein"
  }
}
```

**Response (Example):**
```json
{
  "status": "success",
  "query": "Albert Einstein",
  "count": 3,
  "results": [
    {
      "zim_file": "wikipedia_en_all_maxi_2023-10.zim",
      "path": "A/Albert_Einstein.html",
      "title": "Albert Einstein",
      "score": 0.95,
      "preview": "Albert Einstein was a German-born theoretical physicist...",
      "is_redirect": false
    },
    {
      "zim_file": "wikipedia_en_all_maxi_2023-10.zim",
      "path": "A/Theory_of_relativity.html",
      "title": "Theory of relativity",
      "score": 0.88,
      "preview": "The theory of relativity, or simply relativity, generally encompasses two theories by Albert Einstein...",
      "is_redirect": false
    },
    {
      "zim_file": "gutenberg_en_all_2023-04.zim",
      "path": "E/Einstein_Albert/Relativity.html",
      "title": "Relativity: The Special and the General Theory by Albert Einstein",
      "score": 0.85,
      "preview": "A book by Albert Einstein on the theory of relativity.",
      "is_redirect": false
    }
  ],
  "pagination": {
    "start_offset": 0,
    "max_results": 20,
    "has_more": false
  }
}
```

## Reading an Entry

### `read_zim_entry`

**Request:**
```json
{
  "tool": "read_zim_entry",
  "params": {
    "zim_file": "wikipedia_en_all_maxi_2023-10.zim",
    "entry_path": "A/Albert_Einstein.html",
    "format": "text"
  }
}
```

**Response (Example):**
```json
{
  "status": "success",
  "entry": {
    "path": "A/Albert_Einstein.html",
    "title": "Albert Einstein",
    "content": "Albert Einstein was a German-born theoretical physicist who is widely held to be one of the greatest and most influential scientists of all time... [full text content]",
    "content_length": 150000,
    "format": "text",
    "is_redirect": false
  }
}
```

## Searching and Extracting Content in One Step

### `search_and_extract_content`

**Request:**
```json
{
  "tool": "search_and_extract_content",
  "params": {
    "query": "Theory of relativity",
    "max_results": 1
  }
}
```

**Response (Example):**
```json
{
  "status": "success",
  "query": "Theory of relativity",
  "count": 1,
  "results": [
    {
      "path": "A/Theory_of_relativity.html",
      "title": "Theory of relativity",
      "content": "The theory of relativity, or simply relativity, generally encompasses two theories by Albert Einstein: special relativity and general relativity... [full text content]",
      "content_type": "text",
      "content_length": 120000,
      "preview": "The theory of relativity, or simply relativity, generally encompasses two theories by Albert Einstein...",
      "is_redirect": false,
      "metadata": {}
    }
  ],
  "format": "text"
}
```


