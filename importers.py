from pathlib import Path
from PIL import Image

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
TEXT_EXTS = {".txt", ".csv", ".json"}
DOC_EXTS = {".docx"}
PDF_EXTS = {".pdf"}

def supported(path):
    return Path(path).suffix.lower() in IMAGE_EXTS | TEXT_EXTS | DOC_EXTS | PDF_EXTS

def image_size(path):
    with Image.open(path) as im:
        return im.size
