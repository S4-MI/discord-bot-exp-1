import discord
from discord.ext import commands
from config import DISCORD_TOKEN, NOTIFICATION_CHANNEL_ID
from notifications import NotificationManager
from tasks import TaskManager
from commands import CommandManager

# Configure intents
intents = discord.Intents.default()
intents.message_content = True


class ContestBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.notification_channel_id = NOTIFICATION_CHANNEL_ID

    async def setup_hook(self):
        self.notification_manager = NotificationManager(self)
        self.task_manager = TaskManager(self, self.notification_manager)

        # Add commands as a cog
        await self.add_cog(CommandManager(self))

    async def on_ready(self):
        print(f'Bot logged in as {self.user}')
        channel = self.get_channel(self.notification_channel_id)
        await channel.send("Bot is ready!")


# Run the bot
if __name__ == "__main__":
    bot = ContestBot()
    bot.run(DISCORD_TOKEN)
