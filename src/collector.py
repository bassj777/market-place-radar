from playwright.sync_api import sync_playwright
from src.models import Offer


USER_DATA_DIR = "data/playwright_profile"
MARKETPLACE_URL = "https://www.facebook.com/marketplace"


def collect_offers() -> list[Offer]:
    offers: list[Offer] = []

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=[
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ],
        )

        page = context.new_page()

        page.goto(
            MARKETPLACE_URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        page.wait_for_timeout(8000)

        cards = page.locator("a[href*='/marketplace/item/']").all()

        print(f"[INFO] Cards encontrados: {len(cards)}")

        for card in cards:
            try:
                offer = parse_card(card)

                if offer:
                    offers.append(offer)

            except Exception as error:
                print(f"[WARN] No se pudo procesar una card: {error}")

        context.close()

    return offers


def parse_card(card) -> Offer | None:
    text = card.inner_text()
    url = card.get_attribute("href")

    if not text or not url:
        return None

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if len(lines) < 3:
        return None

    price_text = lines[0]
    title = lines[1]
    location = lines[2]

    price = parse_price(price_text)

    if price is None:
        return None

    if url.startswith("/"):
        url = f"https://www.facebook.com{url}"

    return Offer(
        title=title,
        price=price,
        location=location,
        url=url,
        category="vehicles",
    )


def parse_price(price_text: str) -> float | None:
    clean_text = (
        price_text
        .replace("$", "")
        .replace(",", "")
        .replace("MXN", "")
        .replace("Gratis", "0")
        .replace(" ", "")
        .strip()
    )

    try:
        return float(clean_text)
    except ValueError:
        return None