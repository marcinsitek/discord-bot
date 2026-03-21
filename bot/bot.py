import discord
from bot.message_handler import MessageHandler
from bot.config import logger

class DiscordBot(discord.Client):

    def __init__(self, handler: MessageHandler, **kwargs):
        self.handler = handler

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, **kwargs)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")

    async def on_message(self, message):

        if message.author == self.user:
            return

        if self.user in message.mentions:
            logger.info("Message for bot received")
            response = await self.handler.process_message(message)
            logger.info("Sending response ...")
            await message.channel.send(f'Hi, @{message.author} {response}')
            