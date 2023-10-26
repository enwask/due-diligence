from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

from api.llm.skills import *
from api.secrets import OPENAI_KEY

# Construct the kernel and add AI services
kernel = Kernel()
kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", OPENAI_KEY))

# Set up the product comparison skill
product_comparison: Skill = load_skill(kernel, "ProductComparison")

# Expose the skill functions
extract_features: SkillFunction = get_skill_function(product_comparison, "ExtractFeatures")
extract_features_async: AsyncSkillFunction = get_async_skill_function(product_comparison, "ExtractFeatures")
