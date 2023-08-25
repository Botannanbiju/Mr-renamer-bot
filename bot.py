from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw import layer
from config import Config
from aiohttp import web
from route import web_server

class Bot(Client):

    def __init__(self):
        super().__init__(
            "my_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={"root": "plugins"}
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        if Config.WEBHOOK:
            app = web.Application()
            app.add_routes([web.route("*", web_server)])
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", 8080)
            await site.start()
        print(f"{me.first_name} Is Started.....✨️")
        for id in Config.ADMINS:
            try:
                await self.send_message(id, f"**{me.first_name} Is Started.....✨️**")
            except:
                pass
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**{me.mention} Is Restarted!!**\n\n📅 Date: `{date}`\n⏰ Time: `{time}`\n🌐 Timezone: `Asia/Kolkata`\n\n🉐 Version: `v{__version__} (Layer {layer})`")
            except:
                print("Please make sure this bot is an admin in your log channel")

Bot().run()
        
