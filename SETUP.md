# Interceptor M - Setup Guide

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies:
- `flask` - Web framework
- `supabase` - Supabase client
- `python-dotenv` - Environment variables loader

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Supabase credentials:

```bash
cp .env.example .env
```

Or create `.env` manually with:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_supabase_key
```

### 3. Run the Application

```bash
python app.py
```

The app will start at `http://localhost:5000`

### 4. Supabase Agent Skills (Optional)

For enhanced Supabase integration in AI coding tools:

```bash
npx skills add supabase/agent-skills
```

## Project Structure

```
Interceptor_M/
├── .env           # Supabase credentials (not committed)
├── .env.example   # Template for .env
├── app.py         # Main Flask application
├── requirements.txt
└── SETUP.md       # This file
```
