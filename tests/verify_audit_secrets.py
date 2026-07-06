import subprocess
import os
from pathlib import Path

def test_audit_secrets_clean():
    """Test that the audit script passes on a clean directory."""
    result = subprocess.run(['python3', 'scripts/audit_secrets.py'], capture_output=True, text=True)
    assert result.returncode == 0
    assert "No hardcoded secrets detected" in result.stdout

def test_audit_secrets_fail():
    """Test that the audit script fails when a secret is present."""
    test_file = Path('scripts/test_secret.py')
    test_file.write_text("api_key = 'ghp_fake_github_token_12345678901234'")
    try:
        result = subprocess.run(['python3', 'scripts/audit_secrets.py'], capture_output=True, text=True)
        assert result.returncode == 1
        assert "SECURITY WARNING" in result.stdout
    finally:
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_audit_secrets_clean()
    test_audit_secrets_fail()
    print("All audit tests passed!")
