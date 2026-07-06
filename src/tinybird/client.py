"""Tinybird client configuration for Interceptor_M project.

This module initializes the Tinybird client with resources from tinybird_resources.py.
Environment variables are loaded from .env.local or system environment.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from tinybird_sdk import Tinybird

from src.tinybird.tinybird_resources import sample_events, sample_event_totals

# Load environment variables from .env.local if it exists
_env_path = Path(__file__).parent / ".env.local"
if _env_path.exists():
    load_dotenv(_env_path)


def get_tinybird_client() -> Tinybird:
    """Get or create a Tinybird client instance.
    
    Returns:
        Tinybird: Configured Tinybird client instance.
    """
    return Tinybird(
        {
            "datasources": {"sample_events": sample_events},
            "pipes": {"sample_event_totals": sample_event_totals},
            "base_url": os.getenv("TINYBIRD_API_URL", "https://api.tinybird.co"),
            "token": os.getenv("TINYBIRD_TOKEN"),
        }
    )


# Global client instance
tinybird: Tinybird = get_tinybird_client()

__all__ = ["tinybird", "get_tinybird_client"]
