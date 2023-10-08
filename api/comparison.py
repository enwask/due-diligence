from api.products.google_shopping import search_products, get_description
from api.semantics.kernel import compare

# Typing
from semantic_kernel.orchestration.sk_context import SKContext
from typing import List, Any


# Search for products with the given query and return an object for comparison and display
def fetch_products(query: str, num: int = 5, max_desc_len: int = 200) -> List[Any]:
    print("Parsing search results...")

    # Get search results
    search_results = search_products(query, num=num)
    res: List[Any] = [None] * len(search_results)

    # Recursively add the data we want for each product
    for i in range(len(search_results)):
        print(f"\nFetching data for product {i + 1}/{len(search_results)}")
        print(f"Product name: {search_results[i]['title']}")

        product = search_results[i]
        title_split = product["title"].replace(" - ", " ").split(' ')
        res[i] = {
            "title": ' '.join(title_split[:6]) + ("..." if len(title_split) > 6 else ""),  # str
            "price": product["price"],  # float
            "url": product["url"],  # str
            "thumbnail": product["thumbnail"],  # str
            "description": get_description(product["product_id"], max_desc_len)  # str
        }

    return res


# Compare the given products and return an SKContext from the kernel
def compare_products(products: List[Any]) -> SKContext:
    print("Building prompt...")

    # Build the prompt input from product info
    prompt = "\n\n".join([
        f"{product['title']}\nDescription: {product['description']}"
        for product in products])

    print("\nFull prompt:\n")
    print(prompt)

    print("\nThinking...")

    # Send the prompt to the kernel and return the result
    return compare(prompt)

