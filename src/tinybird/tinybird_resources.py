"""Tinybird resources definition for Interceptor_M project.

This module defines datasources and endpoints for analytics tracking.
"""

from tinybird_sdk import define_datasource, define_endpoint, engine, node, p, t

# --- Datasources ---

app_token = ""  # Set via environment variable TINYBIRD_TOKEN

sample_events = define_datasource(
    "sample_events",
    {
        "description": "Application events for analytics tracking",
        "schema": {
            "event_id": t.string(),
            "event_type": t.string(),
            "event_name": t.string(),
            "timestamp": t.date_time(),
            "user_id": t.string().nullable(),
            "session_id": t.string(),
            "page_url": t.string().nullable(),
            "country": t.string().low_cardinality().nullable(),
            "device": t.string().low_cardinality().nullable(),
            "properties": t.json().nullable(),
        },
        "engine": engine.merge_tree(
            {
                "sorting_key": ["event_type", "timestamp"],
                "partition_key": ["toYYYYMM(timestamp)"],
            }
        ),
    },
)


# --- Endpoints ---

sample_event_totals = define_endpoint(
    "sample_event_totals",
    {
        "description": "Aggregate event counts by type and time period",
        "params": {
            "start_date": p.date_time(),
            "end_date": p.date_time(),
            "event_type": p.string().optional(),
            "limit": p.int32().optional(100),
        },
        "nodes": [
            node(
                {
                    "name": "filtered_events",
                    "sql": """
                SELECT 
                    event_type,
                    event_name,
                    count() AS total_events,
                    countIf(user_id IS NOT NULL) AS unique_users,
                    min(timestamp) AS first_event,
                    max(timestamp) AS last_event
                FROM sample_events
                WHERE timestamp >= {{DateTime(start_date)}}
                  AND timestamp <= {{DateTime(end_date)}}
                  {% if defined(event_type) %}
                  AND event_type = {{String(event_type)}}
                  {% endif %}
                GROUP BY event_type, event_name
                ORDER BY total_events DESC
                LIMIT {{Int32(limit, 100)}}
            """,
                }
            ),
        ],
        "output": {
            "event_type": t.string(),
            "event_name": t.string(),
            "total_events": t.uint64(),
            "unique_users": t.uint64(),
            "first_event": t.date_time(),
            "last_event": t.date_time(),
        },
    },
)
