# Git Authentication Helper Guide

This guide explains how to set up and use the Git Authentication Helper system for the **Interceptor_M** project.

---

## 📁 File Structure

The authentication system is stored in the `.github/auth/` directory:

```
.github/auth/
├── .git_credentials_config.json.example  # Template for credentials
├── .gitignore_additions.txt              # Rules to exclude sensitive files
├── git_auth_helper.py                    # Python script for Git operations
└── GIT_AUTH_GUIDE.md                     # This guide
```

---

## 🔐 Setup Instructions

### 1. Configure Your GitHub Token

1. **Generate a GitHub Token**:
   - Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens).
   - Click **Generate new token** (classic).
   - Give it a descriptive name (e.g., `Interceptor_M`).
   - Select the following scopes:
     - `repo` (full control of private repositories)
     - `admin:repo_hook` (if you need webhooks)
   - Click **Generate token** and copy the token.

2. **Store the Token Securely**:
   - **Option 1 (Recommended)**: Use environment variables:
     ```bash
     export GITHUB_TOKEN="your_github_token"
     export GITHUB_USERNAME="Commonfields25"
     export GIT_USER_NAME="Your Name"
     export GIT_USER_EMAIL="your.email@example.com"
     ```
     Add these lines to your `~/.bashrc` or `~/.zshrc` to persist them.

   - **Option 2**: Use the config file:
     - Copy `.git_credentials_config.json.example` to `.git_credentials_config.json`.
     - Fill in the placeholders with your actual credentials:
       ```json
       {
         "github": {
           "token": "your_github_token",
           "username": "Commonfields25",
           "user_name": "Your Name",
           "user_email": "your.email@example.com",
           "default_branch": "main"
         }
       }
       ```
     - **⚠️ Important**: Never commit `.git_credentials_config.json` to Git. It is already excluded via `.gitignore_additions.txt`.

---

## 🛠️ Using the Git Authentication Helper

The `git_auth_helper.py` script automates common Git operations. Here is how to use it:

### 1. Test Your Configuration

Run the following command to verify your setup:

```bash
python .github/auth/git_auth_helper.py test-config
```

If successful, you will see:
```
✅ Configuration is valid.
```

### 2. Clone a Repository

To clone the **Interceptor_M** repository:

```bash
python .github/auth/git_auth_helper.py clone-repo https://github.com/Commonfields25/Interceptor_M.git
```

To clone into a specific directory:

```bash
python .github/auth/git_auth_helper.py clone-repo https://github.com/Commonfields25/Interceptor_M.git --target my_project
```

### 3. Create a Pull Request

To create a PR from your current branch to `main`:

```bash
python .github/auth/git_auth_helper.py create-pr \
  --title "Fix encoding and params" \
  --body "This PR fixes encoding issues and parameter handling." \
  --base main \
  --head fix-encoding-params
```

---

## 📌 Best Practices

1. **Never Commit Sensitive Files**:
   - Ensure `.git_credentials_config.json` and `.env` are **never** committed to Git.
   - The `.gitignore_additions.txt` file already excludes these files.

2. **Use Environment Variables for Security**:
   - Prefer environment variables over config files for sensitive data.

3. **Keep Your Token Secure**:
   - Treat your GitHub token like a password. Never share it or hardcode it in scripts.

4. **Rotate Tokens Regularly**:
   - Regenerate your GitHub token periodically for security.

---

## 🚀 Example Workflow

Here is how you might use this system in a typical workflow:

1. **Clone the Repository**:
   ```bash
   python .github/auth/git_auth_helper.py clone-repo https://github.com/Commonfields25/Interceptor_M.git
   cd Interceptor_M
   ```

2. **Create a New Branch**:
   ```bash
   git checkout -b feature/new-model
   ```

3. **Make Your Changes**:
   - Edit files, add features, etc.

4. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat: add new model"
   git push -u origin feature/new-model
   ```

5. **Create a Pull Request**:
   ```bash
   python .github/auth/git_auth_helper.py create-pr \
     --title "feat: add new model" \
     --body "This PR adds a new model to the project." \
     --base main \
     --head feature/new-model
   ```

---

## 🔍 Troubleshooting

### Error: Missing Required Configuration Keys

If you see:
```
Error: Missing required configuration keys: token, username
```

**Solution**: Ensure your environment variables or config file are correctly set up. Run:

```bash
python .github/auth/git_auth_helper.py test-config
```

### Error: Failed to Create PR

If the PR creation fails:
- Verify your GitHub token has the `repo` scope.
- Ensure the branch exists on the remote repository.
- Check that the token is still valid.

### Error: 'requests' Library Missing

If you see:
```
Error: 'requests' library is required. Install it with: pip install requests
```

**Solution**: Install the `requests` library:
```bash
pip install requests
```

---

## 📜 License

This guide and the associated scripts are provided as-is for use in the **Interceptor_M** project.

---

## 🙌 Contributing

If you have suggestions or improvements, feel free to open an issue or submit a PR!