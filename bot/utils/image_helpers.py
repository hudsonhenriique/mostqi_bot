from PIL import Image
import io
import base64

def compress_and_encode_image(image_path, quality=70, max_size=(800, 800)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)  
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality)
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
