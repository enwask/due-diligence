import json
from functools import cache
from os.path import abspath
from urllib.parse import quote

from aiostream.stream import merge as merge_streams
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler as fastapi_handle_http_exception
from fastapi.responses import StreamingResponse
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.staticfiles import StaticFiles

from api.llm import collect_names_async, collect_features_async
from api.response import LoadStatus, ProductData, LoadError, json_stream
from api.vendor import Vendor, vendors, vendor_info
from api.website.pug import PugRenderer

# Create FastAPI app and mount static files
app = FastAPI()
app.mount("/static", StaticFiles(directory=abspath("static")), name="static")

# Create template renderer and default context
templates = PugRenderer(abspath("static/pug"))
default_context = {}


# Decorator for asynchronous template routes
def template(route: str) -> callable:
    def wrapper(fun: callable) -> callable:
        @app.get(route, response_class=HTMLResponse)
        async def template_route():
            # Add returned context to a copy of the default context
            res, add = await fun()
            ctx = default_context.copy()
            ctx.update(add)

            # Render template and return response
            return templates.response(res, ctx)

        return fun

    return wrapper


# Type alias for template responses (template file path, context)
TemplateResponse: type = tuple[str, dict[str, any]]


# 404 page
@cache
@app.exception_handler(404)
async def error_404(request: Request, _: Exception):
    return await handle_http_exception(request,
                                       HTTPException(status_code=404, detail="We couldn't find the requested page."))


# HTTP exception handler
@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exception: HTTPException) -> Response:
    accepts = request.headers.get("accept", "")
    if "text/html" in accepts:
        return HTMLResponse(templates.render("error.pug", {
            "status_code": exception.status_code,
            "detail": exception.detail
        }))
    else:
        return await fastapi_handle_http_exception(request, exception)


# Product comparison endpoint
@app.get("/compare/{query}")
async def compare(query: str, vendor: Vendor = Vendor.BEST_BUY, num: int = 10):
    num = min(20, max(1, num))

    @json_stream
    async def fun():
        try:
            # Search for products
            yield LoadStatus("Searching products...").json()
            products = vendors[vendor].search_products(quote(query), num)

            # Get product features and fix names
            # TODO: Move this to another module
            yield LoadStatus("Extracting features...").json()
            name_fixed: list[bool] = [False for _ in products]
            features: list[None | dict[str, any]] = [None for _ in products]

            # Operate on each result as it comes in
            streamer = merge_streams(collect_names_async(products), collect_features_async(products))
            num_sent = 0
            async with streamer.stream() as stream:
                async for res in stream:
                    index, val = res
                    if isinstance(val, str):
                        # Product name fixed
                        products[index].name = val
                        name_fixed[index] = True

                        # If features are not ready, skip this iteration
                        if features[index] is None:
                            continue
                    else:
                        # Product features extracted
                        features[index] = val

                        # If name is not ready, skip this iteration
                        if not name_fixed[index]:
                            continue

                    # Send product data
                    yield [
                        LoadStatus("Extracting features... (%d/%d)" % (num_sent + 1, len(products))).json(),
                        ProductData(products[index], features[index]).json()]
                    num_sent += 1

        # Handle error in feature loading
        except Exception as e:
            yield LoadError("Internal error: " + str(e)).json()

    # Return the generator function as a streaming response
    # TODO: this should also be a decorator for cleaner route functions
    headers = {"X-Content-Type-Options": "nosniff"}
    return StreamingResponse(fun(), media_type="application/json", headers=headers)


# Product comparison endpoint
@app.get("/tune/{query}")
async def tune(query: str, vendor: Vendor = Vendor.BEST_BUY, num: int = 10):
    async def fun():
        try:
            # Search for products
            yield "<p>Searching for products...</p>"
            products = vendors[vendor].search_products(quote(query), num)

            # Fix product names FIXME: Use the thing below with stream merge
            # yield "<p>Fixing product names...</p>"
            # await gather_names_async(products)

            # Get product features
            yield "<p>Extracting features...</p>"
            name_fixed = [False for _ in products]
            features: list[None | dict[str, any]] = [None for _ in products]

            # Operate on each result as it comes in
            streamer = merge_streams(collect_names_async(products), collect_features_async(products))
            num_sent = 0
            async with streamer.stream() as stream:
                async for res in stream:
                    index: int = -1
                    feat: dict[str, any]

                    if isinstance(res, int):
                        # Product name fixed
                        name_fixed[res] = True
                        # products[]

                        # If features are not ready, end iteration
                        if features[res] is None:
                            continue
                    else:
                        # Product features extracted
                        index, feat = res
                        features[index] = feat

                        # If name is not ready, end iteration
                        if not name_fixed[index]:
                            continue

                    # Send response chunk
                    br = '\n'  # No backslashes in f-string
                    yield f"<h2>{products[index].name}</h2>"
                    yield f"<textarea style='width:60%;height:300px;'>{products[index].desc.replace(br, ' ')}</textarea><br/><br/>"
                    yield f"<textarea style='width:60%;height:300px;' id='i{num_sent}'>{json.dumps(ProductData(products[index], feat).json()['features'], indent=2)}</textarea><br/><br/>"
                    yield f"<button id='b{num_sent}' style='padding:10px 5px;'>Remove linebreaks</button><br/><br/><br/>"
                    yield f"<script>let el{num_sent}=document.querySelector('#b{num_sent}');el{num_sent}.onclick=()=>{{i{num_sent}.value=i{num_sent}.value.replaceAll('\\n',' ').replaceAll('   ',' ');}};</script>"

                    num_sent += 1

        # Handle error in feature loading
        except Exception as e:
            yield LoadError("Internal error: " + str(e)).json()

    # Return the generator function as a streaming response
    headers = {"X-Content-Type-Options": "nosniff"}
    return StreamingResponse(fun(), media_type="text/html", headers=headers)


# Home page / product comparison frontend
@cache
@template("/")
async def search() -> TemplateResponse:
    return "search.pug", {
        "title": "Search",
        "default_vendor": "best_buy",
        "vendors": [
            {
                "id": vendor.value,
                "name": vendor_info[vendor][0],
                "enabled": vendor_info[vendor][1],
                "badge": vendor_info[vendor][2] or ""
            } for vendor in Vendor
        ]
    }
