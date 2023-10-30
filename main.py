from functools import cache
from os.path import abspath
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from starlette.responses import HTMLResponse

from api.llm import fix_product_names_async, collect_features_async
from api.response import LoadStatus, ProductData, LoadError
from api.vendor import Vendor, vendors
from api.website.pug import PugRenderer

# Create FastAPI app and template renderer
app = FastAPI()
templates = PugRenderer(abspath("static/templates"))


# Decorator for asynchronous template routes
def template(route: str) -> callable:
    def wrapper(func: callable) -> callable:
        @app.get(route, response_class=HTMLResponse)
        async def template_route():
            return templates.response(*await func())

        return func

    return wrapper


# Type alias for template responses (template file path, context)
TemplateResponse: type = tuple[str, dict[str, any]]


# 404 page
@cache
@app.exception_handler(404)
# @template("/404")
async def error_404(request: any, _: Exception):
    return await http_exception(request, HTTPException(status_code=404, detail="We couldn't find the requested page."))


@app.exception_handler(HTTPException)
async def http_exception(_: any, exception: HTTPException) -> HTMLResponse:
    return HTMLResponse(templates.render("error.pug", {
        "status_code": exception.status_code,
        "detail": exception.detail
    }))


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
