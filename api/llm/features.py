import json
from asyncio import create_task, gather, as_completed
from typing import AsyncIterable

from api.llm import extract_features_async_fun
from api.vendor import Product

key_map = {
    "display resolution": "resolution",
    "RAM": "memory",
    "ram": "memory",
    "system memory": "memory",
    "storage capacity": "storage",
    "capacity": "storage",
    "wireless connectivity": "wireless",
    "operating system": "os",
    "operating system compatibility": "os",
    "gpu": "graphics",
    "display size": "screen size",
    "chip": "processor"
}

val_map = {
    "inch": "\"",
    "inches": "\"",
    "hours": "hrs",
    "Ultra HD": "UHD",

    **{f"{i} x {j}": f"{i}x{j}" for i in range(10) for j in range(10)},
    **{f"{i} {chr(ch1)}{chr(ch2)}": f"{i} {chr(ch1)}{chr(ch2)}"
       for i in range(10) for ch1 in range(ord('A'), ord('Z') + 1)
       for ch2 in range(ord('A'), ord('Z') + 1)}
}

val_remove = {
    "array", "options"
}


def cleanup_feature(key: str, val: any) -> tuple[str, any]:
    k, v = key, val
    for old, new in key_map.items():
        if k == old:
            k = new
        else:
            k = k.replace(old, new)

    if isinstance(v, str):
        if v in ("true", "false"):
            v = v == "true"

        elif v == "null" or v.lower() == "n/a" or v in val_remove:
            v = None

        else:
            for old, new in val_map.items():
                if v == old:
                    v = new
                else:
                    v = v.replace(old, new)

    return k, v


# Gets the product features for a single product description
async def get_features_async(description: str) -> dict[str, any]:
    res = await extract_features_async_fun(description)
    feats_json = json.loads(res.result)

    feats = {}
    for k, v in feats_json.items():
        k, v = cleanup_feature(k, v)
        if v is not None:
            feats[k] = v

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
