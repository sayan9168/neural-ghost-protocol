import cv2
import numpy as np
from PIL import Image
from typing import Dict, Optional, Any
import os

class ImageValidator:
    """Validate images for steganography operations"""
    
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.error = None
        self.img = None
    
    def validate(self) -> bool:
        """
        Validate image for steganography
        
        Checks:
        - File exists
        - Valid image format
        - Sufficient size for data hiding
        - Color image (not grayscale)
        
        Returns:
            bool: True if valid
        """
        # Check file exists
        if not os.path.exists(self.image_path):
            self.error = "File does not exist"
            return False
        
        # Try to load image
        try:
            self.img = cv2.imread(self.image_path)
            if self.img is None:
                self.error = "Failed to load image - invalid format"
                return False
        except Exception as e:
            self.error = f"Error loading image: {str(e)}"
            return False
        
        # Check dimensions
        if self.img.shape[0] < 10 or self.img.shape[1] < 10:
            self.error = "Image too small for steganography"
            return False
        
        # Check if color image
        if len(self.img.shape) == 2:
            self.error = "Grayscale images not supported - use color images"
            return False
        
        return True
    
    def get_info(self) -> Dict[str, Any]:
        """Get image information"""
        if self.img is None:
            return {}
        
        return {
            'path': self.image_path,
            'width': self.img.shape[1],
            'height': self.img.shape[0],
            'channels': self.img.shape[2] if len(self.img.shape) > 2 else 1,
            'total_pixels': self.img.shape[0] * self.img.shape[1],
            'valid': self.validate()
        }


class MetadataHandler:
    """Handle image metadata extraction and analysis"""
    
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.img = None
        self._load_image()
    
    def _load_image(self):
        """Load image for metadata processing"""
        try:
            self.img = cv2.imread(self.image_path)
        except:
            self.img = None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive image statistics"""
        if self.img is None:
            return {'error': 'Failed to load image'}
        
        # Calculate capacity (assuming 1 bit per channel)
        total_bits = self.img.shape[0] * self.img.shape[1] * 3
        capacity_bytes = total_bits // 8
        
        # Estimate used capacity (simplified - would need actual analysis)
        # This is a placeholder for more sophisticated analysis
        used_capacity = 0.0  # Would require decoding to know actual usage
        
        return {
            'size': os.path.getsize(self.image_path),
            'dimensions': f"{self.img.shape[1]}x{self.img.shape[0]}",
            'format': 'PNG' if self.image_path.lower().endswith('.png') else 'JPEG',
            'color_mode': 'BGR' if len(self.img.shape) == 3 else 'Grayscale',
            'capacity_used': used_capacity,
            'max_capacity_bytes': capacity_bytes
        }
    
    def extract_exif(self) -> Dict[str, str]:
        """Extract EXIF metadata if available"""
        try:
            with Image.open(self.image_path) as img:
                exif_data = img._getexif()
                if not exif_data:
                    return {}
                
                # Map EXIF tags to readable names
                exif_mapping = {
                    271: 'Make',
                    272: 'Model',
                    306: 'DateTime',
                    256: 'ImageWidth',
                    257: 'ImageHeight',
                    34665: 'ExifOffset',
                    34853: 'GPSInfo',
                }
                
                result = {}
                for tag_id, value in exif_data.items():
                    tag_name = exif_mapping.get(tag_id, f'Tag_{tag_id}')
                    result[tag_name] = str(value)
                
                return result
        except Exception as e:
            return {}
    
    def analyze_histogram(self) -> Dict[str, list]:
        """Analyze color channel histograms"""
        if self.img is None:
            return {}
        
        histograms = {}
        colors = ['Blue', 'Green', 'Red']
        
        for i, color in enumerate(colors):
            if i < self.img.shape[2]:
                hist = cv2.calcHist([self.img], [i], None, [256], [0, 256])
                histograms[color] = hist.flatten().tolist()
        
        return histograms
    
    def detect_compression_artifacts(self) -> float:
        """Detect level of compression artifacts (0-1 scale)"""
        if self.img is None:
            return 0.0
        
        # Simple metric: variance in smooth regions
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Higher edge density might indicate compression artifacts
        edge_ratio = np.sum(edges > 0) / edges.size
        return min(1.0, edge_ratio * 10)
