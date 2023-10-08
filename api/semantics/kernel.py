# Kernel setup and core skills
from logging import Logger

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import CompleteRequestSettings
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Typing
from semantic_kernel.memory.semantic_text_memory_base import SemanticTextMemoryBase
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from typing import Dict, TypeAlias, Callable

# Secrets
from api.secrets import openai_key
from api.semantics.skills import load_skill

# Construct the semantic kernel and add OpenAI chat service
kernel: Kernel = Kernel()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", openai_key))

# Set up the skills we need
Skill: TypeAlias = Dict[str, SKFunctionBase]
__comparison_skill: Skill = load_skill(kernel, "Comparison")

# Get the skill functions we need from the kernel skills
__compare_products_function: SKFunctionBase = __comparison_skill["CompareProducts"]

# Expose the actual functions
compare: Callable[[str | None, ContextVariables | None, SKContext | None, SemanticTextMemoryBase | None,
                   CompleteRequestSettings | None, Logger | None], SKContext] = __compare_products_function.invoke

__all__ = ["kernel", "compare"]
