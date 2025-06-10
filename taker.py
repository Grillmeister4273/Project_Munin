import sys
from picamera import PiCamera

def capture_image(filename="/munin/originalimage.png"):
    with PiCamera() as camera:
        camera.start_preview()
        # Allow the camera to adjust to lighting conditions
        camera.sleep(2)
        camera.capture(filename)
        camera.stop_preview()
        print(f"Image saved as {filename}")

if __name__ == "__main__":
    # Get the filename from command-line arguments or use the default
    filename = sys.argv[1] if len(sys.argv) > 1 else "/munin/originalimage.png"
    if not filename.endswith(".png"):
        print("Error: Filename must end with '.png'")
    else:
        capture_image(filename)
