# taskmanager.py
import subprocess
import editimage
import time
import yaml
from logg import log_and_retry
import logging
import negotiator
import picamera

# Configure logging
logging.basicConfig(
    filename='/home/cam/munin/logs/taskmanager.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load image_params from YAML file
with open('/home/cam/munin/gt/image_params.yaml', 'r') as file:
    image_params = yaml.safe_load(file)['image_params']

# Counter that tracks the current image index
current_image_index = 0

# Initialize false_counter
false_counter = 0

# Initialize the camera
camera = picamera.PiCamera()

@log_and_retry(retries=3)
def process_next_image():
    global current_image_index, false_counter
    logging.info(f"Starting processing for image index: {current_image_index}")
    false_counter = 0  # Reset false_counter

    try:
        # Capture the image using rpicam
        image_path = f"/home/cam/munin/gt/gt{current_image_index:03d}/captured_image.jpg"
        camera.capture(image_path)
        logging.info(f"Image captured and saved to {image_path}")

        # Get the parameters for the current image
        params_for_editing = image_params[current_image_index]

        # Call the function from imgedit.py
        editimage.process_image(
            binarise=params_for_editing['binarise'],
            grayscale=params_for_editing['grayscale'],
            remove_noise=params_for_editing['remove_noise'],
            noise_kernel_size=params_for_editing['noise_kernel_size'],
            crop_coords=params_for_editing['crop_coords'],
            text=params_for_editing['text']
        )

        # Pass the processed image to the corresponding script
        subprocess.run(["python3", "pngcf.py"])

        logging.info(f"Image {current_image_index} processed successfully.")
        # Increment the counter
        current_image_index += 1
    except Exception as e:
        logging.error(f"Error processing image {current_image_index}: {e}")
        raise

    else:  # If "False" is returned
        false_counter += 1
        logging.warning(f"Retrying image {current_image_index}, false_counter: {false_counter}")

        if false_counter == 1:
            # Execute the same step again
            editimage.process_image(
                binarise=params_for_editing['binarise'],
                grayscale=params_for_editing['grayscale'],
                remove_noise=params_for_editing['remove_noise'],
                noise_kernel_size=params_for_editing['noise_kernel_size'],
                crop_coords=params_for_editing['crop_coords'],
                text=params_for_editing['text']
            )
        elif false_counter == 2:
            # Check for ID 99
            params_for_editing = next((p for p in image_params if p['id'] == 99), None)
            if params_for_editing:
                editimage.process_image(
                    binarise=params_for_editing['binarise'],
                    grayscale=params_for_editing['grayscale'],
                    remove_noise=params_for_editing['remove_noise'],
                    noise_kernel_size=params_for_editing['noise_kernel_size'],
                    crop_coords=params_for_editing['crop_coords'],
                    text=params_for_editing['text']
                )
                # Add logic to send status_id=2 if false_counter == 3
                if false_counter == 3:
                    negotiator.send_status(status_id=2)