# MCP ZIM Server - Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- At least 1GB of free disk space (more depending on your ZIM files)

## Installation Methods

### Method 1: Direct Installation (Recommended)

1. **Download the source code:**
   ```bash
   # If you have git
   git clone <repository-url>
   cd mcp-zim-server
   
   # Or download and extract the ZIP file
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the installation:**
   ```bash
   python -m mcp_zim_server --help
   ```

### Method 2: Development Installation

1. **Clone and install in development mode:**
   ```bash
   git clone <repository-url>
   cd mcp-zim-server
   pip install -e .
   ```

2. **Test the installation:**
   ```bash
   mcp-zim-server --help
   ```

## Setting Up ZIM Files

1. **Create a directory for your ZIM files:**
   ```bash
   mkdir zim_files
   ```

2. **Download ZIM files from Kiwix:**
   - Visit https://library.kiwix.org/
   - Download ZIM files for the content you want (Wikipedia, Project Gutenberg, etc.)
   - Place them in your `zim_files` directory

3. **Example ZIM files to try:**
   - Wikipedia (English): `wikipedia_en_all_maxi_2023-10.zim` (very large, ~95GB)
   - Wikipedia (Simple English): `wikipedia_en_simple_all_maxi_2023-10.zim` (smaller, ~1GB)
   - Project Gutenberg: `gutenberg_en_all_2023-04.zim` (~50GB)

## Configuration

1. **Copy the example configuration:**
   ```bash
   cp examples/config.env .env
   ```

2. **Edit the configuration:**
   ```bash
   nano .env
   ```

3. **Key settings to configure:**
   - `ZIM_FILES_DIRECTORY`: Path to your ZIM files
   - `MAX_SEARCH_RESULTS`: Maximum search results per query
   - `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Running the Server

### For MCP Clients (Claude Desktop, etc.)

1. **Add to your MCP client configuration:**
   ```json
   {
     "mcpServers": {
       "zim-server": {
         "command": "python",
         "args": ["-m", "mcp_zim_server", "--transport", "stdio"],
         "env": {
           "ZIM_FILES_DIRECTORY": "/path/to/your/zim/files"
         }
       }
     }
   }
   ```

2. **Restart your MCP client** to load the server.

### For Testing (SSE Mode)

1. **Run the server:**
   ```bash
   python -m mcp_zim_server --transport sse --port 8000
   ```

2. **Test with curl:**
   ```bash
   curl http://localhost:8000/sse
   ```

## Verification

1. **Check that ZIM files are discovered:**
   - The server logs should show "Discovered X ZIM files" on startup
   - If it shows 0, check your ZIM_FILES_DIRECTORY path

2. **Test basic functionality:**
   ```bash
   python test_mcp_server.py
   ```

## Troubleshooting

If you encounter issues, see the [Troubleshooting Guide](docs/troubleshooting.md) for common solutions.

## Next Steps

- Read the [Usage Examples](docs/usage_examples.md) to learn how to use the tools
- Configure your MCP client to use the server
- Start exploring your ZIM files with the LLM!

