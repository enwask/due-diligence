from asyncio import create_task, gather

from api.data import Product
from api.llm import shorten_name_async_fun


# Shortens the product name
async def shorten_name_async(name: str) -> str:
    res = await shorten_name_async_fun(name)
    return res.result


# Shortens the product name from (key, product name) for use with fix_product_names_async
async def __shorten_name_wrapped_async(index: int, name: str) -> tuple[int, str]:
    return index, await shorten_name_async(name)


async def fix_product_names_async(products: list[Product]) -> None:
    # Create a task for each product
    tasks = [create_task(__shorten_name_wrapped_async(i, products[i].name)) for i in range(len(products))]

    # Wait for features from all products
    res = await gather(*tasks)

    # Update product names
    for index, new_name in res:
        products[index].name = new_name
