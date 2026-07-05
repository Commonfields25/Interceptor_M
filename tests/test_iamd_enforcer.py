import pytest
import os
import tempfile
from scripts.iamd_enforcer import validate_iamd_header

def test_valid_header():
    content = """---
agent: D1
action: Update
timestamp: 2026-07-01T12:00:00Z
related_gate: G2
status: Validated
---
# Content
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        is_valid, error = validate_iamd_header(temp_path)
        assert is_valid is True
        assert error is None
    finally:
        os.remove(temp_path)

def test_missing_header():
    content = "# Just content"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        is_valid, error = validate_iamd_header(temp_path)
        assert is_valid is False
        assert "Missing IAMD YAML header" in error
    finally:
        os.remove(temp_path)

def test_missing_fields():
    content = """---
agent: D1
status: Validated
---
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        is_valid, error = validate_iamd_header(temp_path)
        assert is_valid is False
        assert "Missing required IAMD fields" in error
    finally:
        os.remove(temp_path)
