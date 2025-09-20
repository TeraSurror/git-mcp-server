#!/usr/bin/env python3
"""
MCP Server with Git operations (add, commit, push) using FastMCP
"""

import subprocess
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Git Operations Server")

@mcp.tool()
def git_add(
    files: Optional[str] = None,
    all_files: bool = False,
    interactive: bool = False,
    patch: bool = False,
    repository_path: Optional[str] = None
) -> dict:
    """
    Add files to the Git staging area.
    
    Args:
        files: Space-separated list of file paths to add (e.g., "file1.txt file2.py")
        all_files: If True, adds all modified files (equivalent to 'git add .')
        interactive: If True, runs git add in interactive mode
        patch: If True, runs git add in patch mode
        repository_path: Path to the git repository (defaults to current directory)
    
    Returns:
        Dictionary with status, message, and command output
    """
    
    try:
        # Set working directory
        if repository_path:
            repo_path = Path(repository_path).resolve()
            if not repo_path.exists():
                return {
                    "status": "error",
                    "message": f"Repository path does not exist: {repository_path}"
                }
        else:
            repo_path = Path.cwd()
        
        # Check if it's a git repository
        if not (repo_path / ".git").exists():
            return {
                "status": "error",
                "message": f"Not a git repository: {repo_path}"
            }
        
        # Build git add command
        cmd = ["git", "add"]
        
        if interactive:
            cmd.append("--interactive")
        elif patch:
            cmd.append("--patch")
        elif all_files:
            cmd.append(".")
        elif files:
            # Split files string and add each file
            file_list = files.strip().split()
            cmd.extend(file_list)
        else:
            return {
                "status": "error",
                "message": "Must specify either files, all_files=True, interactive=True, or patch=True"
            }
        
        # Execute the git add command
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Files successfully added to staging area",
                "command": " ".join(cmd),
                "stdout": result.stdout.strip() if result.stdout.strip() else "No output",
                "repository_path": str(repo_path)
            }
        else:
            return {
                "status": "error",
                "message": "Git add command failed",
                "command": " ".join(cmd),
                "stderr": result.stderr.strip(),
                "repository_path": str(repo_path)
            }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Git add command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def git_commit(
    message: str,
    all_files: bool = False,
    amend: bool = False,
    repository_path: Optional[str] = None
) -> dict:
    """
    Create a Git commit with the staged changes.
    
    Args:
        message: Commit message (required)
        all_files: If True, automatically stage all modified files before committing
        amend: If True, amend the previous commit instead of creating a new one
        repository_path: Path to the git repository (defaults to current directory)
    
    Returns:
        Dictionary with status, message, and command output
    """
    
    try:
        if not message.strip():
            return {
                "status": "error",
                "message": "Commit message cannot be empty"
            }
        
        # Set working directory
        if repository_path:
            repo_path = Path(repository_path).resolve()
            if not repo_path.exists():
                return {
                    "status": "error",
                    "message": f"Repository path does not exist: {repository_path}"
                }
        else:
            repo_path = Path.cwd()
        
        # Check if it's a git repository
        if not (repo_path / ".git").exists():
            return {
                "status": "error",
                "message": f"Not a git repository: {repo_path}"
            }
        
        # Build git commit command
        cmd = ["git", "commit", "-m", message]
        
        if all_files:
            cmd.insert(2, "-a")  # Insert after "git commit"
        
        if amend:
            cmd.insert(2, "--amend")
        
        # Execute the git commit command
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Commit created successfully",
                "command": " ".join(cmd),
                "stdout": result.stdout.strip(),
                "repository_path": str(repo_path)
            }
        else:
            return {
                "status": "error",
                "message": "Git commit command failed",
                "command": " ".join(cmd),
                "stderr": result.stderr.strip(),
                "repository_path": str(repo_path)
            }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Git commit command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def git_push(
    remote: str = "origin",
    branch: Optional[str] = None,
    force: bool = False,
    set_upstream: bool = False,
    repository_path: Optional[str] = None
) -> dict:
    """
    Push commits to a remote Git repository.
    
    Args:
        remote: Name of the remote repository (default: "origin")
        branch: Branch name to push (if None, pushes current branch)
        force: If True, force push (use with caution!)
        set_upstream: If True, set upstream tracking for the branch
        repository_path: Path to the git repository (defaults to current directory)
    
    Returns:
        Dictionary with status, message, and command output
    """
    
    try:
        # Set working directory
        if repository_path:
            repo_path = Path(repository_path).resolve()
            if not repo_path.exists():
                return {
                    "status": "error",
                    "message": f"Repository path does not exist: {repository_path}"
                }
        else:
            repo_path = Path.cwd()
        
        # Check if it's a git repository
        if not (repo_path / ".git").exists():
            return {
                "status": "error",
                "message": f"Not a git repository: {repo_path}"
            }
        
        # Get current branch if no branch specified
        if branch is None:
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if branch_result.returncode == 0:
                branch = branch_result.stdout.strip()
                if not branch:
                    return {
                        "status": "error",
                        "message": "Could not determine current branch"
                    }
            else:
                return {
                    "status": "error",
                    "message": "Failed to get current branch",
                    "stderr": branch_result.stderr.strip()
                }
        
        # Build git push command
        cmd = ["git", "push"]
        
        if set_upstream:
            cmd.extend(["-u", remote, branch])
        else:
            cmd.extend([remote, branch])
        
        if force:
            cmd.insert(2, "--force")  # Insert after "git push"
        
        # Execute the git push command
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120  # Longer timeout for push operations
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": f"Successfully pushed to {remote}/{branch}",
                "command": " ".join(cmd),
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),  # Push info often goes to stderr
                "repository_path": str(repo_path)
            }
        else:
            return {
                "status": "error",
                "message": f"Git push to {remote}/{branch} failed",
                "command": " ".join(cmd),
                "stderr": result.stderr.strip(),
                "repository_path": str(repo_path)
            }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Git push command timed out after 2 minutes"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

@mcp.tool()
def git_status(repository_path: Optional[str] = None) -> dict:
    """
    Get the current git status to see what files can be added.
    
    Args:
        repository_path: Path to the git repository (defaults to current directory)
    
    Returns:
        Dictionary with git status information
    """
    
    try:
        # Set working directory
        if repository_path:
            repo_path = Path(repository_path).resolve()
            if not repo_path.exists():
                return {
                    "status": "error",
                    "message": f"Repository path does not exist: {repository_path}"
                }
        else:
            repo_path = Path.cwd()
        
        # Check if it's a git repository
        if not (repo_path / ".git").exists():
            return {
                "status": "error",
                "message": f"Not a git repository: {repo_path}"
            }
        
        # Get git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "repository_path": str(repo_path),
                "porcelain_output": result.stdout.strip(),
                "message": "Git status retrieved successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Git status command failed",
                "stderr": result.stderr.strip()
            }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Git status command timed out"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="http", host="0.0.0.0", port=5001)