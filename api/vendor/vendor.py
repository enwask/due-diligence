from enum import Enum


class Vendor(Enum):
    # AMAZON = "amazon"
    BEST_BUY = "best_buy"
    EBAY = "ebay"
    ETSY = "etsy"
    GOOGLE_SHOPPING = "google_shopping"
    WALMART = "walmart"

    def __str__(self) -> str:
        return self.value


vendor_info: dict[Vendor, str | tuple[str, bool, str | None]] = {
    # Vendor.AMAZON: ("Amazon", False, "Coming soon"),
    Vendor.BEST_BUY: ("Best Buy", True, None),
    Vendor.EBAY: ("eBay", True, None),
    Vendor.ETSY: ("Etsy", True, None),
    Vendor.GOOGLE_SHOPPING: ("Google Shopping", False, "Legacy"),
    Vendor.WALMART: ("Walmart", False, "Coming soon")
}