#  AI File Processing Agent - Complete Website

A complete AI-powered file processing agent with intelligent document analysis, structured data extraction, and comprehensive file management.

## Features

-  **Text File Upload**: Support for TXT, MD, DOC, DOCX files
-  **Image File Upload**: Support for PNG, JPG, JPEG, GIF, WEBP files
-  **Audio File Upload**: Support for MP3, WAV, OGG, FLAC, M4A, AAC files
-  **File Management**: View and delete uploaded files with database tracking
-  **File Training**: Process and analyze uploaded files (text analysis, image processing, audio analysis)
-  **statistics Dashboard**: View total files and training statistics
-  **Training History**: Track all training/processing operations with detailed history
-  **SQLite Database**: Persistent storage for file metadata and training history
-  **Modern UI**: Clean and responsive interface

## Installation

step1:-intsall ollama or to have an api key :
1, ollama
   -works at offline
   
| Model             | Parameters | Size  | Download                         |
|------------------|------------|-------|----------------------------------|
| Gemma 3          | 1B         | 815MB | `ollama run gemma:1b`             |
| Gemma 3          | 4B         | 3.3GB | `ollama run gemma:4b`             |
| Gemma 3          | 12B        | 8.1GB | `ollama run gemma:12b`            |
| Gemma 3          | 27B        | 17GB  | `ollama run gemma:27b`            |
| QwQ              | 32B        | 20GB  | `ollama run qwq`                  |
| DeepSeek-R1      | 7B         | 4.7GB | `ollama run deepseek-r1`          |
| DeepSeek-R1      | 671B       | 404GB | `ollama run deepseek-r1:671b`     |
| Llama 4          | 109B       | 67GB  | `ollama run llama4:scout`         |
| Llama 4          | 400B       | 245GB | `ollama run llama4:maverick`      |
| Llama 3.3        | 70B        | 43GB  | `ollama run llama3.3`             |
| Llama 3.2        | 3B         | 2.0GB | `ollama run llama3.2`             |
| Llama 3.2        | 1B         | 1.3GB | `ollama run llama3.2:1b`          |
| Llama 3.2 Vision | 11B        | 7.9GB | `ollama run llama3.2-vision`      |
| Llama 3.2 Vision | 90B        | 55GB  | `ollama run llama3.2-vision:90b` |
| Llama 3.1        | 8B         | 4.7GB | `ollama run llama3.1`             |
| Llama 3.1        | 405B       | 231GB | `ollama run llama3.1:405b`        |
| Phi 4            | 14B        | 9.1GB | `ollama run phi4`                 |
| Phi 4 Mini       | 3.8B       | 2.5GB | `ollama run phi4-mini`            |
| Mistral          | 7B         | 4.1GB | `ollama run mistral`              |
| Moondream 2      | 1.4B       | 829MB | `ollama run moondream`            |
| Neural Chat      | 7B         | 4.1GB | `ollama run neural-chat`          |
| Starling         | 7B         | 4.1GB | `ollama run starling-lm`          |
| Code Llama       | 7B         | 3.8GB | `ollama run codellama`            |
| Llama 2 Uncensored | 7B      | 3.8GB | `ollama run llama2-uncensored`   |
| LLaVA            | 7B         | 4.5GB | `ollama run llava`                |
| Granite 3.3      | 8B         | 4.9GB | `ollama run granite3.3`           |

Note:You should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models.

2, API keys of other chatboats

replace the model name to be in agent.py files

step2:- installing packages
for windows: pip install faiss-cpu numpy requests
             pip insall ollama(after installing ollama on your system, only when use this instead other api keys)

step3:- Desktop Installation (Optional)

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

2. Create an Electron wrapper (see Electron documentation

 
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
AI-Agent-Projects/
│
├── 📁 1-Flask-Web-App/              # Insurance Claims Processing Website
│   ├── 📁 backend/
│   │   ├── app.py                    # Flask backend server with database
│   │   ├── models.py                 # Database models (FileRecord, TrainingHistory)
│   │   ├── config.py              
│   │   └── requirements.txt         
│   │
│   ├── 📁 frontend/
│   │   ├── index.html                # Main HTML page
│   │   └── 📁 static/
│   │       ├── script.js              # Styling
│   │       └── style.css           
│   │
│   ├── 📁 database/
│   │   └── file_agent.db           # SQLite database (created automatically)
│   │
│   ├── 📁 uploads/                  AUTO-CREATED
│   │   ├── text/
│   │   ├── image/
│   │   └── audio/
│   │
│   ├── 📁 scripts/
│   │   ├── install.bat            # Windows installation script
│   │   ├── run.bat                  # Windows launcher script
│   │   ├── START_AGENT.bat         
│   │   └── setup_supabase.py       
│   │
│   ├── 📁 docs/
│   │   ├── README.md               
│   │   ├── COMPLETE_SETUP.md              
│   │   ├── START_HERE.md            
│   │   ├── FIXES_APPLIED.md        
│   │   ├── TROUBLESHOOTING.md       
│   │   ├── QUICK_START.txt    
│   │
│   └── .gitignore                  
│
├── 📁 2-RAG-Agent/                  # Document Q&A System
│   ├── 📁 ingestion/
│   │   ├── ingest.py               
│   │                 
│   │
│   ├── 📁 agents/
│   │   ├── agent.py                 (basic version)
│   │   └── agent1.py                 (enhanced version)
│   │
│   ├── 📁 data/                      
│   │   └── (our PDFs here)
│   │
│   ├── 📁 indexes/
│   │   ├── index.faiss              AUTO-CREATED by ingest.py
│   │   └── metadata.pkl             AUTO-CREATED by agent.py
│   │
│   ├── 📁 docs/
│   │   └── RAG_AGENT_README.md      
│   │
│   └── requirements.txt            # Python dependencies
│
└── 📁 3-Shared-Resources/
    └── 📁 training-data/
        └── (insurance policy samples)

   
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



## Troubleshooting

- **Port already in use**: Change the port in `app.py` (line 126)
- **Upload fails**: Check file size (max 100MB) and file type
- **Files not showing**: Click the "Refresh" button
- **Database errors**: Delete `file_agent.db` to reset the database (this will delete all records)
- **Training fails**: Check file format and ensure the file is not corrupted

## License

This project is open source and available for personal use.


