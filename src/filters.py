from src.models import Offer


def filter_by_max_price(offers: list[Offer], max_price: float) -> list[Offer]:
    return [offer for offer in offers if offer.price <= max_price]