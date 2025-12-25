from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class FileRecord(db.Model):
    """Database model for uploaded files"""
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # text, image, audio
    file_size = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), default='uploaded')  # uploaded, processing, trained, error
    metadata = db.Column(db.Text)  # JSON string for additional metadata
    
    # Relationship to training history
    training_history = db.relationship('TrainingHistory', backref='file_record', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'fileType': self.file_type,
            'fileSize': self.file_size,
            'filePath': self.file_path,
            'uploadDate': self.upload_date.isoformat() if self.upload_date else None,
            'status': self.status,
            'metadata': self.metadata,
            'trainingCount': len(self.training_history)
        }

class TrainingHistory(db.Model):
    """Database model for training/processing history"""
    __tablename__ = 'training_history'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    training_type = db.Column(db.String(100), nullable=False)  # text_analysis, image_processing, audio_analysis
    training_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime)
    result = db.Column(db.Text)  # JSON string for training results
    error_message = db.Column(db.Text)
    processing_time = db.Column(db.Float)  # Processing time in seconds
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'fileId': self.file_id,
            'trainingType': self.training_type,
            'status': self.training_status,
            'startTime': self.start_time.isoformat() if self.start_time else None,
            'endTime': self.end_time.isoformat() if self.end_time else None,
            'result': self.result,
            'errorMessage': self.error_message,
            'processingTime': self.processing_time
        }

