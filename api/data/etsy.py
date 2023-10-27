from api.data.product import Product, ProductBase
from api.data.vendor import Vendor


class Etsy(ProductBase):
    # noinspection PyProtocol
    def __init__(self) -> None:
        super().__init__()

    # noinspection PyMethodMayBeStatic
    def get_vendor(self) -> Vendor:
        return Vendor.ETSY

    def get_product(self, product_id: str, **kwargs: any) -> Product:
        return super().get_product(product_id)

    def search_products(self, query: str, num: int = 50, **kwargs: any) -> list[Product]:
        return super().search_products(**kwargs)
