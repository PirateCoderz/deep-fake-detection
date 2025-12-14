"""
Security utilities for input sanitization and validation.
"""
import re
import html
from typing import Optional


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for storage
    """
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename


def sanitize_text_input(text: Optional[str], max_length: int = 500) -> Optional[str]:
    """
    Sanitize text input to prevent XSS attacks.
    
    Args:
        text: User input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text or None
    """
    if text is None:
        return None
    
    # Escape HTML entities
    text = html.escape(text.strip())
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text if text else None


def validate_image_content(content: bytes) -> tuple[bool, Optional[str]]:
    """
    Validate image file content to ensure it's actually an image.
    
    Args:
        content: File content bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check minimum size
    if len(content) < 100:
        return False, "File too small to be a valid image"
    
    # Check magic bytes for common image formats
    magic_bytes = {
        b'\xFF\xD8\xFF': 'JPEG',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'RIFF': 'WEBP',  # Needs additional check
    }
    
    for magic, format_name in magic_bytes.items():
        if content.startswith(magic):
            # Additional check for WEBP
            if format_name == 'WEBP' and b'WEBP' not in content[:20]:
                continue
            return True, None
    
    return False, "File does not appear to be a valid image format"


def validate_request_id(request_id: str) -> bool:
    """
    Validate request ID format (UUID).
    
    Args:
        request_id: Request ID to validate
        
    Returns:
        True if valid UUID format
    """
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(request_id))
