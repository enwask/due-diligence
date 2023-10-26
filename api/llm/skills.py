from logging import Logger
from os.path import abspath
from typing import Optional, TypeAlias, Protocol

from semantic_kernel.connectors.ai import CompleteRequestSettings
from semantic_kernel.kernel import Kernel
from semantic_kernel.memory.semantic_text_memory_base import SemanticTextMemoryBase
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase

# Type for Semantic Kernel skills
Skill: TypeAlias = dict[str, SKFunctionBase]


# Type for individual skill functions' invocation methods
class SkillFunction(Protocol):
    def __call__(self, input: Optional[str] = None,
                 variables: ContextVariables = None,
                 context: Optional["SKContext"] = None,
                 memory: Optional[SemanticTextMemoryBase] = None,
                 settings: Optional[CompleteRequestSettings] = None,
                 log: Optional[Logger] = None) -> SKContext: ...


# Type for individual skill functions' asynchronous invocation methods
class AsyncSkillFunction(Protocol):
    async def __call__(self, input: Optional[str] = None,
                       variables: ContextVariables = None,
                       context: Optional["SKContext"] = None,
                       memory: Optional[SemanticTextMemoryBase] = None,
                       settings: Optional[CompleteRequestSettings] = None,
                       log: Optional[Logger] = None, **kwargs) -> SKContext: ...


# Helper function to load a skill from disk
def load_skill(kernel: Kernel, path: str) -> dict[str, SKFunctionBase]:
    return kernel.import_semantic_skill_from_directory(abspath("data/skills"), path)


# Helper function to get a skill function from a skill
def get_skill_function(skill: Skill, function_name: str) -> SkillFunction:
    return skill[function_name].invoke


# Helper function to get an asynchronous skill function from a skill
def get_async_skill_function(skill: Skill, function_name: str) -> AsyncSkillFunction:
    return skill[function_name].invoke_async
