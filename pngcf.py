import os
import sys
from logg import log_and_retry
import logging

# Configure logging
logging.basicConfig(
    filename='/home/moe/munin/logs/pngcf.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@log_and_retry(retries=3)
def main():
    """
    Main function to pass status_id to taskmanager.py.
    """
    logging.info("Starting PNG comparison.")
    if len(sys.argv) < 2:
        sys.exit(1)

    status_id = int(sys.argv[1])  # Accept status_id as an argument
    if status_id in [0, 1, 2]:
        logging.info(f"Passing status_id {status_id} to taskmanager.py.")
        os.system(f"python3 taskmanager.py {status_id}")
    else:
        logging.error(f"Invalid status_id {status_id}. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
