from pyrogram.errors import FloodWait
import asyncio

    async def start(self):
        try:
            await super().start()
        except FloodWait as e:
            wait_time = e.value
            print(f"[FloodWait] Telegram says wait {wait_time} seconds before restarting...")
            await asyncio.sleep(wait_time)
            return await self.start()  # Retry after waiting

        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by 𝘾𝙤𝙙𝙚 𝕏 𝘽𝙤𝙩𝙯\nhttps://t.me/CodeXBotz")
        self.username = usr_bot_me.username
