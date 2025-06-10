import os
import sys
from difflib import SequenceMatcher
from logg import log_and_retry
import logging

# Configure logging
logging.basicConfig(
    filename='/home/moe/munin/logs/textcf.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@log_and_retry(retries=3)
def calculate_similarity(text1, text2):
    """
    Calculates the similarity between two texts in percentage.

    The similarity is calculated using the SequenceMatcher's ratio method:
    ratio = (2 * M) / T
    where:
    - M is the number of matches (characters that are the same and in the same order in both texts).
    - T is the total number of characters in both texts combined.

    The result is multiplied by 100 to convert it into a percentage.
    """
    logging.info("Calculating similarity between extracted and ground-truth text.")
    return SequenceMatcher(None, text1, text2).ratio() * 100

@log_and_retry(retries=3)
def load_gt_text(prozid):
    """
    Loads the ground-truth text from the file ./gt/gt(prozid).
    """
    logging.info(f"Loading ground-truth text for process ID: {prozid}")
    gt_path = f"./gt/gt{prozid}" # Adjusted to use f-string for clarity
    with open(gt_path, 'r', encoding='utf-8') as file:
        return file.read()

@log_and_retry(retries=3)
def main():
    """
    Main function that compares the text from reader.py with the ground-truth text.
    """
    logging.info("Starting text comparison.")
    if len(sys.argv) < 3:
        sys.exit(1)

    # Retrieve the process ID and similarity threshold from command-line arguments
    prozid = sys.argv[1]
    similarity_threshold = float(sys.argv[2])

    # Load text from reader.py
    with open('temp.txt', 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    # Load ground-truth text
    gt_text = load_gt_text(prozid)

    # Calculate similarity
    similarity = calculate_similarity(extracted_text.strip(), gt_text.strip())

    logging.info(f"Similarity: {similarity:.2f}% (Threshold: {similarity_threshold}%)")

    # Result based on similarity
    if similarity >= similarity_threshold:
        logging.info("Similarity threshold met. Passing status_id 1 to taskmanager.py.")
        os.system("python3 taskmanager.py 1")
    else:
        logging.warning("Similarity threshold not met. Passing status_id 0 to taskmanager.py.")
        os.system("python3 taskmanager.py 0")

if __name__ == "__main__":
    main()