from asyncio import create_task, gather, as_completed
from typing import AsyncIterable

from api.llm import shorten_name_async_fun
from api.vendor import Product


# Shortens the product name
async def shorten_name_async(name: str) -> str:
    res = await shorten_name_async_fun(name)
    return res.result


# Shortens the product name from (key, product name) for use with fix_product_names_async
async def __shorten_name_wrapped_async(index: int, name: str) -> tuple[int, str]:
    print(f"Shortening name #{index}: {name}")
    res = index, await shorten_name_async(name)
    print(f"Done shortening name #{index}: {name}")
    return res


async def gather_names_async(products: list[Product]) -> None:
    # Create a task for each product
    tasks = [create_task(__shorten_name_wrapped_async(i, products[i].name)) for i in range(len(products))]

    # Wait for features from all products
    res = await gather(*tasks)

    # Update product names
    for index, new_name in res:
        products[index].name = new_name


# Fixes the names of products in the list, yielding each index as it is done
async def collect_names_async(products: list[Product]) -> AsyncIterable[int]:
    # Create a task for each product
    tasks = [create_task(__shorten_name_wrapped_async(i, products[i].name)) for i in range(len(products))]

    # Yield indices as they are done
    for task in as_completed(tasks):
        index, res = await task
        products[index].name = res
        yield index
