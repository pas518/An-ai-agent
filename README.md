# 🤖 AI File Processing Agent - Complete Website

A complete AI-powered file processing agent with intelligent document analysis, structured data extraction, and comprehensive file management.

## Features

- 📄 **Text File Upload**: Support for TXT, MD, DOC, DOCX files
- 🖼️ **Image File Upload**: Support for PNG, JPG, JPEG, GIF, WEBP files
- 🎵 **Audio File Upload**: Support for MP3, WAV, OGG, FLAC, M4A, AAC files
- 📋 **File Management**: View and delete uploaded files with database tracking
- 🎓 **File Training**: Process and analyze uploaded files (text analysis, image processing, audio analysis)
- 📊 **Statistics Dashboard**: View total files and training statistics
- 📜 **Training History**: Track all training/processing operations with detailed history
- 💾 **SQLite Database**: Persistent storage for file metadata and training history
- 🎨 **Modern UI**: Clean and responsive interface

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Navigate to `http://127.0.0.1:5000`
   - The application will open automatically

## Usage

1. **Upload Files:**
   - Click on any of the upload areas (Text, Image, or Audio)
   - Select one or multiple files
   - Files will be uploaded automatically

2. **View Files:**
   - All uploaded files are displayed in the "Uploaded Files" section
   - Files show upload date, status, and training count
   - Files are organized by type with file size information

3. **Train Files:**
   - Click the "🎓 Train" button next to any file to process it
   - Text files: Analyzes word count, character count, and line count
   - Image files: Extracts dimensions and metadata
   - Audio files: Processes audio file information
   - Training status is tracked and displayed in real-time

4. **View Training History:**
   - Click "📜 View History" to see all training operations
   - View processing times, results, and any errors
   - History includes timestamps and detailed information

5. **Delete Files:**
   - Click the "Delete" button next to any file to remove it
   - Deletes both the file and its database record

## Project Structure

```
.
├── app.py              # Flask backend server with database
├── models.py          # Database models (FileRecord, TrainingHistory)
├── index.html         # Main HTML page
├── static/
│   ├── style.css     # Styling
│   └── script.js     # Frontend JavaScript
├── uploads/           # Uploaded files (created automatically)
│   ├── text/         # Text files
│   ├── image/        # Image files
│   └── audio/        # Audio files
├── file_agent.db      # SQLite database (created automatically)
├── requirements.txt   # Python dependencies
├── install.bat        # Windows installation script
├── run.bat           # Windows launcher script
└── README.md         # This file
```

## Configuration

- **Port**: Default is 5000 (change in `app.py` if needed)
- **Max File Size**: 100MB (configurable in `app.py`)
- **Upload Folder**: `uploads/` directory (created automatically)
- **Database**: SQLite database `file_agent.db` (created automatically on first run)

## Database

The application uses SQLite to store:
- **File Records**: All uploaded files with metadata (filename, type, size, upload date, status)
- **Training History**: Complete history of all training/processing operations with results and timestamps

The database is automatically created when you first run the application. All file operations are tracked in the database for history and statistics.

## Desktop Installation (Optional)

To create a standalone desktop application:

### Option 1: Using PyInstaller

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create executable:
   ```bash
   pyinstaller --onefile --windowed --name "FileUploadAgent" app.py
   ```

3. The executable will be in the `dist/` folder

### Option 2: Using Electron (for cross-platform)

1. Install Electron:
   ```bash
   npm install -g electron
   ```

2. Create an Electron wrapper (see Electron documentation)

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (line 126)
- **Upload fails**: Check file size (max 100MB) and file type
- **Files not showing**: Click the "Refresh" button
- **Database errors**: Delete `file_agent.db` to reset the database (this will delete all records)
- **Training fails**: Check file format and ensure the file is not corrupted

## License

This project is open source and available for personal use.

