# 🔐 Credentials & Secret Management

> **IMPORTANT:** NEVER share or commit actual GitHub tokens (ghp_...) or API keys to this repository.

## 1. Handling Sensitive Tokens
The project uses GitHub Secrets for all automated operations. If you have a token (like the one previously shared in chat):

1. **REVOKE IT IMMEDIATELY** if it has been exposed in plain text.
2. **ADD TO SECRETS:**
   - Go to `Settings > Secrets and variables > Actions`.
   - Click `New repository secret`.
   - Name: `GH_PROD_TOKEN` (or similar).
   - Value: Paste your token there.
3. **USE IN WORKFLOWS:**
   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.GH_PROD_TOKEN }}
   ```

## 2. Local Development
Create a `.env` file in your local environment (This file is ignored by Git):
```bash
# .env
GITHUB_TOKEN=your_private_token_here
