from semantic_kernel import Kernel
from semantic_kernel.orchestration.sk_function_base import SKFunctionBase
from typing import Dict
from os.path import abspath


# Helper function to load a skill from disk
def load_skill(kernel: Kernel, path: str) -> Dict[str, SKFunctionBase]:
    return kernel.import_semantic_skill_from_directory(abspath("data/skills"), path)


# Helper function to get a skill function from a skill on disk
def get_skill_function(kernel: Kernel, skill_path: str, function_name: str) -> SKFunctionBase:
    skill = load_skill(kernel, skill_path)
    return skill[function_name]
