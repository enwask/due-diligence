from typing import Optional, Any

import requests

# Base URL for the GimmeProxy API.
base_url = "https://gimmeproxy.com/api/getProxy"


def get_proxy(**kwargs) -> Optional[str]:
    """Gets a proxy from the GimmeProxy API as a string in the form ip:port."""

    # Returns a proxy in the form of a string
    kwargs["ipPort"] = True
    kwargs["get"] = True
    kwargs["post"] = True
    kwargs["maxCheckPeriod"] = 600
    request = requests.get(base_url, params=kwargs)

    # If the request was not successful, return None
    if request.status_code != 200:
        return None

    return request.text


def get_proxy_https(**kwargs) -> Optional[str]:
    """Gets a proxy from the GimmeProxy API as a string in the form ip:port. Filters for
    proxies supporting get, post, and https requests, that have been checked within the last hour."""

    return get_proxy(supportsHttps=True, **kwargs)
