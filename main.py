from src.loader import load_offers_from_json
from src.database import create_database, insert_offer, get_all_offers, was_notified, mark_as_notified
from src.scoring import calculate_score, classify_score
from src.notifier import should_notify, notify_offer
from src.collector import collect_offers



def main():
    create_database()

    offers = collect_offers()  

    for offer in offers:
        offer.score = calculate_score(offer)
        insert_offer(offer)

        if should_notify(offer) and not was_notified(str(offer.url)) :
            notify_offer(offer)
            mark_as_notified(str(offer.url))

    stored_offers = get_all_offers()

    print("\n=== OFERTAS EN SQLITE ===\n")

    for offer in stored_offers:
        title, price, location, url, category, score = offer
        classification = classify_score(score)

        print(f"[{classification}] {title}")
        print(f"Precio: ${price}")
        print(f"Ubicación: {location}")
        print(f"Categoría: {category}")
        print(f"Score: {score}")
        print(f"URL: {url}")
        print("-" * 40)


if __name__ == "__main__":
    main()