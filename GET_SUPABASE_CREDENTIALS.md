# 🔑 How to Get Supabase Credentials (Visual Guide)

## 📍 Step-by-Step with Screenshots Location

### 1. Login to Supabase
**URL**: https://supabase.com

- Click **"Start your project"**
- Sign up with GitHub, Google, or Email
- Verify email if needed

---

### 2. Create Project

After login:
- Click **"New Project"** button
- Fill in:
  - **Name**: `AI File Agent` (or any name)
  - **Database Password**: Create and **SAVE THIS!**
  - **Region**: Choose closest
  - **Plan**: Free
- Click **"Create new project"**
- Wait 2-3 minutes

---

### 3. Get Connection Credentials

#### Path in Dashboard:
```
Dashboard → Your Project → ⚙️ Settings → Database
```

#### What You'll See:

**Option A: Connection Pooling (Recommended)**
- Tab: **"Connection Pooling"**
- Format: **"URI"**
- Copy the entire connection string
- Looks like:
  ```
  postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
  ```

**Option B: Connection String (Direct)**
- Tab: **"Connection string"**
- Format: **"URI"**
- Copy the connection string
- Looks like:
  ```
  postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres
  ```

**Option C: Individual Components**
- **Host**: `db.[your-project-ref].supabase.co`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres`
- **Password**: (the one you created)

---

## 📋 Quick Copy-Paste Template

Once you have your connection string, create `.env` file:

```env
SUPABASE_URL=postgresql://postgres:YOUR-PASSWORD-HERE@db.YOUR-PROJECT-REF.supabase.co:5432/postgres
```

**Replace:**
- `YOUR-PASSWORD-HERE` → Your database password
- `YOUR-PROJECT-REF` → Your project reference (in the URL)

---

## 🎯 Example

If your connection string is:
```
postgresql://postgres:MySecurePass123@db.abcdefghijk.supabase.co:5432/postgres
```

Your `.env` file should be:
```env
SUPABASE_URL=postgresql://postgres:MySecurePass123@db.abcdefghijk.supabase.co:5432/postgres
```

---

## ✅ Verification

After setting up, when you run:
```bash
python app.py
```

You should see:
```
✅ Connected to Supabase (PostgreSQL)
```

If you see:
```
✅ Using SQLite database (local)
```

Then Supabase is not configured - check your `.env` file.

---

## 🆘 Need Help?

1. **Can't find connection string?**
   - Make sure you're in: **Settings** → **Database**
   - Look for **"Connection Pooling"** or **"Connection string"** section

2. **Forgot password?**
   - Go to: **Settings** → **Database** → **Reset database password**

3. **Project not ready?**
   - Wait 2-3 minutes after creating
   - Check project status in dashboard

---

**That's all you need!** 🚀


