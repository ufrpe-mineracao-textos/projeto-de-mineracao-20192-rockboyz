# pacman -S tesseract
# pacman -S tesseract-data-eng
# pip install Pillow
# pip install pytesseract

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def img2txt(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

print(img2txt('001.png'))