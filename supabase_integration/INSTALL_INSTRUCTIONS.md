# Installation Guide - Interceptor_M

## Prerequisites

- Python 3.9+
- pip package manager

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

## Supabase Configuration

Get your credentials from your Supabase project dashboard and add them to the `.env` file:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```