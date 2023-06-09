import discord
from discord.ext import commands
from common import const


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=const.PREFIX,
            intents=discord.Intents.all(),
            sync_command=True,
        )

        self.initial_extension = [
            "Cogs.error_handler",
            "Cogs.voice_channel_handler",
            "Cogs.voice_channel_log_handler",
            "Cogs.role_handler",
            "Cogs.channel_entry_handler",
            "Cogs.self_description_handler",
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)

        await bot.tree.sync()

    async def on_ready(self):
        print(f"DISCORD BOT : {self.user}")
        print(
            f"Discord Version : {discord.__version__}")
        print(f"On ready")


if __name__ == '__main__':
    bot = Bot()
    bot.run(const.TOKEN)
