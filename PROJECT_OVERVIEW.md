# 🤖 AI File Processing Agent - Complete Project

## 📋 Project Overview

This is a **complete AI-powered file processing agent** that:
- 📤 Uploads and manages files (Text, Image, Audio)
- 🧠 Extracts structured data from documents
- 💾 Stores data in SQLite database
- 📊 Tracks processing history
- 🎯 Provides intelligent claim data extraction

## 🏗️ Project Structure

```
AI-File-Processing-Agent/
│
├── app.py                 # Main Flask backend server
├── models.py             # Database models (SQLAlchemy)
├── index.html            # Frontend HTML
├── requirements.txt      # Python dependencies
│
├── static/              # Frontend assets
│   ├── style.css        # Styling
│   └── script.js        # JavaScript/AJAX
│
├── uploads/             # Uploaded files (auto-created)
│   ├── text/
│   ├── image/
│   └── audio/
│
├── file_agent.db        # SQLite database (auto-created)
│
├── install.bat          # Windows installation script
├── run.bat              # Windows launcher
│
└── Documentation/
    ├── README.md        # Main documentation
    ├── HOW_TO_TEST.md   # Testing guide
    └── TROUBLESHOOTING.md # Troubleshooting
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
Or double-click: `install.bat`

### 2. Run the Application
```bash
python app.py
```
Or double-click: `run.bat`

### 3. Access the Website
Browser opens automatically at: **http://127.0.0.1:5000**

## ✨ Features

### 🤖 AI-Powered Features
- **Intelligent Data Extraction**: Automatically extracts structured data from documents
- **Claim Processing**: Specialized for insurance claim data extraction
- **Pattern Recognition**: Uses regex patterns to find relevant information
- **Smart Categorization**: Automatically categorizes files by type

### 📁 File Management
- Upload Text, Image, and Audio files
- Support for PDF, DOC, DOCX, TXT, MD
- Image formats: PNG, JPG, JPEG, GIF, WEBP
- Audio formats: MP3, WAV, OGG, FLAC, M4A, AAC

### 💾 Database Features
- SQLite database for persistent storage
- File metadata tracking
- Training history
- Statistics dashboard

### 📊 Structured Data Extraction
Extracts from documents:
- `case_id` - Case identifier
- `claim_type` - Type of claim
- `state` - US state
- `policy_type` - Policy category
- `claim_amount` - Monetary amount
- `filled_date` - Date information
- `special_flags` - Important flags
- `case_description` - Full description

## 🎯 How It Works

1. **Upload Files**: Drag & drop or click to upload
2. **AI Processing**: Click "Train" to process files
3. **Data Extraction**: AI extracts structured data
4. **View Results**: See extracted data in modal popup
5. **History Tracking**: All operations saved to database

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite + SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Processing**: PyPDF2
- **API**: RESTful endpoints

## 📡 API Endpoints

- `GET /` - Main page
- `POST /api/upload` - Upload files
- `GET /api/files` - List all files
- `GET /api/files/<id>` - Get file details
- `DELETE /api/files/<id>` - Delete file
- `POST /api/train/<id>` - Process/train file
- `GET /api/training-history` - Get training history
- `GET /api/stats` - Get statistics
- `GET /api/health` - Health check

## 🎨 UI Features

- Modern, responsive design
- Real-time file upload status
- Interactive training history
- Statistics dashboard
- Modal popups for results
- Copy-to-clipboard functionality

## 📦 Dependencies

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
PyPDF2==3.0.1
```

## 🔒 Security Features

- File type validation
- Secure filename handling
- File size limits (100MB)
- SQL injection protection (SQLAlchemy)
- CORS enabled for local development

## 📈 Future Enhancements

- [ ] Machine learning model integration
- [ ] OCR for image text extraction
- [ ] Audio transcription
- [ ] Multi-language support
- [ ] Cloud storage integration
- [ ] User authentication
- [ ] Advanced analytics

## 🐛 Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.

## 📝 License

This project is open source and available for personal use.

## 👨‍💻 Development

To contribute or modify:
1. Install dependencies: `pip install -r requirements.txt`
2. Run in debug mode: `python app.py`
3. Check logs in terminal
4. Use browser console (F12) for frontend debugging

---

**Built with ❤️ using Flask, SQLAlchemy, and modern web technologies**

