from functools import cache
from os.path import abspath
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler as fastapi_handle_http_exception
from fastapi.responses import StreamingResponse
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.staticfiles import StaticFiles

from api.llm import fix_product_names_async, collect_features_async
from api.response import LoadStatus, ProductData, LoadError
from api.vendor import Vendor, vendors
from api.website.pug import PugRenderer

# Create FastAPI app and mount static files
app = FastAPI()
app.mount("/static", StaticFiles(directory=abspath("static")), name="static")

# Create template renderer and default context
templates = PugRenderer(abspath("static/templates"))
default_context = {
}


# Decorator for asynchronous template routes
def template(route: str) -> callable:
    def wrapper(func: callable) -> callable:
        @app.get(route, response_class=HTMLResponse)
        async def template_route():
            # Add returned context to a copy of the default context
            res, add = await func()
            ctx = default_context.copy()
            ctx.update(add)

            # Render template and return response
            return templates.response(res, ctx)

        return func

    return wrapper


# Type alias for template responses (template file path, context)
TemplateResponse: type = tuple[str, dict[str, any]]


# 404 page
@cache
@app.exception_handler(404)
# @template("/404")
async def error_404(request: Request, _: Exception):
    return await handle_http_exception(request,
                                       HTTPException(status_code=404, detail="We couldn't find the requested page."))


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
async def compare(query: str, vendor: Vendor = Vendor.BEST_BUY):
    async def gen():
        try:
            # Search for products
            yield LoadStatus("Searching for products...").str()
            products = vendors[vendor].search_products(quote(query), 5)

            yield LoadStatus("Fixing product names...").str()
            await fix_product_names_async(products)

            yield LoadStatus("Extracting features...").str()
            num_sent = 0
            async for index, feat in collect_features_async(products):
                yield LoadStatus("Extracting features... (%d/%d)" % (num_sent + 1, len(products))).str()
                yield ProductData(products[index], feat).str()
                num_sent += 1
        except Exception as e:
            yield LoadError("Internal error: " + str(e))

    headers = {"X-Content-Type-Options": "nosniff"}
    return StreamingResponse(gen(), media_type="text/json", headers=headers)
