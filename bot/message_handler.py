import re

from bot.llm import LLMChatbot
from bot.config import logger
from db.db import DBClient

class MessageHandler:

    def __init__(
            self, 
            dbclient: DBClient, 
            llm: LLMChatbot, 
            messages_schema: str, 
            messages_table: str
    ):
        self.dbclient = dbclient
        self.llm = llm
        self.messages_schema = messages_schema
        self.messages_table = messages_table

    def _remove_bot_id(self, message: str) -> str:
        return re.sub(r"<[^>]*>", "", message)
        
    async def process_message(self, message) -> str:

        message_user = message.author.name
        message_content = self._remove_bot_id(message.content)
        message_ts = message.created_at

        logger.info(f"Message from user: {message_user} passed to LLM")
        response = await self.llm.generate_response(message_user, message_content)
        logger.info(f"Response for user: {message_user} received")

        rows = [(message_user, message_ts, message_content, response)]
        logger.info("Inserting to db ...")
        self.dbclient.insert(
            rows=rows, 
            schema=self.messages_schema, 
            table=self.messages_table
        )

        return response
