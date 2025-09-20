# Git MCP Server

A Model Context Protocol (MCP) server that provides Git operations through standardized tools. This server allows AI assistants and other MCP clients to interact with Git repositories programmatically.

## What This Project Does

This MCP server exposes four main Git operations as MCP tools:

- **`git_add`** - Add files to the Git staging area with support for specific files, all files, interactive mode, and patch mode
- **`git_commit`** - Create commits with custom messages, support for staging all files, and amend functionality
- **`git_push`** - Push commits to remote repositories with configurable remote, branch, force push, and upstream tracking
- **`git_status`** - Get the current status of a Git repository to see what files can be added

All tools support:
- Working with any Git repository by specifying a `repository_path`
- Comprehensive error handling and timeout protection
- Detailed response information including command output and status

## Prerequisites

- Python 3.12 or higher
- Git installed on your system
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd git-mcp-server
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

## Running the Server

### Development Mode

Run the server directly:
```bash
python main.py
```

The server will start on `http://0.0.0.0:5001` by default.

### Production Mode

For production use, you can run it with a WSGI server like gunicorn:
```bash
uv run gunicorn main:mcp.app -b 0.0.0.0:5001
```

## Adding to Cursor IDE

To use this MCP server with Cursor, you need to configure it in your Cursor settings:

1. Open Cursor settings (Cmd/Ctrl + ,)
2. Navigate to "Features" → "Model Context Protocol"
3. Add a new MCP server configuration:

```json
{
  "mcpServers": {
    "git-mcp-server": {
      "command": "python",
      "args": ["/absolute/path/to/your/git-mcp-server/main.py"],
      "env": {}
    }
  }
}
```

Replace `/absolute/path/to/your/git-mcp-server/main.py` with the actual absolute path to your `main.py` file.

### Alternative Configuration for HTTP Transport

If you prefer to run the server as a standalone HTTP service:

```json
{
  "mcpServers": {
    "git-mcp-server": {
      "command": "uv",
      "args": ["run", "python", "/absolute/path/to/your/git-mcp-server/main.py"],
      "env": {}
    }
  }
}
```

4. Restart Cursor to load the new MCP server
5. The Git tools should now be available in your Cursor chat interface

## Usage Examples

Once configured in Cursor, you can use the Git tools in your chat:

- "Add all modified files to staging"
- "Commit the staged changes with message 'Fix bug in user authentication'"
- "Push the current branch to origin"
- "Show me the git status of this repository"

## API Reference

### git_add
Add files to the Git staging area.

**Parameters:**
- `files` (optional): Space-separated list of file paths
- `all_files` (bool): Add all modified files (default: False)
- `interactive` (bool): Interactive mode (default: False)
- `patch` (bool): Patch mode (default: False)
- `repository_path` (optional): Path to git repository

### git_commit
Create a Git commit.

**Parameters:**
- `message` (required): Commit message
- `all_files` (bool): Stage all files before committing (default: False)
- `amend` (bool): Amend previous commit (default: False)
- `repository_path` (optional): Path to git repository

### git_push
Push commits to remote repository.

**Parameters:**
- `remote` (str): Remote name (default: "origin")
- `branch` (optional): Branch name (defaults to current branch)
- `force` (bool): Force push (default: False)
- `set_upstream` (bool): Set upstream tracking (default: False)
- `repository_path` (optional): Path to git repository

### git_status
Get Git repository status.

**Parameters:**
- `repository_path` (optional): Path to git repository

## Security Considerations

- The server runs Git commands with the same permissions as the user running it
- Be cautious with `force` push operations
- The server validates repository paths and checks for Git repositories before executing commands
- All commands have timeout protection (10-120 seconds depending on operation)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]
