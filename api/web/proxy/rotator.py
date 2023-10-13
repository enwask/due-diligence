import logging as log

from .proxy import get_proxy_https
import requests
from fake_useragent import UserAgent

class ProxyRotator:
    """
    A class that rotates proxies from the GimmeProxy API. Provides a method to make a request with the current proxy.
    Also randomizes user agent per request if enabled (which it is by default).

    Args:
        threshold: The number of requests that can be sent before rotating proxies
        **kwargs: Keyword arguments to pass to the GimmeProxy API when requesting a new proxy
    """

    def __init__(self, threshold: int = 10, randomize_user_agent=True, **kwargs) -> None:
        self.args = kwargs
        self.threshold = threshold
        self.count = 0
        self.proxy = ""
        self.proxies = {}
        self.user_agent: UserAgent = None

        if randomize_user_agent:
            self.user_agent = UserAgent()

        # Get the first proxy
        self.rotate()

    def rotate(self) -> None:
        """Rotates the active proxy."""

        log.info("Rotating proxy...")
        self.proxy = get_proxy_https(**self.args)
        log.debug("GimmeProxy returned proxy: %s", self.proxy)
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy
        }

    def request(self, url: str, method: str = "get", **kwargs) -> requests.Response:
        """
        Makes a request with the current proxy.

        Args:
            method: The HTTP method to use
            url: The URL to request
            **kwargs: Keyword arguments to pass to requests.request

        Returns:
            The response from the request
        """

        # If the proxy has been used more than the threshold, rotate it
        if self.count >= self.threshold:
            self.rotate()
            self.count = 0
        self.count += 1

        # Add user agent to headers if enabled (and if not already present)
        if self.user_agent is not None:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            if "User-Agent" not in kwargs["headers"]:
                kwargs["headers"]["User-Agent"] = self.user_agent.random

        # Make the request
        response = requests.request(method, url, proxies=self.proxies, **kwargs)
        return response
