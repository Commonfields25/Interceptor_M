from datetime import datetime, timezone

from dotenv import load_dotenv


def main():
    load_dotenv(".env.local")

    from src.tinybird.client import tinybird

    now = datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    # Ingest data using the Events API
    tinybird.page_views.ingest(
        {
            "timestamp": now,
            "session_id": "abc123",
            "pathname": "/home",
            "referrer": "https://google.com",
        }
    )

    # Query the endpoint
    result = tinybird.top_pages.query(
        {
            "start_date": "2026-01-01 00:00:00",
            "end_date": now,
            "limit": 5,
        }
    )

    for row in result["data"]:
        print(row["pathname"], row["views"])


if __name__ == "__main__":
    main()
