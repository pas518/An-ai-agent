# 🔗 Supabase Database Setup Guide

## 📋 Overview

This guide will help you connect your AI File Processing Agent to Supabase (PostgreSQL) instead of the local SQLite database.

## 🚀 Quick Setup Steps

### Step 1: Create Supabase Account
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project

### Step 2: Get Your Database Credentials

#### Option A: Connection Pooler URL (Recommended)
1. Go to **Project Settings** → **Database**
2. Scroll to **Connection Pooling**
3. Copy the **Connection string** (URI format)
4. It looks like: `postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres`

#### Option B: Individual Components
1. Go to **Project Settings** → **Database**
2. Find these values:
   - **Host**: `db.[your-project-ref].supabase.co`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres`
   - **Password**: Your database password

### Step 3: Configure Your App

1. **Create `.env` file** in the project root:
   ```bash
   # Copy the example file
   copy .env.example .env
   ```

2. **Edit `.env` file** and add your credentials:

   **Option A - Using Connection URL:**
   ```env
   SUPABASE_URL=postgresql://postgres:your-password@your-project.supabase.co:5432/postgres
   ```

   **Option B - Using Individual Components:**
   ```env
   SUPABASE_DB_HOST=db.your-project.supabase.co
   SUPABASE_DB_PORT=5432
   SUPABASE_DB_NAME=postgres
   SUPABASE_DB_USER=postgres
   SUPABASE_DB_PASSWORD=your-password
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python app.py
   ```

## ✅ Verification

When you start the server, you should see:
```
✅ Connected to Supabase (PostgreSQL)
```

If you see:
```
✅ Using SQLite database (local)
```
Then Supabase connection is not configured, and it's using local SQLite.

## 🔧 Troubleshooting

### Connection Failed
- **Check credentials**: Make sure password and host are correct
- **Check network**: Ensure you can reach Supabase servers
- **Check SSL**: Supabase requires SSL connections

### "Module not found: psycopg2"
```bash
pip install psycopg2-binary
```

### "Connection timeout"
- Check if your IP is allowed in Supabase dashboard
- Supabase free tier has connection limits
- Try using Connection Pooler instead of direct connection

### Still using SQLite?
- Check `.env` file exists
- Check credentials are correct
- Check file is in project root directory
- Restart the server after changing `.env`

## 📊 Database Schema

The app will automatically create these tables in Supabase:

1. **files** - Stores uploaded file metadata
2. **training_history** - Stores processing history

## 🔒 Security Notes

- **Never commit `.env` file** to git
- `.env` is already in `.gitignore`
- Keep your database password secure
- Use Supabase's connection pooler for better performance

## 🎯 Benefits of Supabase

✅ **Cloud Storage** - Access from anywhere  
✅ **Scalability** - Handles more data  
✅ **Backup** - Automatic backups  
✅ **Real-time** - Can add real-time features later  
✅ **Free Tier** - 500MB database, 2GB bandwidth  

## 🔄 Switching Back to SQLite

If you want to use SQLite again:
1. Delete or rename `.env` file
2. Restart the server
3. It will automatically use SQLite

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres)

---

**Need Help?** Check the server logs for detailed error messages.


