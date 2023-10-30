from bestbuyapi import BestBuyAPI

from api.vendor.product import Product, ProductBase
from api.vendor.vendor import Vendor
from api.secrets import BEST_BUY_KEY

api = BestBuyAPI(BEST_BUY_KEY)


class BestBuy(ProductBase):
    # noinspection PyProtocol
    def __init__(self) -> None:
        super().__init__()

    # noinspection PyMethodMayBeStatic
    def get_vendor(self) -> Vendor:
        return Vendor.BEST_BUY

    def get_product(self, product_id: str, **kwargs: any) -> Product:
        return super().get_product(product_id)

    def search_products(self, query: str, num: int = 50, **kwargs: any) -> list[Product]:
        # https://bestbuyapis.github.io/bby-query-builder/#/productSearch
        kwargs.update({
            "sort": "salePrice.dsc",
            "show": "sku,name,longDescription,salePrice,url,thumbnailImage,features.feature",
            "pageSize": num,
            "format": "json"
        })

        products = []
        # noinspection PyBroadException
        try:
            # Construct the search query
            search = "name=" + '&'.join(query.split('+')) + "*"

            # Perform the search
            res = api.products.search(search, **kwargs)

            # Parse the results
            for item in res["products"]:
                # Add features to the product description
                desc = item["longDescription"]
                for feat in item["features"]:
                    desc += f" {feat['feature']}"

                # Add the product to the list
                products.append(Product(
                    Vendor.BEST_BUY,
                    str(item["sku"]),  # SKU is numeric
                    item["name"],
                    desc,
                    item["salePrice"],
                    item["url"],
                    item["thumbnailImage"]
                ))

        # Fail softly and return products we found before the error, if any
        except Exception as e:
            return products

        # Return the products if we were successful
        return products
