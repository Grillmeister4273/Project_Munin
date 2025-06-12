# reader.py

import os
import pytesseract
from PIL import Image
from logg import log_and_retry
import logging

# Path to Tesseract installation (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Configure logging
logging.basicConfig(
    filename='/home/moe/munin/reader.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@log_and_retry(retries=3)
def get_image():
    """
    Load the processed image from the specified path.
    """
    image_path = '/home/cam/munin/imgedit_output.png'  # Standard path of the processed image
    logging.info(f"Loading image from {image_path}")
    return Image.open(image_path)
    
@log_and_retry(retries=3)
def extract_text(image):
    """
    Extract text from the given image using Tesseract OCR.
    """
    logging.info("Extracting text from image using Tesseract OCR.")
    text = pytesseract.image_to_string(image, lang='deu')  # Adjust language if necessary
    return text

@log_and_retry(retries=3)
def save_text_to_file(text):
    """
    Save the extracted text to a temporary file.
    """
    text = "\n".join([line for line in text.splitlines() if line.strip()])
    logging.info("Saving extracted text to temp.txt.")
    with open('temp.txt', 'w') as file:
        file.write(text)

# Pass text to textcf.py script
def pass_text_to_script():
    logging.info("Passing text to textcf.py script.")
    os.system('python3 /home/cam/munin/textcf.py temp.txt')

