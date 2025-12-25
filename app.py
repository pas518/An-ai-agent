from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import json
import webbrowser
import threading
import time
from datetime import datetime
from models import db, FileRecord, TrainingHistory
import hashlib
import re
from config import get_database_uri, USE_SUPABASE

app = Flask(__name__)
CORS(app)

# Database Configuration - Supports Supabase (PostgreSQL) or SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PostgreSQL/Supabase specific settings
if USE_SUPABASE:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'connect_timeout': 10,
            'sslmode': 'require'
        }
    }

# Initialize database
db.init_app(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'text': {'txt', 'md', 'doc', 'docx', 'pdf'},
    'image': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'},
    'audio': {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac'}
}

# Create upload directories
for file_type in ['text', 'image', 'audio']:
    upload_dir = os.path.join(UPLOAD_FOLDER, file_type)
    os.makedirs(upload_dir, exist_ok=True)
    # Ensure directory is writable
    if not os.access(upload_dir, os.W_OK):
        app.logger.warning(f'Upload directory not writable: {upload_dir}')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        if USE_SUPABASE:
            print("✅ Connected to Supabase (PostgreSQL)")
        else:
            print("✅ Using SQLite database (local)")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {str(e)}")
        print("   Trying to continue...")

def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, set())

def extract_text_from_pdf(filepath):
    """Extract text from PDF file"""
    try:
        import PyPDF2
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        return None

def extract_structured_claim_data(content):
    """Extract structured claim data from text content"""
    # Initialize structured data
    structured_data = {
        'case_id': '',
        'claim_type': '',
        'state': '',
        'policy_type': '',
        'claim_amount': '',
        'filled_date': '',
        'special_flags': [],
        'case_description': ''
    }
    
    # Convert content to lowercase for case-insensitive matching
    content_lower = content.lower()
    content_original = content
    
    # Extract Case ID - look for patterns like "Case ID:", "Case #", "Case Number:", etc.
    case_id_patterns = [
        r'case\s*id[:\s]+([A-Z0-9\-]+)',
        r'case\s*#\s*([A-Z0-9\-]+)',
        r'case\s*number[:\s]+([A-Z0-9\-]+)',
        r'claim\s*id[:\s]+([A-Z0-9\-]+)',
        r'claim\s*#\s*([A-Z0-9\-]+)',
        r'id[:\s]+([A-Z]{2,}\d{4,})',
    ]
    for pattern in case_id_patterns:
        match = re.search(pattern, content_original, re.IGNORECASE)
        if match:
            structured_data['case_id'] = match.group(1).strip()
            break
    
    # Extract Claim Type
    claim_type_patterns = [
        r'claim\s*type[:\s]+([^\n]+)',
        r'type\s*of\s*claim[:\s]+([^\n]+)',
        r'claim\s*category[:\s]+([^\n]+)',
    ]
    claim_types = ['auto', 'health', 'property', 'life', 'disability', 'liability', 'medical', 'accident']
    for pattern in claim_type_patterns:
        match = re.search(pattern, content_original, re.IGNORECASE)
        if match:
            structured_data['claim_type'] = match.group(1).strip()
            break
    # If not found, try to detect from keywords
    if not structured_data['claim_type']:
        for ctype in claim_types:
            if ctype in content_lower:
                structured_data['claim_type'] = ctype.capitalize()
                break
    
    # Extract State - US states
    us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state_patterns = [
        r'state[:\s]+([A-Z]{2})\b',
        r'location[:\s]+([A-Z]{2})\b',
        r'\b([A-Z]{2})\s+state\b',
    ]
    for pattern in state_patterns:
        match = re.search(pattern, content_original)
        if match and match.group(1) in us_states:
            structured_data['state'] = match.group(1)
            break
    
    # Extract Policy Type
    policy_type_patterns = [
        r'policy\s*type[:\s]+([^\n]+)',
        r'type\s*of\s*policy[:\s]+([^\n]+)',
        r'policy\s*category[:\s]+([^\n]+)',
    ]
    policy_types = ['individual', 'group', 'family', 'corporate', 'commercial', 'personal']
    for pattern in policy_type_patterns:
        match = re.search(pattern, content_original, re.IGNORECASE)
        if match:
            structured_data['policy_type'] = match.group(1).strip()
            break
    if not structured_data['policy_type']:
        for ptype in policy_types:
            if ptype in content_lower:
                structured_data['policy_type'] = ptype.capitalize()
                break
    
    # Extract Claim Amount
    amount_patterns = [
        r'claim\s*amount[:\s$]+([\d,]+\.?\d*)',
        r'amount[:\s$]+([\d,]+\.?\d*)',
        r'\$([\d,]+\.?\d*)',
        r'([\d,]+\.?\d*)\s*dollars?',
    ]
    for pattern in amount_patterns:
        matches = re.findall(pattern, content_original, re.IGNORECASE)
        if matches:
            # Get the largest amount (likely the claim amount)
            amounts = [float(m.replace(',', '')) for m in matches]
            if amounts:
                structured_data['claim_amount'] = f"${max(amounts):,.2f}"
                break
    
    # Extract Filled Date / Filed Date
    date_patterns = [
        r'filed?\s*date[:\s]+([^\n]+)',
        r'date\s*filed[:\s]+([^\n]+)',
        r'submission\s*date[:\s]+([^\n]+)',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, content_original, re.IGNORECASE)
        if match:
            structured_data['filled_date'] = match.group(1).strip()
            break
    
    # Extract Special Flags
    flag_keywords = ['urgent', 'priority', 'fraud', 'investigation', 'appeal', 'denied', 'approved', 'pending', 'review']
    for keyword in flag_keywords:
        if keyword in content_lower:
            structured_data['special_flags'].append(keyword.capitalize())
    
    # Extract Case Description - usually the longest paragraph or section
    description_patterns = [
        r'description[:\s]+([^\n]+(?:\n[^\n]+){0,10})',
        r'case\s*description[:\s]+([^\n]+(?:\n[^\n]+){0,10})',
        r'details[:\s]+([^\n]+(?:\n[^\n]+){0,10})',
    ]
    for pattern in description_patterns:
        match = re.search(pattern, content_original, re.IGNORECASE | re.DOTALL)
        if match:
            structured_data['case_description'] = match.group(1).strip()[:500]  # Limit to 500 chars
            break
    
    # If no description found, use first substantial paragraph
    if not structured_data['case_description']:
        paragraphs = [p.strip() for p in content_original.split('\n\n') if len(p.strip()) > 50]
        if paragraphs:
            structured_data['case_description'] = paragraphs[0][:500]
    
    return structured_data

def process_text_file(filepath):
    """Process text/PDF file and extract structured claim data"""
    try:
        content = ""
        file_ext = os.path.splitext(filepath)[1].lower()
        
        # Read text or PDF
        if file_ext == '.pdf':
            content = extract_text_from_pdf(filepath)
            if content is None:
                return {
                    'success': False,
                    'error': 'PDF processing requires PyPDF2. Install with: pip install PyPDF2'
                }
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        
        if not content or len(content.strip()) == 0:
            return {
                'success': False,
                'error': 'File is empty or could not extract text'
            }
        
        # Extract structured claim data
        structured_data = extract_structured_claim_data(content)
        
        # Basic text analysis
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.splitlines())
        
        # Format output as requested
        output_format = f"""case_id={structured_data['case_id'] or 'N/A'}
claim_type={structured_data['claim_type'] or 'N/A'}
state={structured_data['state'] or 'N/A'}
policy_type={structured_data['policy_type'] or 'N/A'}
claim_amount={structured_data['claim_amount'] or 'N/A'}
filled_date={structured_data['filled_date'] or 'N/A'}
special_flags={structured_data['special_flags'] if structured_data['special_flags'] else '[]'}
case_description={structured_data['case_description'] or 'N/A'}"""
        
        metadata = {
            'wordCount': word_count,
            'charCount': char_count,
            'lineCount': line_count,
            'structuredData': structured_data,
            'processedAt': datetime.utcnow().isoformat()
        }
        
        return {
            'success': True,
            'metadata': metadata,
            'structuredOutput': output_format,
            'summary': f'Extracted structured data: Case ID={structured_data["case_id"] or "N/A"}, Claim Type={structured_data["claim_type"] or "N/A"}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_image_file(filepath):
    """Process image file for training"""
    try:
        # Basic image metadata
        file_size = os.path.getsize(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        
        metadata = {
            'fileSize': file_size,
            'format': ext[1:] if ext else 'unknown',
            'processedAt': datetime.utcnow().isoformat()
        }
        
        # Try to get image dimensions if PIL is available
        try:
            from PIL import Image
            with Image.open(filepath) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['mode'] = img.mode
        except ImportError:
            pass
        except Exception:
            pass
        
        return {
            'success': True,
            'metadata': metadata,
            'summary': f'Image file processed: {metadata.get("width", "?")}x{metadata.get("height", "?")}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def process_audio_file(filepath):
    """Process audio file for training"""
    try:
        file_size = os.path.getsize(filepath)
        ext = os.path.splitext(filepath)[1].lower()
        
        metadata = {
            'fileSize': file_size,
            'format': ext[1:] if ext else 'unknown',
            'processedAt': datetime.utcnow().isoformat()
        }
        
        return {
            'success': True,
            'metadata': metadata,
            'summary': f'Audio file processed: {file_size} bytes'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and save to database"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided', 'success': False}), 400
        
        file = request.files['file']
        file_type = request.form.get('fileType', 'text')
        
        # Validate file
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected', 'success': False}), 400
        
        # Validate file type
        if not allowed_file(file.filename, file_type):
            allowed = ', '.join(ALLOWED_EXTENSIONS.get(file_type, []))
            return jsonify({
                'error': f'Invalid file type for {file_type}. Allowed types: {allowed}',
                'success': False
            }), 400
        
        # Process file
        original_filename = file.filename
        filename = secure_filename(file.filename)
        
        # Ensure filename is not empty after securing
        if not filename:
            filename = f"file_{int(time.time())}"
            ext = os.path.splitext(original_filename)[1]
            if ext:
                filename += ext
        
        filepath = os.path.join(UPLOAD_FOLDER, file_type, filename)
        
        # Ensure upload directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Handle duplicate filenames
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, file_type, filename)
            counter += 1
        
        # Save file
        try:
            file.save(filepath)
        except Exception as save_error:
            app.logger.error(f'File save error: {str(save_error)}')
            return jsonify({
                'error': f'Failed to save file: {str(save_error)}',
                'success': False
            }), 500
        
        # Verify file was saved
        if not os.path.exists(filepath):
            return jsonify({
                'error': 'File was not saved properly',
                'success': False
            }), 500
        
        file_size = os.path.getsize(filepath)
        
        # Save to database
        file_record = FileRecord(
            filename=filename,
            original_filename=original_filename,
            file_type=file_type,
            file_size=file_size,
            file_path=filepath,
            status='uploaded'
        )
        
        try:
            db.session.add(file_record)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'{file_type.capitalize()} file uploaded successfully',
                'file': file_record.to_dict()
            }), 200
        except Exception as db_error:
            db.session.rollback()
            app.logger.error(f'Database error: {str(db_error)}')
            # Try to clean up file if database fails
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
            return jsonify({
                'error': f'Database error: {str(db_error)}',
                'success': False
            }), 500
            
    except Exception as e:
        app.logger.error(f'Upload error: {str(e)}', exc_info=True)
        return jsonify({
            'error': f'Upload failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is running',
        'database': 'connected'
    }), 200

@app.route('/api/files', methods=['GET'])
def list_files():
    """List all uploaded files from database"""
    try:
        files = FileRecord.query.order_by(FileRecord.upload_date.desc()).all()
        return jsonify({
            'files': [file.to_dict() for file in files]
        }), 200
    except Exception as e:
        app.logger.error(f'List files error: {str(e)}')
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    """Get a specific file by ID"""
    try:
        file_record = FileRecord.query.get_or_404(file_id)
        return jsonify({'file': file_record.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a specific file from database and filesystem"""
    try:
        file_record = FileRecord.query.get_or_404(file_id)
        filepath = file_record.file_path
        
        # Delete from database (cascade will delete training history)
        db.session.delete(file_record)
        db.session.commit()
        
        # Delete from filesystem
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'success': True, 'message': 'File deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/train/<int:file_id>', methods=['POST'])
def train_file(file_id):
    """Train/process a file"""
    try:
        file_record = FileRecord.query.get_or_404(file_id)
        
        # Determine training type based on file type
        training_type_map = {
            'text': 'text_analysis',
            'image': 'image_processing',
            'audio': 'audio_analysis'
        }
        training_type = training_type_map.get(file_record.file_type, 'general_processing')
        
        # Create training history record
        training = TrainingHistory(
            file_id=file_id,
            training_type=training_type,
            training_status='processing',
            start_time=datetime.utcnow()
        )
        db.session.add(training)
        file_record.status = 'processing'
        db.session.commit()
        
        # Process file in background (simulated)
        start_time = time.time()
        
        # Process based on file type
        if file_record.file_type == 'text':
            result = process_text_file(file_record.file_path)
        elif file_record.file_type == 'image':
            result = process_image_file(file_record.file_path)
        elif file_record.file_type == 'audio':
            result = process_audio_file(file_record.file_path)
        else:
            result = {'success': False, 'error': 'Unknown file type'}
        
        processing_time = time.time() - start_time
        
        # Update training record
        training.end_time = datetime.utcnow()
        training.processing_time = processing_time
        training.result = json.dumps(result)
        
        if result.get('success'):
            training.training_status = 'completed'
            file_record.status = 'trained'
            if 'metadata' in result:
                file_record.metadata = json.dumps(result['metadata'])
        else:
            training.training_status = 'failed'
            training.error_message = result.get('error', 'Processing failed')
            file_record.status = 'error'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'File training completed',
            'training': training.to_dict(),
            'result': result,
            'structuredOutput': result.get('structuredOutput', '')
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/training-history/<int:file_id>', methods=['GET'])
def get_training_history(file_id):
    """Get training history for a specific file"""
    try:
        FileRecord.query.get_or_404(file_id)  # Check if file exists
        training_history = TrainingHistory.query.filter_by(file_id=file_id)\
            .order_by(TrainingHistory.start_time.desc()).all()
        
        return jsonify({
            'history': [t.to_dict() for t in training_history]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/training-history', methods=['GET'])
def get_all_training_history():
    """Get all training history"""
    try:
        training_history = TrainingHistory.query\
            .order_by(TrainingHistory.start_time.desc()).limit(50).all()
        
        return jsonify({
            'history': [t.to_dict() for t in training_history]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about files and training"""
    try:
        total_files = FileRecord.query.count()
        files_by_type = db.session.query(
            FileRecord.file_type,
            db.func.count(FileRecord.id)
        ).group_by(FileRecord.file_type).all()
        
        total_training = TrainingHistory.query.count()
        completed_training = TrainingHistory.query.filter_by(training_status='completed').count()
        
        return jsonify({
            'totalFiles': total_files,
            'filesByType': {ftype: count for ftype, count in files_by_type},
            'totalTraining': total_training,
            'completedTraining': completed_training
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Open browser automatically after a short delay
    def open_browser():
        time.sleep(1.5)  # Wait for server to start
        webbrowser.open('http://127.0.0.1:5000')
    
    print("\n" + "="*50)
    print("  AI File Processing Agent - Starting Server")
    print("="*50)
    print("\n  Server will start at: http://127.0.0.1:5000")
    if USE_SUPABASE:
        print("  Database: Supabase (PostgreSQL) - Cloud")
    else:
        print("  Database: SQLite (Local)")
    print("  Opening browser automatically...")
    print("  Press Ctrl+C to stop the server\n")
    print("="*50 + "\n")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=True, host='127.0.0.1', port=5000)
