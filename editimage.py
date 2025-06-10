# imgedit.py

import sys
sys.path.insert(0, '/home/cam/munin/tools') # still needed?
cv2 = Path('/home/cam/munin/tools/munin/opencv2')
import subprocess
from logg import log_and_retry
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='/home/cam/munin/logs/editimage.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@log_and_retry(retries=3)
def process_image(input_path='/home/cam/munin/originalimage.png',
                  output_path='/home/cam/munin/editedimage.png',
                  binarise=False,
                  grayscale=False,
                  remove_noise=False,
                  noise_kernel_size=3,
                  crop_coords=None,
                  text=False):
    """
    Loads an image, applies various edits, and saves the result.

    Parameters:
        input_path (str): The path to the input image.
        output_path (str): The path to the output image.
        binarise (bool): Whether to binarize the image.
        grayscale (bool): Whether to convert the image to grayscale.
        remove_noise (bool): Whether to remove noise.
        noise_kernel_size (int): The kernel size for noise reduction.
        crop_coords (tuple): The coordinates for cropping the image (x1, y1, x2, y2).
        text (bool): Whether to pass the image to reader.py.
    """

    logging.info(f"Processing image: {input_path}")

    img = cv2.imread(input_path)
    processed_img = img.copy()

    if crop_coords:
        logging.info(f"Cropping image with coordinates: {crop_coords}")
        x1, y1, x2, y2 = map(int, crop_coords)
        processed_img = processed_img[y1:y2, x1:x2]
    
    if grayscale or binarise:
        if len(processed_img.shape) == 3 and processed_img.shape[2] == 3:
            logging.info("Converting image to grayscale.")
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)

    if remove_noise:
        logging.info(f"Removing noise with kernel size: {noise_kernel_size}")
        processed_img = cv2.medianBlur(processed_img, noise_kernel_size)

    if binarise:
        logging.info("Binarising image.")
        _, processed_img = cv2.threshold(processed_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    logging.info(f"Saving processed image to: {output_path}")
    cv2.imwrite(output_path, processed_img)

    # Pass the image to the appropriate script
    if text:
        logging.info("Passing image to reader.py.")
        subprocess.run(["python3", "/home/cam/munin/tools/opencv2/reader.py", output_path])
    else:
        logging.info("Passing image to pngcf.py.")
        subprocess.run(["python3", "/home/cam/munin/tools/opencv2/pngcf.py", output_path])