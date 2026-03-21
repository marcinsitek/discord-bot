from bot.bot import DiscordBot
from bot.message_handler import MessageHandler
from bot.llm import LLMChatbot
from bot.config import (
    DISCORD_TOKEN,
    MODEL_NAME,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    MESSAGES_SCHEMA,
    MESSAGES_TABLE,
    logger
)
from db.db import DBClient



handler = MessageHandler(
    dbclient=DBClient(
        dbname=POSTGRES_DB, 
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST
    ),
    llm=LLMChatbot(model_name=MODEL_NAME),
    messages_schema=MESSAGES_SCHEMA,
    messages_table=MESSAGES_TABLE
)

bot = DiscordBot(handler=handler)

logger.info("Running bot ...")
bot.run(DISCORD_TOKEN)
