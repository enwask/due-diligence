from .message import Message
from api.vendor import Product


class ProductData(Message):
    def __init__(self, product: Product, features: dict[str, any]):
        self.product = product
        self.features = features

    def json(self, **kwargs) -> dict[str, any]:
        return {
            "type": "product",
            "id": self.product.vendor.value + ':' + self.product.id,
            "name": self.product.name,
            "price": self.product.price,
            "url": self.product.url,
            "image": self.product.img,
            "features": self.features,
            **kwargs
        }
