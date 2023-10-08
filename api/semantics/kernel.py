# Kernel setup and core skills
from logging import Logger

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import CompleteRequestSettings
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.search_engine import GoogleConnector
from semantic_kernel.core_skills.web_search_engine_skill import WebSearchEngineSkill

# Typing
from semantic_kernel.memory.semantic_text_memory_base import SemanticTextMemoryBase
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from typing import Dict, TypeAlias, Callable

# Secrets
from api.secrets import openai_key, google_search_key
from api.semantics.skills import load_skill

# Construct the semantic kernel and add OpenAI chat service
__kernel = Kernel()
__kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", openai_key))

# Set up the Google Search connector
__CUSTOM_SEARCH_ID: str = "c1f73ff9ebb8a473a"  # Search engine ID; publicly available anyway
__google_search_connector = GoogleConnector(api_key=google_search_key, search_engine_id=__CUSTOM_SEARCH_ID)

# Set up the skills we need
Skill: TypeAlias = Dict[str, SKFunctionBase]

__comparison_skill: Skill = load_skill(__kernel, "Comparison")
__search_skill: Skill = __kernel.import_skill(WebSearchEngineSkill(__google_search_connector), "Search")

# Get the skill functions we need from the kernel skills
__compare_products_function: SKFunctionBase = __comparison_skill["CompareProducts"]
__async_search_function: SKFunctionBase = __search_skill["searchAsync"]

# Expose the actual functions
compare: Callable[[str | None, ContextVariables | None, SKContext | None, SemanticTextMemoryBase | None,
                   CompleteRequestSettings | None, Logger | None], SKContext] = __compare_products_function.invoke

search: Callable[[str | None, ContextVariables | None, SKContext | None, SemanticTextMemoryBase | None,
                  CompleteRequestSettings | None, Logger | None], SKContext] = __async_search_function.invoke

__all__ = ["compare", "search"]
