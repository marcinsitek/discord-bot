import logging
import os 

# logger
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger("bot-logger")
logger.setLevel(logging.DEBUG)

# LLM
MODEL_NAME = "Qwen/Qwen3-0.6B"

# Database
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = "postgres"
MESSAGES_SCHEMA = "public"
MESSAGES_TABLE = "messages"

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
