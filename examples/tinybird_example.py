"""Example usage of Tinybird Forward integration.

This script demonstrates how to:
1. Ingest events into the sample_events datasource
2. Query the sample_event_totals endpoint
3. Display results
"""

import json
from datetime import datetime, timedelta
from typing import Any

# Import the Tinybird client
from src.tinybird.client import tinybird


def ingest_sample_events():
    """Ingest sample events into Tinybird."""
    # Sample events data
    events = [
        {
            "event_id": "evt_001",
            "event_type": "page_view",
            "event_name": "homepage_viewed",
            "timestamp": datetime.now().isoformat(),
            "user_id": "user_123",
            "session_id": "sess_abc",
            "page_url": "https://example.com/",
            "country": "FR",
            "device": "desktop",
            "properties": json.dumps({"browser": "Chrome", "os": "Windows"}),
        },
        {
            "event_id": "evt_002",
            "event_type": "click",
            "event_name": "button_clicked",
            "timestamp": datetime.now().isoformat(),
            "user_id": "user_123",
            "session_id": "sess_abc",
            "page_url": "https://example.com/pricing",
            "country": "FR",
            "device": "desktop",
            "properties": json.dumps({"button_id": "cta-primary"}),
        },
        {
            "event_id": "evt_003",
            "event_type": "page_view",
            "event_name": "pricing_viewed",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "user_id": "user_456",
            "session_id": "sess_def",
            "page_url": "https://example.com/pricing",
            "country": "US",
            "device": "mobile",
            "properties": json.dumps({"browser": "Safari", "os": "iOS"}),
        },
    ]

    # Ingest events using the datasource reference
    try:
        result = tinybird.datasources["sample_events"].ingest(events)
        print(f"✅ Ingested {len(events)} events successfully")
        return result
    except Exception as e:
        print(f"❌ Error ingesting events: {e}")
        raise


def query_event_totals(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    event_type: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Query the event totals endpoint.

    Args:
        start_date: Start of the time range (default: 30 days ago)
        end_date: End of the time range (default: now)
        event_type: Optional filter by event type
        limit: Maximum number of results (default: 100)

    Returns:
        List of event aggregation results.
    """
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=30)

    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "limit": limit,
    }
    if event_type:
        params["event_type"] = event_type

    try:
        response = tinybird.pipes["sample_event_totals"].query(params)
        print("✅ Query executed successfully")
        return response["data"]
    except Exception as e:
        print(f"❌ Error querying: {e}")
        raise


def display_results(results: list[dict[str, Any]]):
    """Display query results in a formatted way."""
    if not results:
        print("No results to display.")
        return

    print("\n" + "=" * 80)
    print("EVENT TOTALS RESULTS")
    print("=" * 80)

    for i, row in enumerate(results, 1):
        print(f"\n{i}. {row.get('event_name', 'N/A')}")
        print(f"   Type: {row.get('event_type', 'N/A')}")
        print(f"   Total Events: {row.get('total_events', 0):,}")
        print(f"   Unique Users: {row.get('unique_users', 0):,}")
        print(
            f"   Period: {row.get('first_event', 'N/A')} → {row.get('last_event', 'N/A')}"
        )


def main():
    """Main function demonstrating Tinybird usage."""
    print("🚀 Tinybird Forward Integration Example")
    print("-" * 40)

    # Step 1: Ingest events
    print("\n📤 Step 1: Ingesting sample events...")
    ingest_sample_events()

    # Step 2: Query aggregated results
    print("\n📥 Step 2: Querying event totals...")
    results = query_event_totals(
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now(),
    )

    # Step 3: Display results
    print("\n📊 Step 3: Displaying results...")
    display_results(results)

    print("\n" + "=" * 80)
    print("✅ Example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
