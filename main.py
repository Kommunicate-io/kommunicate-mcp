# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict
from config import KOMMUNICATE_API_KEY, KOMMUNICATE_BASE_URL

# Initialize FastMCP server
#mcp = FastMCP("KommunicateDemo")
# Specify dependencies for deployment and development
mcp = FastMCP("KommunicateDemo", dependencies=["requests"])


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

# 👤 Tool: Update User Details in Kommunicate
@mcp.tool()
def update_user_details(userId: str, email: str = None, displayName: str = None, imageLink: str = None, metadata: Dict = None) -> Dict:
    """
    Update user details in Kommunicate.
    
    Args:
        userId: The user ID to be updated.
        email: (Optional) User's email address.
        displayName: (Optional) User's display name.
        imageLink: (Optional) URL of user's profile image.
        metadata: (Optional) Dictionary of key-value pairs for additional user metadata.
    
    Returns:
        JSON response from Kommunicate API.
    
    Example:
        update_user_details(
            userId="user123",
            email="user@example.com",
            displayName="John Doe",
            imageLink="https://example.com/profile.jpg",
            metadata={"key1": "value1", "key2": "value2"}
        )
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/user/update"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json",
        "Of-User-Id": userId
    }
    
    # Build payload with only provided fields
    payload = {}
    if email is not None:
        payload["email"] = email
    if displayName is not None:
        payload["displayName"] = displayName
    if imageLink is not None:
        payload["imageLink"] = imageLink
    if metadata is not None:
        payload["metadata"] = metadata

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# 👥 Tool: Change Conversation Assignee in Kommunicate
@mcp.tool()
def change_conversation_assignee(groupId: str, assignee: str, ofUserId: str = "bot", sendNotifyMessage: bool = True, takeOverFromBot: bool = True) -> Dict:
    """
    Change the assignee of a conversation in Kommunicate.
    
    Args:
        groupId: The unique identifier of the conversation.
        assignee: The email ID of the human agent to assign the conversation to.
        ofUserId: (Optional) The user ID to include in the Of-User-Id header. Defaults to "bot".
        sendNotifyMessage: (Optional) Whether to send a notification message about the assignee change. Defaults to True.
        takeOverFromBot: (Optional) Whether to remove all bots from the conversation. Defaults to True.
    
    Returns:
        JSON response from Kommunicate API with one of the following statuses:
        - "updated": Successfully changed assignee
        - "already updated": Conversation already assigned to the specified agent
        - "AGENT_IS_ALREADY_ENGAGED": Agent has reached their maximum handling limit
        - Error responses for invalid agent ID or conversation ID
    
    Example:
        change_conversation_assignee(
            groupId="support-12345",
            assignee="agent@example.com",
            sendNotifyMessage=False
        )
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/group/assignee/change"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json",
        "Of-User-Id": ofUserId
    }
    
    # Using query parameters as per API documentation
    params = {
        "groupId": groupId,
        "assignee": assignee,
        "sendNotifyMessage": str(sendNotifyMessage).lower(),
        "takeOverFromBot": str(takeOverFromBot).lower()
    }

    response = requests.patch(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

# 👤 Tool: Get User Details from Kommunicate
@mcp.tool()
def get_user_details(userIdList: List[str]) -> List[Dict]:
    """
    Get details for a list of users from Kommunicate.
    
    Args:
        userIdList: List of user IDs to fetch details for.
    
    Returns:
        List of user detail objects containing:
        - userId: User ID of the user
        - userName: Display name of the user
        - connected: Current connected status (online/offline)
        - lastSeenAtTime: Timestamp of last seen
        - createdAtTime: Timestamp of user creation
        - imageLink: Profile image URL
        - deactivated: User active/inactive status
        - phoneNumber: User's phone number
        - unreadCount: Total unread message count
        - lastLoggedInAtTime: Timestamp of last login
        - lastMessageAtTime: Timestamp of last message
    
    Example:
        get_user_details(["user123", "user456"])
    """
    url = f"{KOMMUNICATE_BASE_URL}/rest/ws/user/v2/detail"
    headers = {
        "Api-Key": KOMMUNICATE_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "userIdList": userIdList
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# 🚀 Run the server
if __name__ == "__main__":
    mcp.run()
