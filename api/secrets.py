from os import environ as env

# Constants
OPENAI_KEY = env["KEY_OPENAI"]
BEST_BUY_KEY = env["KEY_VENDOR_BEST_BUY"]

__all__ = ["OPENAI_KEY", "BEST_BUY_KEY"]
