import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

from api import secrets
from api.skills import load_skill

# Fetch the OpenAI key from Google Secret Manager
openai_key = str(secrets.get_secret_openai())

# Construct the semantic kernel and add OpenAI chat service
kernel = sk.Kernel()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", openai_key))
