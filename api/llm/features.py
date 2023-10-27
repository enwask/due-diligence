import json
from asyncio import create_task, gather, as_completed
from typing import TypeVar, AsyncIterable

from api.data import Product
from api.llm import extract_features_async_fun

# Generic type for dict keys used throughout this file
T = TypeVar("T")


# Gets the product features for a single product description
async def get_features_async(description: str) -> dict[str, any]:
    res = await extract_features_async_fun(description)
    return json.loads(res.result)


# Gets the product features from (key, product description) for use with collect_product_features_async
# The first element of the tuple is the same key passed through the input tuple
async def __get_features_wrapped_async(index: int, description: str) -> tuple[int, dict[str, any]]:
    print("Getting features for product", index)
    res = index, await get_features_async(description)
    print("Got features for product", index)
    return res


# Gets product features, returning all at once when all are done
async def gather_features_async(products: list[Product]) -> list[dict[str, any]]:
    # Create a task for each product
    tasks = [create_task(__get_features_wrapped_async(i, products[i].desc)) for i in range(len(products))]

    # Wait for features from all products
    res = await gather(*tasks)

    # Unwrap the results
    return [r[1] for r in res]


# Gets product features, yielding each as it is done
async def collect_features_async(products: list[Product]) -> AsyncIterable[dict[str, any]]:
    # Create a task for each product
    tasks = [create_task(__get_features_wrapped_async(i, products[i].desc)) for i in range(len(products))]

    # Yield features as they are done
    for task in as_completed(tasks):
        res = await task
        yield res[1]
