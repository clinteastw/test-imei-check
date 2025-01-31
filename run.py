import asyncio

import uvicorn

from api.main import app
from api.models.tokens import APIToken
from bot.bot import start_bot
from bot.models import TgUser
from config import ADMIN_IDS, BOT_API_TOKEN


async def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await APIToken.add_admin_token(BOT_API_TOKEN)
    await TgUser.add_users_to_whitelist(ADMIN_IDS)
    await asyncio.gather(start_bot(), start_fastapi())

if __name__ == "__main__":
    asyncio.run(main())
    
    