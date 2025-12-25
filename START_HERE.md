# 🎯 START HERE - Quick Testing Guide

## ⚡ Fastest Way to Test (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
**OR** just double-click: `install.bat`

### 2️⃣ Start Server
```bash
python app.py
```
**OR** just double-click: `run.bat`

### 3️⃣ Test in Browser
Browser opens automatically at: **http://127.0.0.1:5000**

---

## 🧪 What You'll See

### **Main Page:**
```
┌─────────────────────────────────────┐
│   📁 File Upload Agent              │
│   Upload and manage files           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📊 Statistics                       │
│ Total Files: 0                     │
│ Training Completed: 0               │
└─────────────────────────────────────┘

┌──────────┬──────────┬──────────┐
│ 📄 Text  │ 🖼️ Image │ 🎵 Audio │
│ Files    │ Files    │ Files    │
└──────────┴──────────┴──────────┘

┌─────────────────────────────────────┐
│ 📋 Uploaded Files                   │
│ [🔄 Refresh] [📜 View History]     │
│                                     │
│ (Files will appear here)            │
└─────────────────────────────────────┘
```

---

## ✅ Quick Test Steps

### **Test 1: Upload a File**
1. Click on "📄 Text Files" area
2. Select `test_claim.txt` (I created this for you!)
3. ✅ File should appear in "Uploaded Files"

### **Test 2: Train the File**
1. Click "🎓 Train" button next to the file
2. Wait 1-2 seconds
3. ✅ Modal popup appears with structured data:
   ```
   case_id=CLM-2024-001
   claim_type=Auto Insurance
   state=CA
   ...
   ```

### **Test 3: Check Database**
1. Look in folder → See `file_agent.db` file
2. ✅ Database file exists = Database is working!

### **Test 4: View History**
1. Click "📜 View History"
2. ✅ See all training operations listed

### **Test 5: Check Statistics**
1. Look at Statistics section
2. ✅ Numbers update after upload/train

---

## 🎯 What Success Looks Like

✅ **Frontend:**
- Beautiful interface loads
- Upload buttons work
- Files appear after upload
- Train button works
- Modal shows structured data

✅ **Database:**
- `file_agent.db` file exists
- Files persist after refresh
- Training history saved

✅ **Training:**
- Extracts structured data
- Shows in formatted output
- Saves to history

---

## 🐛 If Something Doesn't Work

### **"Module not found"**
→ Run: `pip install -r requirements.txt`

### **Port 5000 busy**
→ Edit `app.py`, change port to 5001

### **Browser doesn't open**
→ Manually go to: `http://127.0.0.1:5000`

### **PDF processing fails**
→ Run: `pip install PyPDF2`

---

## 📝 Test File Included

I've created `test_claim.txt` for you to test with!

Just:
1. Start server
2. Upload `test_claim.txt`
3. Click "Train"
4. See the magic! ✨

---

## 🎉 You're Ready!

Everything is set up. Just run:
```bash
python app.py
```

And start testing! 🚀

