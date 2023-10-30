import json
from asyncio import create_task, gather, as_completed
from typing import TypeVar, AsyncIterable

from api.vendor import Product
from api.llm import extract_features_async_fun

# Generic type for dict keys used throughout this file
T = TypeVar("T")

key_map = {
    "display resolution": "resolution",
    "system memory": "memory",
    "RAM": "memory",
    "ram": "memory",
    "storage capacity": "storage",
    "capacity": "storage",
    "wireless connectivity": "wireless",
    "operating system": "os",
    "operating system compatibility": "os",
}

val_map = {
    "inch": "\"",
    "inches": "\"",

    **{f"{i}x{j}": f"{i} x {j}" for i in range(10) for j in range(10)},
    **{f"{i}{ch}": f"{i} {ch}" for i in range(10) for ch in range(ord('a'), ord('z') + 1)},
    **{f"{i}{ch}": f"{i} {ch}" for i in range(10) for ch in range(ord('A'), ord('Z') + 1)}
}


def cleanup_feature(k: str, v: any) -> tuple[str, any]:
    for old, new in key_map.items():
        k.replace(old, new)

    if v is str:
        if v in ("true", "false"):
            v = v == "true"

        elif v == "null":
            v = None

        else:
            for old, new in val_map.items():
                v.replace(old, new)

    return k, v


# Gets the product features for a single product description
async def get_features_async(description: str) -> dict[str, any]:
    res = await extract_features_async_fun(description)
    feats = json.loads(res.result)
    feats = dict([cleanup_feature(k, v) for k, v in feats.items()])

    return feats


# Gets the product features from (key, product description) for use with collect_product_features_async
# The first element of the tuple is the same key passed through the input tuple
async def __get_features_wrapped_async(index: int, description: str) -> tuple[int, dict[str, any]]:
    res = index, await get_features_async(description)
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
async def collect_features_async(products: list[Product]) -> AsyncIterable[tuple[int, dict[str, any]]]:
    # Create a task for each product
    tasks = [create_task(__get_features_wrapped_async(i, products[i].desc)) for i in range(len(products))]

    # Yield features as they are done
    for task in as_completed(tasks):
        res = await task
        yield res
