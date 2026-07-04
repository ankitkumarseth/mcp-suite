# Trello MCP Server

A fully featured Model Context Protocol (MCP) server for Trello. This server provides read and write tools to allow AI agents to view, manage, and update Trello boards, lists, cards, checklists, labels, and attachments natively.

## Prerequisites

1. Python 3.10+
2. [uv](https://github.com/astral-sh/uv) (for dependency management)
3. Trello Developer API Key and Token

### Generating Trello Credentials
1. Go to [Trello Power-Ups Admin](https://trello.com/power-ups/admin) and create a new integration to get your **API Key**.
2. Click on the "Token" link on the same page to generate a long-lived **Server Token** that grants authorization to your account.

## Installation & Setup

1. Clone this repository or navigate to this folder.
2. Ensure you have `uv` installed (`brew install uv`).
3. Set up your environment variables:
   Copy `.env.example` to `.env` and fill in your credentials.

```bash
cp .env.example .env
```

`.env` should look like this:
```env
TRELLO_API_KEY=your_api_key_here
TRELLO_TOKEN=your_token_here
```

## Global MCP Integration (Google Antigravity)

To make this server available globally to your AGY agents across any directory, you must define it in the global config:

1. Open or create `~/.gemini/config/mcp_config.json`
2. Add this server using absolute paths to both the `uv` executable and `main.py`:

```json
{
  "mcpServers": {
    "trello-server": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "/absolute/path/to/Workspace/mcp-suite/trello-server/main.py"
      ]
    }
  }
}
```

## Available Tools

This MCP server provides the following native tools for agents:

### Read Tools
- `get_boards()`: Lists all boards for the authenticated user.
- `get_lists(board_id)`: Lists all lists on a specific board.
- `get_cards(list_id)`: Lists all cards in a specific list.
- `get_labels(board_id)`: Gets all labels (names, colors, IDs) on a board.
- `get_checklists(card_id)`: Gets all checklists (names and IDs) on a specific card.

### Write Tools
- `create_list(board_id, name)`: Creates a new list.
- `update_list(list_id, name)`: Renames an existing list.
- `create_card(list_id, name, desc)`: Creates a new card in a list.
- `update_card(card_id, name, desc, list_id, due, pos)`: Fully updates a card (including due dates and positional ordering).
- `delete_card(card_id)`: Permanently deletes a card.
- `add_label_to_card(card_id, label_id)`: Attaches a label (like 'Practice' or 'P0') to a card.
- `add_checklist(card_id, name)`: Creates a new checklist on a card.
- `add_checklist_item(checklist_id, name)`: Appends an item to an existing checklist.
- `add_comment(card_id, text)`: Appends a comment to a card.
- `add_attachment(card_id, url, name)`: Attaches an external URL to a card natively.
