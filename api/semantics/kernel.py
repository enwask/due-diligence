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
__kernel = sk.Kernel()
__kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", openai_key))

# Set up the Google Search connector
__CUSTOM_SEARCH_ID = "c1f73ff9ebb8a473a"  # Search engine ID; publicly available anyway
__google_search_connector = GoogleConnector(api_key=google_search_key, search_engine_id=__CUSTOM_SEARCH_ID)

# Set up the skills we need
Skill: TypeAlias = Dict[str, SKFunctionBase]

__comparison_skill: Skill = load_skill(__kernel, "Comparison")
__search_skill: Skill = __kernel.import_skill(WebSearchEngineSkill(__google_search_connector), "Search")

# Get the functions we need from the kernel skills
compare_products_function: SKFunctionBase = __comparison_skill["CompareProducts"]
async_search_function: SKFunctionBase = __search_skill["searchAsync"]

__all__ = ["compare_products_function", "async_search_function"]
