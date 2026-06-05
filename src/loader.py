import json
from src.models import Offer


def load_offers_from_json(file_path: str) -> list[Offer]:
    with open(file_path, "r", encoding="utf-8") as file:
        raw_offers = json.load(file)

    return [Offer(**offer) for offer in raw_offers]