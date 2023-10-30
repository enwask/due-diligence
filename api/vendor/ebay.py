from ebaysdk.finding import Connection as Search

from api.vendor.product import Product, ProductBase
from api.vendor.vendor import Vendor

# Set up the eBay API
APP_ID = "NicWashb-DueDilig-PRD-7fc7ec590-ff2c0d48"
api = Search(appid=APP_ID, config_file=None)


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
        kwargs["keywords"] = query

        res = api.execute("findItemsAdvanced", kwargs)
        error = api.error()
        if error:
            print(error.response.dict())
            return []

        items = res.reply.searchResult.item
        products = []
        for item in items:
            try:
                products.append(Product(
                    Vendor.EBAY,
                    item["itemId"],
                    item["title"],
                    "",  # FIXME: Add item description
                    float(item["sellingStatus"]["currentPrice"]["value"]),
                    item["galleryURL"],
                ))
            except KeyError:
                pass
