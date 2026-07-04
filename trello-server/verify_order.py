import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
LIST_ID = "6a43df1dc853bec2589ad4b6"

async def verify_order():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.trello.com/1/lists/{LIST_ID}/cards",
            params={'key': TRELLO_API_KEY, 'token': TRELLO_TOKEN, 'fields': 'name,pos'}
        )
        cards = resp.json()
        
        # Cards returned by this endpoint are already sorted by pos in Trello
        for i, c in enumerate(cards):
            print(f"{i+1:02d}. {c['name']} (pos: {c['pos']})")

if __name__ == "__main__":
    asyncio.run(verify_order())
