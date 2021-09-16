from dotenv import load_dotenv
import os

load_dotenv(".env")

OPENAPI_API_KEY = os.environ.get("OPENAPI_API_KEY")
OPENAPI_BUILD_ID = os.environ.get("OPENAPI_BUILD_ID")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
