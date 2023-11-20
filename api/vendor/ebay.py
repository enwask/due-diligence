from ebaysdk.finding import Connection as Search
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.response import ResponseDataObject

from api.vendor.product import Product, ProductBase
from api.vendor.vendor import Vendor

# Set up the eBay API
APP_ID = "NicWashb-DueDilig-PRD-7fc7ec590-ff2c0d48"
search_api = Search(appid=APP_ID, config_file=None)


class Ebay(ProductBase):
    # noinspection PyProtocol
    def __init__(self) -> None:
        super().__init__()

    # noinspection PyMethodMayBeStatic
    def get_vendor(self) -> Vendor:
        return Vendor.EBAY

    def get_product(self, product_id: str, **kwargs: any) -> Product:
        return super().get_product(product_id)

    def search_products(self, query: str, num: int = 50, **kwargs: any) -> list[Product]:
        kwargs.update({
            "keywords": query,
            # "outputSelector": "AspectHistogram"
        })

        res = search_api.execute("findItemsAdvanced", kwargs)
        error = search_api.error()
        if error:
            print(error.response.dict())
            return []

        items: list[ResponseDataObject] = res.reply.searchResult.item
        products: list[Product] = []

        for item in items:
            # data = search_api.execute("GetSingleItem", {"ItemID": item.get("itemId")})
            # print(item.get("itemId"))
            # print(data.reply.item)
            try:
                products.append(Product(
                    Vendor.EBAY,
                    item.get("itemId"),
                    item.get("title"),
                    "",
                    float(item.get("sellingStatus").get("currentPrice").get("value")),
                    item.get("galleryURL"),
                ))
            except KeyError:
                pass

        return products
