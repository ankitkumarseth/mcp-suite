import os
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

mcp = FastMCP("Trello-MCP-Server")

def get_auth_params():
    return {'key': TRELLO_API_KEY, 'token': TRELLO_TOKEN}

def check_auth():
    if not TRELLO_API_KEY or not TRELLO_TOKEN:
        raise ValueError("Missing Trello API Key or Token in environment variables.")

# --- READ TOOLS ---

@mcp.tool()
async def get_boards() -> str:
    """Get all boards for the authenticated user. Returns board names and their IDs."""
    check_auth()
    url = "https://api.trello.com/1/members/me/boards"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={**get_auth_params(), 'fields': 'name,id'})
        if resp.status_code == 200:
            boards = resp.json()
            return "\n".join([f"Board: {b['name']} (ID: {b['id']})" for b in boards]) if boards else "No boards found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_lists(board_id: str) -> str:
    """Get all lists on a specific board. Returns list names and their IDs."""
    check_auth()
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={**get_auth_params(), 'fields': 'name,id'})
        if resp.status_code == 200:
            lists = resp.json()
            return "\n".join([f"List: {lst['name']} (ID: {lst['id']})" for lst in lists]) if lists else "No lists found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_cards(list_id: str) -> str:
    """Get all cards in a specific list. Returns card names and their IDs."""
    check_auth()
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params={**get_auth_params(), 'fields': 'name,id'})
        if resp.status_code == 200:
            cards = resp.json()
            return "\n".join([f"Card: {card['name']} (ID: {card['id']})" for card in cards]) if cards else "No cards found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_labels(board_id: str) -> str:
    """Get all labels on a specific board. Returns label names, colors, and their IDs."""
    check_auth()
    url = f"https://api.trello.com/1/boards/{board_id}/labels"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=get_auth_params())
        if resp.status_code == 200:
            labels = resp.json()
            return "\n".join([f"Label: {lbl.get('name', 'Unnamed')} (Color: {lbl.get('color')}, ID: {lbl['id']})" for lbl in labels]) if labels else "No labels found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_checklists(card_id: str) -> str:
    """Get all checklists on a specific card. Returns checklist names and their IDs."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=get_auth_params())
        if resp.status_code == 200:
            checklists = resp.json()
            return "\n".join([f"Checklist: {cl['name']} (ID: {cl['id']})" for cl in checklists]) if checklists else "No checklists found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_card_details(card_id: str) -> str:
    """Get detailed information about a specific card including description, due date, and URL."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=get_auth_params())
        if resp.status_code == 200:
            card = resp.json()
            return f"Name: {card.get('name')}\nDesc: {card.get('desc')}\nDue: {card.get('due')}\nURL: {card.get('url')}"
        return f"Error: {resp.text}"

@mcp.tool()
async def get_comments(card_id: str) -> str:
    """Get all comments on a specific card."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}/actions"
    params = {**get_auth_params(), 'filter': 'commentCard'}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            actions = resp.json()
            return "\n".join([f"Comment by {a.get('memberCreator', {}).get('fullName')}: {a.get('data', {}).get('text')}" for a in actions]) if actions else "No comments found."
        return f"Error: {resp.text}"

@mcp.tool()
async def get_attachments(card_id: str) -> str:
    """Get all attachments on a specific card."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=get_auth_params())
        if resp.status_code == 200:
            attachments = resp.json()
            return "\n".join([f"Attachment: {att.get('name')} (URL: {att.get('url')})" for att in attachments]) if attachments else "No attachments found."
        return f"Error: {resp.text}"


# --- WRITE TOOLS ---

@mcp.tool()
async def create_list(board_id: str, name: str) -> str:
    """Create a new list on a board. Returns the new List ID."""
    check_auth()
    url = "https://api.trello.com/1/lists"
    params = {**get_auth_params(), 'idBoard': board_id, 'name': name}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return f"Created List ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def update_list(list_id: str, name: str) -> str:
    """Update a list's name."""
    check_auth()
    url = f"https://api.trello.com/1/lists/{list_id}"
    params = {**get_auth_params(), 'name': name}
    async with httpx.AsyncClient() as client:
        resp = await client.put(url, params=params)
        return f"Updated List ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def create_card(list_id: str, name: str, desc: str = "") -> str:
    """Create a new card in a list. Returns the new Card ID."""
    check_auth()
    url = "https://api.trello.com/1/cards"
    params = {**get_auth_params(), 'idList': list_id, 'name': name, 'desc': desc}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return f"Created Card ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def update_card(card_id: str, name: str = None, desc: str = None, list_id: str = None, due: str = None, pos: str = None) -> str:
    """Update a card's name, description, list, due date (ISO string), or position (e.g., 'top', 'bottom', or numeric)."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = get_auth_params()
    if name: params['name'] = name
    if desc: params['desc'] = desc
    if list_id: params['idList'] = list_id
    if due: params['due'] = due
    if pos: params['pos'] = pos
    
    async with httpx.AsyncClient() as client:
        resp = await client.put(url, params=params)
        return f"Updated Card ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def add_label_to_card(card_id: str, label_id: str) -> str:
    """Attach an existing label to a card using the label's ID."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}/idLabels"
    params = {**get_auth_params(), 'value': label_id}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return "Label attached successfully." if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def delete_card(card_id: str) -> str:
    """Delete a card permanently."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, params=get_auth_params())
        return "Card deleted successfully." if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def add_checklist(card_id: str, name: str) -> str:
    """Add a new checklist to a card. Returns the new Checklist ID."""
    check_auth()
    url = "https://api.trello.com/1/checklists"
    params = {**get_auth_params(), 'idCard': card_id, 'name': name}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return f"Created Checklist ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def add_checklist_item(checklist_id: str, name: str) -> str:
    """Add an item to an existing checklist."""
    check_auth()
    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    params = {**get_auth_params(), 'name': name}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return f"Added Item ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def add_comment(card_id: str, text: str) -> str:
    """Add a comment to a card."""
    check_auth()
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {**get_auth_params(), 'text': text}
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, params=params)
        return "Comment added successfully." if resp.status_code == 200 else f"Error: {resp.text}"

@mcp.tool()
async def add_attachment(card_id: str, url: str, name: str = None) -> str:
    """Add a URL link attachment to a card."""
    check_auth()
    api_url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    params = {**get_auth_params(), 'url': url}
    if name: params['name'] = name
    async with httpx.AsyncClient() as client:
        resp = await client.post(api_url, params=params)
        return f"Attachment added successfully. ID: {resp.json().get('id')}" if resp.status_code == 200 else f"Error: {resp.text}"

if __name__ == "__main__":
    mcp.run()
