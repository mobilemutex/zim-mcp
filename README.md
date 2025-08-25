# MCP ZIM Server

An MCP (Model Context Protocol) server that provides offline search and content extraction capabilities for Large Language Models (LLMs) using ZIM files. This server allows LLMs to perform deep research and access information in offline environments, replacing the need for live web access.

## Features

- **Offline Search**: Full-text search across millions of articles within ZIM files.
- **Content Extraction**: Extract and format content from ZIM entries in various formats (text, HTML).
- **ZIM File Discovery**: Automatically discover ZIM files in a specified directory.
- **Caching**: In-memory caching for archives, search results, and file info to improve performance.
- **Configurable**: Easily configurable through environment variables.

## Requirements

- Python 3.10+
- `pip` or `uv` for package installation

## Getting Started

Run the [Python package](https://pypi.org/p/zim-mcp) as a CLI command using [`uv`](https://docs.astral.sh/uv/guides/tools/):

```bash
uvx zim-mcp # see --help for more options
```

## Build/Install from GitHub

1.  **Clone the repository or download the source code:**

    ```bash
    git clone https://github.com/mobilemutex/zim-mcp.git
    cd zim-mcp
    ```

2.  **Run with `uv`:**

    ```bash
    uv run zim-mcp
    ```

    **or with `pipx`:**

    ```bash

    pipx install .
    zim-mcp
    ```

    **or with `pip` and `venv`:**
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install .
    zim-mcp
    ```

## Configuration

The server can be configured using the following environment variables:

-   `ZIM_FILES_DIRECTORY`: The directory where your ZIM files are stored. (Default: `./zim_files`)
-   `MAX_SEARCH_RESULTS`: The maximum number of search results to return per query. (Default: `100`)
-   `SEARCH_TIMEOUT`: The timeout for search operations in seconds. (Default: `30`)
-   `LOG_LEVEL`: The logging level for the server. (Default: `INFO`)

## Tools

### `list_zim_files`

Lists all available ZIM files in the configured directory.

-   list_zim_files()
    -   **Parameters**: None
    -   **Returns**: A dictionary containing a list of ZIM files with their metadata.

### `get_zim_metadata`

Gets detailed metadata about a specific ZIM file.

- get_zim_metadata(zim_file: str)
    -   **Parameters**:
        -   `zim_file` (str): The name of the ZIM file.
    -   **Returns**: A dictionary containing detailed metadata for the specified ZIM file.

### `search_zim_files`

Searches for content across one or multiple ZIM files.

- search_zim_files(query: str, zim_files: Optional[List[str]], max_results: int, start_offset: int) 
    -   **Parameters**:
        -   `query` (str): The search query.
        -   `zim_files` (Optional[List[str]]): A list of ZIM files to search. If not provided, all files are searched.
        -   `max_results` (int): The maximum number of results to return. (Default: 20)
        -   `start_offset` (int): The pagination offset. (Default: 0)
    -   **Returns**: A dictionary containing the search results.

### `read_zim_entry`

Reads the content of a specific entry from a ZIM file.

- read_zim_entry(zim_file: str, entry_path: str, format: str)
    -   **Parameters**:
        -   `zim_file` (str): The name of the ZIM file.
        -   `entry_path` (str): The path to the entry.
        -   `format` (str): The output format (`text`, `html`, `raw`). (Default: `text`)
    -   **Returns**: A dictionary containing the entry's content.

### `search_and_extract_content`

Performs a search and returns the full content of the matching entries.

- search_and_extract_content(query: str, ...)
    -   **Parameters**: Similar to `search_zim_files`, with additional content formatting options.
    -   **Returns**: A dictionary containing the search results with their full content.

### `browse_zim_entries`

Browses entries by path or title patterns.

- browse_zim_entries(zim_file: str, ...)
    -   **Parameters**:
        -   `zim_file` (str): The ZIM file to browse.
        -   `path_pattern` (Optional[str]): A pattern to match against entry paths.
        -   `title_pattern` (Optional[str]): A pattern to match against entry titles.
        -   `limit` (int): The maximum number of entries to return.
    -   **Returns**: A list of matching entries.

### `get_random_entries`

Gets a specified number of random entries from ZIM files.

- get_random_entries(zim_files: Optional[List[str]], count: int)
    -   **Parameters**:
        -   `zim_files` (Optional[List[str]]): A list of ZIM files to get entries from.
        -   `count` (int): The number of random entries to return.
    -   **Returns**: A list of random entries.

## Resource Endpoints

The server also exposes the following resource endpoints:

-   `zim://files`: Lists all available ZIM files.
-   `zim://file/{filename}/metadata`: Provides metadata for a specific ZIM file.
-   `zim://file/{filename}/entry/{path}`: Provides the content of a specific entry.

## Usage

This Python package is published to PyPI as [zim-mcp](https://pypi.org/p/zim-mcp) and can be installed and run with [pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#install-a-package), [pipx](https://pipx.pypa.io/), [uv](https://docs.astral.sh/uv/), [poetry](https://python-poetry.org/), or any Python package manager.

```text
$ pipx install zim-mcp
$ zim-mcp --help

usage: zim-mcp [-h] [--transport {stdio,streamable-http,sse}] [--port PORT]

MCP ZIM Server

options:
  -h, --help            show this help message and exit
  --transport {stdio,streamable-http,sse}
                        Transport type (default: stdio)
  --port PORT           Port for SSE transport (default: 8000)
```

### Running the Server
1.  **Place your ZIM files** in the directory specified by the `ZIM_FILES_DIRECTORY` environment variable (or the default `./zim_files` directory).

2.  **Run the server** using one of the supported transports:

    -   **Standard I/O (stdio):**

        ```bash
        zim-mcp --transport stdio
        ```

    -   **Server-Sent Events (SSE):**

        ```bash
        zim-mcp --transport sse --port 8000
        ```
    
    -   **Server-Sent Events (SSE):**

        ```bash
        zim-mcp --transport streamable-http
        ```

### Using with OpenWeb-UI and MCPO

You can integrate `zim-mcp` with [OpenWeb-UI](https://github.com/open-webui/open-webui) using [MCPO](https://github.com/open-webui/mcpo), an MCP-to-OpenAPI proxy. This allows you to expose `zim-mcp`'s tools through a standard RESTful API, making them accessible to web interfaces and other tools.

#### With `uvx`

You can run `zim-mcp` and `mcpo` together using `uvx`:

```bash
uvx mcpo -- zim-mcp
```

### Standard Input/Output (stdio)

The stdio transport enables communication through standard input and output streams. This is particularly useful for local integrations and command-line tools. See the [spec](https://modelcontextprotocol.io/docs/concepts/transports#built-in-transport-types) for more details.

#### Python

```bash
zim-mcp
```

By default, the Python package will run in `stdio` mode. Because it's using the standard input and output streams, it will look like the tool is hanging without any output, but this is expected.

### Streamable HTTP

Streamable HTTP enables streaming responses over JSON RPC via HTTP POST requests. See the [spec](https://modelcontextprotocol.io/specification/draft/basic/transports#streamable-http) for more details.

By default, the server listens on [127.0.0.1:8000/mcp](https://127.0.0.1/mcp) for client connections. To change any of this, set [FASTMCP_*](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/server/fastmcp/server.py#L78) environment variables. _The server must be running for clients to connect to it._

#### Python

```bash
zim-mcp -t streamable-http
```

By default, the Python package will run in `stdio` mode, so you will have to include `-t streamable-http`.

### Server-sent events (SSE)

> [!WARNING]
> The MCP communiity considers this a legacy transport portcol and is really intended for backwards compatibility. [Streamable HTTP](#streamable-http) is the recommended replacement.

SSE transport enables server-to-client streaming with Server-Send Events for client-to-server and server-to-client communication. See the [spec](https://modelcontextprotocol.io/docs/concepts/transports#server-sent-events-sse) for more details.

By default, the server listens on [127.0.0.1:8000/sse](https://127.0.0.1/sse) for client connections. To change any of this, set [FASTMCP_*](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/server/fastmcp/server.py#L78) environment variables. _The server must be running for clients to connect to it._

#### Python

```bash
zim-mcp -t sse
```

By default, the Python package will run in `stdio` mode, so you will have to include `-t sse`.

## Integrations

### Claude Desktop, Roo Code, etc.

Add the following JSON block to your `claude_desktop_config.json` or `mcp.json` file:

```json
{
  "mcpServers": {
    "zim-mcp": {
      "command": "uvx",
      "args": ["zim_mcp", "--transport", "stdio"],
      "env": {
        "LOG_LEVEL": "INFO",
        "ZIM_FILES_DIRECTORY": "~/zim_files"
      }
    }
  }
}
```

## Development

Contributions are welcome! If you want to contribute to the development of the MCP ZIM Server, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and write tests.
4.  Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


