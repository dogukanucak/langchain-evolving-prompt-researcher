import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "research-assistant")

# SCOPE settings
SCOPE_DATA_PATH = os.getenv("SCOPE_DATA_PATH", "./scope_data")
ENABLE_SCOPE = os.getenv("ENABLE_SCOPE", "true").lower() == "true"

# Set environment variables for LangSmith
if LANGSMITH_API_KEY:
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
if LANGSMITH_TRACING:
    os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
if LANGSMITH_PROJECT:
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
