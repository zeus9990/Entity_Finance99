import discord, asyncio, sys, traceback, config
from discord.ext import commands

discord.utils.setup_logging()

initial_extensions = [
    "Cogs.admin",
    "Cogs.event",
    "Cogs.user"
]

class MyClient(commands.Bot):

    def __init__(self):
        super().__init__(
        command_prefix=".",
        intents=discord.Intents.all(),
        case_insensitive=True,
        strip_after_prefix=True,
        )
    
    async def on_ready(self):
        print(f"{self.user.name} is online.")
        
    async def setup_hook(self) -> None:
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"{extension} loaded successfully")
            except Exception as error:
                print(f"Error loading {extension}", file=sys.stderr)
                traceback.print_exc()
        await self.tree.sync()
  
    async def start_client(self):
        await self.start(config.TOKEN)

asyncio.run(MyClient().start_client())
