from typing import Optional, Protocol

from api.data.vendor import Vendor


class Product:
    def __init__(self, id_: str, name: str, desc: str, price: float, url: str, img: Optional[str] = None) -> None:
        self.id: str = id_
        self.name: str = name
        self.desc: str = desc
        self.price: float = price
        self.url: str = url
        self.img: Optional[str] = img


# Abstract product database for data access layer
class ProductBase(Protocol):
    def __init__(self) -> None: ...

    # Gets the vendor associated with this product database
    def get_vendor_str(self) -> Vendor: ...

    # Gets a product by its id
    def get_product(self, product_id: str, **kwargs: any) -> Product: ...

    # Searches for products by a query (assumes the query has been escaped already)
    # Fails softly: returns an empty list if the search fails
    def search_products(self, query: str, num: int = 50, **kwargs: any) -> list[Product]: ...
