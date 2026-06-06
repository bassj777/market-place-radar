import sqlite3
from src.models import Offer

DB_NAME = "offers.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            location TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            notified INTEGER DEFAULT 0
        )
    """)

    cursor.execute("PRAGMA table_info(offers)")
    columns = [column[1] for column in cursor.fetchall()]

    if "score" not in columns:
        cursor.execute("ALTER TABLE offers ADD COLUMN score INTEGER DEFAULT 0")

    if "notified" not in columns:
        cursor.execute("ALTER TABLE offers ADD COLUMN notified INTEGER DEFAULT 0")
    
    conn.commit()
    conn.close()


def insert_offer(offer: Offer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO offers (title, price, location, url, category, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            offer.title,
            offer.price,
            offer.location,
            str(offer.url),
            offer.category,
            offer.score
        ))

        print(f"[INFO] Oferta guardada: {offer.title}")

    except sqlite3.IntegrityError:
        cursor.execute("""
            UPDATE offers
            SET price = ?, location = ?, category = ?, score = ?
            WHERE url = ?
        """, (
            offer.price,
            offer.location,
            offer.category,
            offer.score,
            str(offer.url)
        ))

        print(f"[INFO] Oferta duplicada actualizada: {offer.title}")

    conn.commit()
    conn.close()


def get_all_offers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, price, location, url, category, score
        FROM offers
        ORDER BY score DESC
    """)

    offers = cursor.fetchall()

    conn.close()
    return offers

def was_notified(url: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT notified FROM offers
        WHERE url = ?
    """, (url,))

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return False

    return result[0] == 1


def mark_as_notified(url: str) -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE offers
        SET notified = 1
        WHERE url = ?
    """, (url,))

    conn.commit()
    conn.close()