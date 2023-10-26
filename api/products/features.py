import json
from asyncio import create_task, gather
from typing import Any, TypeVar

from api.llm import extract_features_async

# Generic type for dict keys used throughout this file
T = TypeVar("T")


# Gets the product features for a single product description
async def get_features_async(description: str) -> dict[str, Any]:
    res = await extract_features_async(description)
    return json.loads(res.result)


# Gets the product features from (key, product description) for use with collect_product_features_async
# The first element of the tuple is the same key passed through the input tuple
async def __get_features_pair_async(product: tuple[str, str]) -> tuple[str, dict[str, Any]]:
    return product[0], await get_features_async(product[1])


# Gets the product features for a dictionary of product descriptions
async def collect_features_async(descriptions: dict[T, str]) -> dict[T, dict[str, Any]]:
    # Create a task for each product
    tasks = [create_task(__get_features_pair_async((k, v))) for k, v in descriptions.items()]

    # Wait for features from all products
    res = await gather(*tasks)
    return dict(res)
