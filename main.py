# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict

# Initialize FastMCP server
#mcp = FastMCP("KommunicateDemo")
# Specify dependencies for deployment and development
mcp = FastMCP("KommunicateDemo", dependencies=["requests"])

# Kommunicate configuration
KOMMUNICATE_API_KEY = "<KOmmunicate-APIKEY>"  # 🔐 Replace with your API key
KOMMUNICATE_BASE_URL = "https://services.kommunicate.io"

# 🧠 Sample tool: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# 🌐 Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# 🛠️ Tool: Create a new Kommunicate conversation
@mcp.tool()
def create_conversation(groupName: str, groupMemberList: List[str]) -> Dict:
    """
    Create a new conversation in Kommunicate.
    
    Args:
        groupName: Name of the group conversation.
        groupMemberList: List of userIds or email addresses of agents/bots/users.
    
    Returns:
        JSON response from Kommunicate API.
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/group/conversation"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "groupName": groupName,
        "groupMemberList": groupMemberList
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# 💬 Tool: Send a message to an existing Kommunicate conversation
@mcp.tool()
def send_message(groupId: str, fromUserName: str, message: str) -> Dict:
    """
    Send a message to a Kommunicate conversation.
    
    Args:
        groupId: The group ID of the conversation.
        fromUserName: The userId of the fromUserName.
        message: The message text.
    
    Returns:
        JSON response from Kommunicate API.
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/message/v2/send"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "groupId": groupId,
        "fromUserName": fromUserName,
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# 🛠️ Tool: Change Conversation Status in Kommunicate
@mcp.tool()
def change_conversation_status(groupId: str, status: int, ofUserId: str = "bot") -> Dict:
    """
    Update the status of a specific conversation in Kommunicate.

    Kommunicate conversations can be in different states such as open, resolved, pending, etc.
    This tool allows you to programmatically change the current status of a conversation by 
    providing the unique group ID of the conversation and the new desired status code.

    Parameters:
    - groupId (str): The unique identifier of the conversation (also known as groupId).
    - status (int): The new status to set for the conversation.
        Available status codes:
          - 1: Open — Conversation is active and unresolved.
          - 2: Resolved — Conversation has been completed or closed.
          - 3: Pending — Awaiting response or further action.
          - 4: Bot Closed — Conversation closed automatically by bot.
          - 5: Snoozed — Temporarily inactive or deferred.
    - ofUserId (str, optional): The user ID to include in the Of-User-Id header. 
        Defaults to "bot".

    Returns:
        JSON response from Kommunicate API.

    Example:
    To mark a conversation with group ID "support-12345" as resolved, use:
        change_conversation_status(groupId="support-12345", status=2)
    
    To specify a different user:
        change_conversation_status(groupId="support-12345", status=2, ofUserId="user@example.com")
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/group/status/change"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json",
        "Of-User-Id": ofUserId
    }
    
    # Using query parameters instead of JSON payload
    params = {
        "groupId": groupId,
        "status": status
    }

    response = requests.patch(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

# 🚀 Run the server
if __name__ == "__main__":
    mcp.run()
