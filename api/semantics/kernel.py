# Kernel setup and core skills
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.search_engine import GoogleConnector
from semantic_kernel.core_skills.web_search_engine_skill import WebSearchEngineSkill

# Typing
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from typing import Dict, TypeAlias

# Secrets
from api.secrets import openai_key, google_search_key
from api.semantics.skills import load_skill

# Construct the semantic kernel and add OpenAI chat service
kernel = sk.Kernel()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", openai_key))

# Set up the Google Search connector
CUSTOM_SEARCH_ID = "c1f73ff9ebb8a473a"
google_search_connector = GoogleConnector(api_key=google_search_key, search_engine_id=CUSTOM_SEARCH_ID)

# Set up the Google search skill
Skill: TypeAlias = Dict[str, SKFunctionBase]

web_search_skill: Skill = kernel.import_skill(WebSearchEngineSkill(google_search_connector))
comparison_skill: Skill = load_skill(kernel, "Comparison")


# Get the skill functions
compare_products_function: SKFunctionBase = comparison_skill["CompareProducts"]
