"""
Utility functions shared across blueprints
"""
import os
from werkzeug.utils import secure_filename

# Default upload directory - configurable via environment variable
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', '/tmp/datas_uploads')

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file, prefix=''):
    """
    Save an uploaded file to the configured upload directory
    
    Args:
        file: FileStorage object from request.files
        prefix: Optional prefix for the filename
        
    Returns:
        str: Full path to the saved file
        
    Raises:
        ValueError: If file is None or has no filename
    """
    if file is None or file.filename == '':
        raise ValueError("No file provided")
    
    filename = secure_filename(file.filename)
    if prefix:
        filename = f"{prefix}_{filename}"
    
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    
    return filepath


def read_tags_in_batches(comm, tags_list, batch_size=10):
    """
    Read PLC tags in batches to avoid errors from reading too many at once
    
    Args:
        comm: PLC communication object with Read() method
        tags_list: List of tag names to read
        batch_size: Maximum tags to read per batch (default: 10)
        
    Returns:
        list: Combined list of all read values
    """
    total = len(tags_list)
    complete_batches, remainder = divmod(total, batch_size)
    
    values = []
    for batch_number in range(complete_batches):
        start = batch_number * batch_size
        end = start + batch_size
        values.extend(comm.Read(tags_list[start:end]))
    
    # Read remaining tags if any
    if remainder > 0:
        start = complete_batches * batch_size
        values.extend(comm.Read(tags_list[start:start + remainder]))
    
    return values
