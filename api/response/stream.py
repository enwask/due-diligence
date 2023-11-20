import json


# Wraps the response generator function to stringify yields from dicts and lists
def json_stream(fun: callable) -> callable:
    async def wrapper(*args, **kwargs):
        # Get next value from response
        gen = fun(*args, **kwargs)
        async for val in gen:
            yield val if isinstance(val, str) else json.dumps(val)

    return wrapper
