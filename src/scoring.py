from src.models import Offer


def calculate_score(offer: Offer) -> int:
    score = 0
    title = offer.title.lower()

    if offer.price <= 10000:
        score += 30

    if "iphone" in title:
        score += 25

    if "thinkpad" in title:
        score += 30

    if "toyota" in title or "corolla" in title:
        score += 25

    if offer.category in ["electronics", "computers"]:
        score += 20

    if offer.category == "cars":
        score += 15

    return min(score, 100)


def classify_score(score: int) -> str:
    if score >= 80:
        return "EXCELENTE"
    if score >= 60:
        return "BUENA"
    if score >= 40:
        return "REGULAR"
    return "DESCARTAR"