import os 
import logging
logger = logging.getLogger(__name__)

def load():
    """
    Load environment variables from .env file.
    This was written as an exercise to learn about environment variables.
    app is configured to use python-dotenv to load environment variables.
    """
    try:
        with open('.env', 'r') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
    except FileNotFoundError:
        logging.error("No .env file found. Continuing without loading environment variables.")
    except ValueError:
        logging.error(f"Error: Incorrect formatting in .env file on line: {line}. Expected format: KEY=VALUE")
            