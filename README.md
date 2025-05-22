# Kommunicate MCP Server

A Model Context Protocol (MCP) server implementation for Kommunicate, enabling seamless integration of AI models with the Kommunicate platform.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Kommunicate API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kommunicate-mcp.git
   cd kommunicate-mcp
   ```

2. Install dependencies using uv:
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

   # Installing MCP CLI
   uv add "mcp[cli]"

   # Installs an MCP server into Claude Desktop
   uv run mcp install main.py


## Tools

### Available Tools

1. **Create Conversation**
   - Function: `create_conversation(groupName: str, groupMemberList: List[str]) -> Dict`
   - Description: Creates a new conversation in Kommunicate with specified group name and member list

2. **Send Message**
   - Function: `send_message(groupId: str, fromUserName: str, message: str) -> Dict`
   - Description: Sends a message to an existing Kommunicate conversation

3. **Change Conversation Status**
   - Function: `change_conversation_status(groupId: str, status: int, ofUserId: str = "bot") -> Dict`
   - Description: Updates the status of a specific conversation
   - Status Codes:
     - 1: Open
     - 2: Resolved
     - 3: Pending
     - 4: Bot Closed
     - 5: Snoozed
