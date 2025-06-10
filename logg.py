# logg.py
# This script defines a decorator to log exceptions and retry a function
# a specified number of times. It uses the logging module to log messages
# to a file. The decorator can be applied to any function, and it will
# log the function name, the attempt number, and any exceptions that occur.
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    filename='/home/moe/munin/logs/error.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_and_retry(retries=3):
    """
    Decorator to log exceptions and retry a function up to a specified number of times.

    Parameters:
        retries (int): Number of retry attempts before giving up.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    logging.info(f"Attempt {attempts + 1} for function {func.__name__}.")
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logging.error(f"Error in {func.__name__} on attempt {attempts}: {e}")
                    if attempts >= retries:
                        logging.error(f"Function {func.__name__} failed after {retries} attempts.")
                        raise
        return wrapper
    return decorator
