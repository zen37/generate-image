import os, uuid
import logging
import json
#import inspect
from datetime import datetime
import base64
from PIL import Image


from constants import (
    ENCODING, DIR_CONFIG, FILE_COMMON_CONFIG,
    DEFAULT_LOG_DIR, DEFAULT_LOG_FILE_NAME,
    SERVICES, SERVICE_KEY_MAPPING,
    DIR_IMAGES, FORMAT_TIME, FILE_IMAGE_EXT, FILE_NAME_SEP
)

def generate_unique_id():
    """generates unique id"""
    return str(uuid.uuid4())


def configure_logging():
    """configures logging based on configuration"""
    config = get_config()
    log_dir = config.get("log_dir", DEFAULT_LOG_DIR)
    log_file = config.get("log_file", DEFAULT_LOG_FILE_NAME)
    log_file_path = os.path.join(log_dir, log_file)

    handlers = [
        logging.StreamHandler(), #if config.get("logging_to_console", True) else None,
        logging.FileHandler(log_file_path)  # Always add FileHandler
    ]

    handlers = [handler for handler in handlers if handler is not None]

    logging.basicConfig(
        level=config.get("log_level", logging.INFO),
        format=config.get("log_format", "%(asctime)s [%(levelname)s]: %(message)s"),
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )

'''
def log_function_call(func):
    def wrapper(*args, **kwargs):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(f"Function {func.__name__} called by {caller} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper
'''

def get_config():
    """reads common configuration file"""
    config_path = os.path.join(DIR_CONFIG, FILE_COMMON_CONFIG)
    return _open_file(config_path)

def get_config_prompt():
    """reads prompt configuration file"""
    config_prompt_path = os.path.join('config', '_prompt.json')
    return _open_file(config_prompt_path )


def _open_file(path):
    """reads file file"""
    try:
        with open(path, "r", encoding=ENCODING) as file:
            result = json.load(file)

        return result
    except FileNotFoundError as e:
        logging.error("File %s not found: %s", path, e)
        # You might choose to return a default configuration or raise the exception depending on your use case.
        return {}
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON in file %s : %s", path, e)
        # Handle the error, e.g., return a default configuration or raise the exception.
        return {}
    except Exception as e:
        logging.error("Unexpected error reading file %s: %s", path, e)
        # Handle the error, e.g., return a default configuration or raise the exception.
        return {}


def get_config_service(provider):
    file_config = provider + ".json"

    config_path = os.path.join(DIR_CONFIG, file_config )

    with open(config_path, "r", encoding = ENCODING) as file:
        config = json.load(file)
    return config


def load_environment_variables():
    """loads environment variables based on the service used for each functionality: text, speech, video"""
    config = get_config()

    for service in SERVICES:
        service_provider = config.get(service, "")
        dotenv_path = os.path.join('./env', f'{service_provider.lower()}.env')
        #logging.info('%s uses %s', service, service_provider)

        try:
            with open(dotenv_path, encoding=ENCODING) as f:
                for line in f:
                    key, value = line.strip().split('=', 1)
                    if service in SERVICE_KEY_MAPPING and key == SERVICE_KEY_MAPPING[service]:
                        os.environ[key] = value

        except FileNotFoundError as e:
            logging.error("Environment file not found for %s: %s", service, e)
        except ValueError as e:
            logging.error("Error processing environment file for %s: %s", service, e)
        except Exception as e:
            logging.error("Unexpected error for %s: %s", service, e)

def get_api_key(service):
    key = os.getenv(SERVICE_KEY_MAPPING[service])
    return key


def construct_filename(filename_prefix, filename_middle):
    timestamp = datetime.now().strftime(FORMAT_TIME)
    filename = f"{filename_prefix}{FILE_NAME_SEP}{filename_middle}{FILE_NAME_SEP}{timestamp}.{FILE_IMAGE_EXT}"
    return filename


def get_file_path(filename_prefix, filename_middle):

    filename = construct_filename(filename_prefix, filename_middle)
    folder = os.path.join(DIR_IMAGES)

    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, filename)


def save(image, filename_prefix, filename_middle, Base64encoding=None):

    image_path = get_file_path(filename_prefix, filename_middle)

    try:
        with open(image_path, "wb") as image_file:
            if Base64encoding:
                image = image_file.write(base64.b64decode(image["base64"]))
            else:
                image_file.write(image)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

    return image_path


def display_image(image_path):
    try:
        image = Image.open(image_path)
        image.show()
    except Exception as e:
        logging.error(f"Error opening the image: {e}")
