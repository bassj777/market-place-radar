import os
import requests
from dotenv import load_dotenv

from src.models import Offer
from src.scoring import classify_score


load_dotenv()

MIN_SCORE_TO_NOTIFY = 60

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def should_notify(offer: Offer) -> bool:
    return offer.score >= MIN_SCORE_TO_NOTIFY


def build_offer_message(offer: Offer) -> str:
    classification = classify_score(offer.score)

    return (
        " 🚨 Nueva oferta detectada 🚨\n\n"
        f"Clasificación: {classification}\n"
        f"Título: {offer.title}\n"
        f"Precio: ${offer.price:,.2f}\n"
        f"Ubicación: {offer.location}\n"
        f"Categoría: {offer.category}\n"
        f"Score: {offer.score}\n"
        f"URL: {offer.url}"
    )


def send_telegram_message(message: str) -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Falta TELEGRAM_BOT_TOKEN en .env")

    if not TELEGRAM_CHAT_ID:
        raise ValueError("Falta TELEGRAM_CHAT_ID en .env")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False,
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()


def notify_offer(offer: Offer) -> None:
    message = build_offer_message(offer)
    send_telegram_message(message)