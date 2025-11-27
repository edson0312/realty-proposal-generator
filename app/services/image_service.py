"""Service for handling image operations including collage generation."""
import os
import tempfile
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from werkzeug.datastructures import FileStorage


class ImageService:
    """Service class for image operations."""
    
    def __init__(self, output_folder: str = "uploads"):
        """
        Initialize image service.
        
        Args:
            output_folder: Directory to save processed images
        """
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def process_uploaded_images(self, files: List[FileStorage]) -> Optional[str]:
        """
        Process uploaded images. If multiple images, create a collage.
        If single image, save it directly.
        
        Args:
            files: List of uploaded image files
            
        Returns:
            Path to processed image file or None if no valid images
        """
        if not files:
            return None
        
        # Filter valid image files and remove duplicates
        valid_files = []
        seen_filenames = set()
        
        for file in files:
            if file and file.filename and self._is_valid_image(file):
                # Skip duplicate filenames
                if file.filename not in seen_filenames:
                    valid_files.append(file)
                    seen_filenames.add(file.filename)
        
        if not valid_files:
            return None
        
        # Limit to 4 images maximum
        valid_files = valid_files[:4]
        
        # Always use collage creation for consistent formatting
        return self._create_collage(valid_files)
    
    def _is_valid_image(self, file: FileStorage) -> bool:
        """Check if file is a valid image."""
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if '.' not in file.filename:
            return False
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        return ext in allowed_extensions
    
    def _save_single_image(self, file: FileStorage) -> str:
        """Save a single image file."""
        # Create temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg', dir=self.output_folder)
        os.close(temp_fd)
        
        try:
            # Open and process image
            image = Image.open(file.stream)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (max 1200px on longest side)
            image = self._resize_image(image, max_size=1200)
            
            # Save as JPEG
            image.save(temp_path, 'JPEG', quality=85, optimize=True)
            
            return temp_path
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    def _create_collage(self, files: List[FileStorage]) -> str:
        """Create a collage from multiple images."""
        # Create temporary file for collage
        temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg', dir=self.output_folder)
        os.close(temp_fd)
        
        try:
            # Load and process images
            images = []
            for file in files:
                try:
                    # Reset file stream position to beginning
                    file.stream.seek(0)
                    img = Image.open(file.stream)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    images.append(img)
                except Exception:
                    continue  # Skip invalid images
            
            if not images:
                raise ValueError("No valid images to create collage")
            
            # Create collage based on number of images
            collage = self._arrange_images(images)
            
            # Save collage
            collage.save(temp_path, 'JPEG', quality=85, optimize=True)
            
            return temp_path
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    def _arrange_images(self, images: List[Image.Image]) -> Image.Image:
        """Arrange images into a collage layout matching the specified formats."""
        num_images = len(images)
        
        # Define collage dimensions
        collage_width = 800
        collage_height = 600
        
        if num_images == 1:
            # Single image - full size, centered
            img = self._resize_to_fit(images[0], collage_width, collage_height)
            collage = Image.new('RGB', (collage_width, collage_height), 'white')
            x_offset = (collage_width - img.width) // 2
            y_offset = (collage_height - img.height) // 2
            collage.paste(img, (x_offset, y_offset))
            
        elif num_images == 2:
            # Side by side layout - equal width
            img_width = collage_width // 2
            img_height = collage_height
            
            # Resize images to fit their allocated space
            left_img = self._resize_to_fit(images[0], img_width, img_height)
            right_img = self._resize_to_fit(images[1], img_width, img_height)
            
            # Create collage
            collage = Image.new('RGB', (collage_width, collage_height), 'white')
            
            # Center images in their halves
            left_x = (img_width - left_img.width) // 2
            left_y = (collage_height - left_img.height) // 2
            right_x = img_width + (img_width - right_img.width) // 2
            right_y = (collage_height - right_img.height) // 2
            
            collage.paste(left_img, (left_x, left_y))
            collage.paste(right_img, (right_x, right_y))
            
        elif num_images == 3:
            # Top row: 2 images side by side, Bottom row: 1 image full width
            top_height = collage_height // 2
            bottom_height = collage_height // 2
            top_img_width = collage_width // 2
            
            # Resize top images
            top_left = self._resize_to_fit(images[0], top_img_width, top_height)
            top_right = self._resize_to_fit(images[1], top_img_width, top_height)
            
            # Resize bottom image to full width
            bottom_img = self._resize_to_fit(images[2], collage_width, bottom_height)
            
            # Create collage
            collage = Image.new('RGB', (collage_width, collage_height), 'white')
            
            # Position top images
            top_left_x = (top_img_width - top_left.width) // 2
            top_left_y = (top_height - top_left.height) // 2
            top_right_x = top_img_width + (top_img_width - top_right.width) // 2
            top_right_y = (top_height - top_right.height) // 2
            
            collage.paste(top_left, (top_left_x, top_left_y))
            collage.paste(top_right, (top_right_x, top_right_y))
            
            # Position bottom image
            bottom_x = (collage_width - bottom_img.width) // 2
            bottom_y = top_height + (bottom_height - bottom_img.height) // 2
            
            collage.paste(bottom_img, (bottom_x, bottom_y))
            
        elif num_images >= 4:
            # 2x2 grid layout
            img_width = collage_width // 2
            img_height = collage_height // 2
            
            # Use only first 4 images
            grid_images = images[:4]
            
            # Create collage
            collage = Image.new('RGB', (collage_width, collage_height), 'white')
            
            # Position images in 2x2 grid
            positions = [
                (0, 0),  # Top left
                (1, 0),  # Top right
                (0, 1),  # Bottom left
                (1, 1)   # Bottom right
            ]
            
            for i, (img, (col, row)) in enumerate(zip(grid_images, positions)):
                # Resize image to fit in quadrant
                resized_img = self._resize_to_fit(img, img_width, img_height)
                
                # Calculate position
                x = col * img_width + (img_width - resized_img.width) // 2
                y = row * img_height + (img_height - resized_img.height) // 2
                
                collage.paste(resized_img, (x, y))
        
        return collage
    
    def _resize_image(self, image: Image.Image, max_size: int) -> Image.Image:
        """Resize image maintaining aspect ratio."""
        width, height = image.size
        
        if width <= max_size and height <= max_size:
            return image
        
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _resize_to_fit(self, image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Resize image to fit within target dimensions while maintaining aspect ratio."""
        width, height = image.size
        
        # Calculate scaling factor
        scale_w = target_width / width
        scale_h = target_height / height
        scale = min(scale_w, scale_h)
        
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
