# 🚀 How to Test Your File Upload Agent

## Step-by-Step Testing Instructions

### **Step 1: Install Dependencies**

Open Command Prompt or PowerShell in this folder and run:

```bash
pip install -r requirements.txt
```

**OR** double-click `install.bat` (Windows)

This will install:
- Flask (web server)
- Flask-CORS (cross-origin support)
- Flask-SQLAlchemy (database)
- PyPDF2 (PDF processing)

### **Step 2: Start the Application**

**Option A - Using Batch File (Easiest):**
- Double-click `run.bat`
- The server will start and browser will open automatically

**Option B - Using Command Line:**
```bash
python app.py
```

You should see:
```
==================================================
  File Upload Agent - Starting Server
==================================================

  Server will start at: http://127.0.0.1:5000
  Database: file_agent.db
  Opening browser automatically...
  Press Ctrl+C to stop the server

==================================================
```

The browser should open automatically at `http://127.0.0.1:5000`

### **Step 3: Test the Frontend**

1. **Check the UI:**
   - You should see 3 upload sections: Text, Image, Audio
   - Statistics section at the top
   - "Uploaded Files" section below

2. **Test File Upload:**
   - Click on "📄 Text Files" area
   - Select any text file (.txt, .md, .pdf, etc.)
   - File should appear in "Uploaded Files" section

### **Step 4: Test Database**

1. **Check Database Creation:**
   - Look in the project folder
   - You should see `file_agent.db` file (SQLite database)
   - This stores all your file records

2. **Verify Data Storage:**
   - Upload a file
   - Check the database file size (should increase)
   - Refresh the page - file should still be there

### **Step 5: Test Training/Structured Data Extraction**

1. **Create a Test File:**

Create a file named `test_claim.txt` with this content:
```
Case ID: CLM-2024-001
Claim Type: Auto Insurance
State: California
Policy Type: Individual
Claim Amount: $15,000.00
Filed Date: 12/25/2024

Case Description:
Vehicle accident occurred on Highway 101. Driver was rear-ended
by another vehicle. Vehicle damage estimated at $15,000.
Special flags: Urgent, Review required.
```

2. **Upload and Train:**
   - Upload the `test_claim.txt` file
   - Click the "🎓 Train" button next to the file
   - Wait 1-2 seconds

3. **Check Results:**
   - A modal popup should appear showing:
     ```
     case_id=CLM-2024-001
     claim_type=Auto Insurance
     state=CA
     policy_type=Individual
     claim_amount=$15,000.00
     filled_date=12/25/2024
     special_flags=['Urgent', 'Review']
     case_description=Vehicle accident occurred...
     ```

### **Step 6: Test Training History**

1. Click "📜 View History" button
2. You should see all training operations listed
3. Each entry shows:
   - Training type
   - Status (Completed/Failed)
   - Processing time
   - Extracted structured data

### **Step 7: Test Statistics**

Check the Statistics section:
- **Total Files:** Should show number of uploaded files
- **Training Completed:** Should show number of successful trainings

### **Step 8: Test File Management**

1. **Delete a File:**
   - Click "🗑️ Delete" button next to any file
   - Confirm deletion
   - File should disappear from list
   - Statistics should update

2. **Refresh:**
   - Click "🔄 Refresh" button
   - All data should reload from database

## 🧪 Quick Test Checklist

- [ ] Server starts without errors
- [ ] Browser opens to `http://127.0.0.1:5000`
- [ ] Can see upload areas (Text, Image, Audio)
- [ ] Can upload a text file
- [ ] File appears in "Uploaded Files" section
- [ ] Can click "Train" button
- [ ] Structured data modal appears after training
- [ ] Can view training history
- [ ] Statistics update correctly
- [ ] Can delete files
- [ ] Database file (`file_agent.db`) exists

## 🐛 Troubleshooting

### **"Module not found" error:**
```bash
pip install -r requirements.txt
```

### **Port 5000 already in use:**
- Close other applications using port 5000
- Or edit `app.py` line 569, change port to 5001

### **Browser doesn't open:**
- Manually go to: `http://127.0.0.1:5000`

### **PDF processing fails:**
```bash
pip install PyPDF2
```

### **Database errors:**
- Delete `file_agent.db` file
- Restart server (database will be recreated)

## 📊 What to Look For

✅ **Frontend Working:**
- Clean, modern interface
- Upload areas respond to clicks
- Files appear after upload
- Buttons work (Train, Delete, Refresh)

✅ **Database Working:**
- `file_agent.db` file exists
- Files persist after page refresh
- Training history is saved

✅ **Training Working:**
- Training completes in 1-3 seconds
- Structured data is extracted
- Modal shows formatted output
- History records are created

## 🎯 Expected Results

When everything works:
1. Upload → File appears immediately
2. Train → Modal shows structured data in 1-2 seconds
3. History → All operations are recorded
4. Database → Data persists after restart

## 💡 Pro Tips

- Use the PDF files in your folder (`header information.pdf`, `Policy Title.pdf`) to test
- Check browser console (F12) for any JavaScript errors
- Check server terminal for Python errors
- Training works best with text/PDF files containing claim information

