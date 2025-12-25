# ⚡ Quick Supabase Setup (5 Minutes)

## 🚀 Fastest Way to Connect

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Setup Script
```bash
python setup_supabase.py
```

Follow the prompts to enter your Supabase credentials.

### Step 3: Start Server
```bash
python app.py
```

You should see: `✅ Connected to Supabase (PostgreSQL)`

---

## 📋 Manual Setup (Alternative)

### 1. Get Supabase Credentials

Go to: **Supabase Dashboard** → **Project Settings** → **Database**

Copy your **Connection Pooling URL** (looks like):
```
postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres
```

### 2. Create `.env` File

Create a file named `.env` in the project root:

```env
SUPABASE_URL=postgresql://postgres:your-password@your-project.supabase.co:5432/postgres
```

### 3. Start Server

```bash
python app.py
```

---

## ✅ Verify Connection

When server starts, you should see:
```
✅ Connected to Supabase (PostgreSQL)
```

If you see:
```
✅ Using SQLite database (local)
```
Then Supabase is not configured (using local database).

---

## 🔄 Switch Back to SQLite

Delete or rename `.env` file, then restart server.

---

## 📚 Full Guide

See `SUPABASE_SETUP.md` for detailed instructions.


