# 🔧 Troubleshooting File Upload Failures

## Common Issues and Solutions

### ❌ Issue: "Upload failed" or "Error" status

#### **1. Server Not Running**
**Symptoms:**
- Files show "✗ Error" immediately
- Notification says "Cannot connect to server"
- Browser console shows "Failed to fetch"

**Solution:**
```bash
# Start the server
python app.py
```
Make sure you see:
```
* Running on http://127.0.0.1:5000
```

---

#### **2. Wrong File Type**
**Symptoms:**
- Error message: "Invalid file type for [type]"
- File uploads but fails validation

**Solution:**
- **Text files:** `.txt`, `.md`, `.doc`, `.docx`, `.pdf`
- **Image files:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`
- **Audio files:** `.mp3`, `.wav`, `.ogg`, `.flac`, `.m4a`, `.aac`

Make sure you're uploading to the correct section!

---

#### **3. Port Already in Use**
**Symptoms:**
- Server won't start
- Error: "Address already in use"

**Solution:**
```python
# Edit app.py, line 569, change port:
app.run(debug=True, host='127.0.0.1', port=5001)
```
Then access at: `http://127.0.0.1:5001`

---

#### **4. Database Errors**
**Symptoms:**
- Error: "Database error: ..."
- Files upload but don't save

**Solution:**
```bash
# Delete database and restart
del file_agent.db
python app.py
```

---

#### **5. CORS Issues**
**Symptoms:**
- Browser console shows CORS errors
- Files fail to upload

**Solution:**
- Make sure `flask-cors` is installed: `pip install flask-cors`
- Check that `CORS(app)` is in `app.py` (line 14)

---

#### **6. File Too Large**
**Symptoms:**
- Error: "Request entity too large"
- Large files fail to upload

**Solution:**
- Current limit: 100MB
- To change, edit `app.py` line 37:
```python
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
```

---

## 🔍 Debugging Steps

### **Step 1: Check Browser Console**
1. Open browser (F12)
2. Go to "Console" tab
3. Look for red error messages
4. Check "Network" tab for failed requests

### **Step 2: Check Server Logs**
1. Look at the terminal where `python app.py` is running
2. Check for error messages
3. Look for stack traces

### **Step 3: Test Server Connection**
1. Open browser
2. Go to: `http://127.0.0.1:5000/api/health`
3. Should see: `{"status":"ok","message":"Server is running","database":"connected"}`

### **Step 4: Test API Endpoint**
1. Open browser
2. Go to: `http://127.0.0.1:5000/api/files`
3. Should see: `{"files":[]}` (empty if no files)

---

## 🧪 Quick Tests

### **Test 1: Server Health**
```bash
# In browser, go to:
http://127.0.0.1:5000/api/health
```
Expected: `{"status":"ok"}`

### **Test 2: File Upload (using curl)**
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "file=@test_claim.txt" \
  -F "fileType=text"
```
Expected: JSON response with file info

### **Test 3: List Files**
```bash
curl http://127.0.0.1:5000/api/files
```
Expected: `{"files":[...]}`

---

## 🐛 Common Error Messages

### **"Cannot connect to server"**
→ Server not running. Start with: `python app.py`

### **"Invalid file type"**
→ Wrong file extension. Check allowed types above.

### **"No file provided"**
→ File input issue. Check browser console.

### **"Database error"**
→ Database issue. Delete `file_agent.db` and restart.

### **"Upload failed: Unknown error"**
→ Check server logs for detailed error.

---

## ✅ Verification Checklist

- [ ] Server is running (`python app.py`)
- [ ] Browser shows page at `http://127.0.0.1:5000`
- [ ] No errors in browser console (F12)
- [ ] No errors in server terminal
- [ ] File type matches upload section
- [ ] File size under 100MB
- [ ] Database file exists (`file_agent.db`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)

---

## 🆘 Still Not Working?

1. **Check all files exist:**
   - `app.py`
   - `models.py`
   - `index.html`
   - `static/script.js`
   - `static/style.css`

2. **Reinstall dependencies:**
   ```bash
   pip uninstall flask flask-cors flask-sqlalchemy sqlalchemy pypdf2 -y
   pip install -r requirements.txt
   ```

3. **Reset everything:**
   ```bash
   # Delete database
   del file_agent.db
   
   # Delete uploads
   rmdir /s uploads
   
   # Restart server
   python app.py
   ```

4. **Check Python version:**
   ```bash
   python --version
   ```
   Should be Python 3.7 or higher.

---

## 📞 Need More Help?

Check the error message in:
1. Browser console (F12 → Console tab)
2. Server terminal output
3. Notification popup in the app

The improved error handling will now show more specific error messages!

