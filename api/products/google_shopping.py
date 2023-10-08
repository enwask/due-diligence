import requests
from urllib import parse
from typing import Any, List

from api.secrets import oxylabs_user, oxylabs_key

__ENDPOINT = "https://realtime.oxylabs.io/v1/queries"
__auth = (oxylabs_user, oxylabs_key)


# Get raw JSON results from Oxylabs API
def __search(query: str, min_price: int = None, max_price: int = None) -> Any:
    payload = {
        "source": "google_shopping_search",
        "query": parse.quote(query),
        "parse": "true"
    }

    # Add price constraints if present
    if min_price is not None or max_price is not None:
        payload["context"] = []

        if min_price is not None:
            payload["context"].append({"key": "min_price", "value": min_price})
        if max_price is not None:
            payload["context"].append({"key": "max_price", "value": max_price})

    # Send the request
    response = requests.post(__ENDPOINT, auth=__auth, json=payload)
    return response.json()


# Fix the URL of a product object, which is sometimes malformed in the Oxylabs API response
def __fix_url(url: str) -> str:
    # Remove the "url?url=" prefix if present
    res = url[8:] if url.startswith("/url?url=") else url

    # Add the domain prefix if missing (for links to Google Shopping pages)
    if res.startswith("/shopping/product/"):
        res = "https://www.google.com" + res

    # Remove any query parameters
    return res.split('?')[0]


# Fix a product's malformed URL and return it, or return None if not a Google Shopping listing
def __fix_product(product: Any) -> Any:
    product["url"] = __fix_url(product["url"])
    return product if product["url"].startswith("https://www.google.com/shopping/product/") else None


# Get a list of product objects from Oxylabs API, optionally filtered by price and/or limited by # of results
def search_products(query: str, min_price: int = None, max_price: int = None, num: int = 0) -> List[Any]:
    results = __search(query, min_price, max_price)

    # Extract product array from first (presumably only) page of results; filter for Google Shopping pages
    res = list(filter(lambda p: p is not None,
                      map(__fix_product,
                          results["results"][0]["content"]["results"]["organic"])))

    # Limit results if requested
    return res[:min(num, len(res))] if num > 0 else res


# Scrapes a Google Shopping product page for more detailed information
def __get_product_info(product_id: str) -> Any:
    payload = {
        "source": "google_shopping_product",
        "query": parse.quote(product_id),
        "parse": "true"
    }

    # Send the request
    response = requests.post(__ENDPOINT, auth=__auth, json=payload)
    return response.json()


# Retrieves the top review for a given product ID, truncated to the max length (in characters) if specified
# If no reviews are found, returns None
def get_top_review(product_id: str, max_len: int = 0) -> str | None:
    results = __get_product_info(product_id)

    # Extract top review if present
    try:
        res = results["results"][0]["content"]["reviews"]["top_review"]["text"]
    except KeyError:
        return None

    # Clean up review string and return
    if res.endswith(" Less"):
        res = res[:-5]

    # Truncate if requested
    return res[:min(max_len, len(res))] if max_len > 0 else res


# Gets a product's long-form description from its Google Shopping page
def get_description(product_id: str, num_chars: int = 0) -> str:
    results = __get_product_info(product_id)

    # Extract description if present
    res = results["results"][0]["content"]["description"]

    # Clean up description string and return
    res = (res[:-5] if res.endswith(" Less") else res).replace("%20", ' ')

    # Truncate if requested
    return res[:min(num_chars, len(res))] if num_chars > 0 else res


# TODO: Everything here should probably be asynchronous
__all__ = ["search_products", "get_top_review", "get_description"]