from .best_buy import BestBuy
from .ebay import Ebay
from .etsy import Etsy
from .product import Product, ProductBase
from .vendor import *

best_buy = BestBuy()
ebay = Ebay()
etsy = Etsy()

vendors = {
    Vendor.BEST_BUY: best_buy,
    Vendor.EBAY: ebay,
    Vendor.ETSY: etsy
}
