import locale
import os
import logging
from dotenv import load_dotenv
import json
import inspect


from constants import (
    ENCODING, DIR_CONFIG, FILE_COMMON_CONFIG,
    SERVICES, SERVICE_KEY_MAPPING
)


def configure_logging():
    """configures logging based on configuration"""
    config = get_config()

    handlers = [
        logging.StreamHandler(), #if config.get("logging_to_console", True) else None,
        logging.FileHandler("log.txt")  # Always add FileHandler
    ]

    handlers = [handler for handler in handlers if handler is not None]

    logging.basicConfig(
        level=config.get("logging_level", logging.INFO),
        format=config.get("logging_format", "%(asctime)s [%(levelname)s]: %(message)s"),
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )


def log_function_call(func):
    def wrapper(*args, **kwargs):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(f"Function {func.__name__} called by {caller} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

def get_config():
    """reads common configuration file"""
    config_path = os.path.join(DIR_CONFIG, FILE_COMMON_CONFIG)
    try:
        with open(config_path, "r", encoding=ENCODING) as file:
            config = json.load(file)
        return config
    except FileNotFoundError as e:
        logging.error("Configuration file not found: %s", e)
        # You might choose to return a default configuration or raise the exception depending on your use case.
        return {}
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON in configuration file: %s", e)
        # Handle the error, e.g., return a default configuration or raise the exception.
        return {}
    except Exception as e:
        logging.error("Unexpected error reading configuration file: %s", e)
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
        logging.info('%s uses %s', service, service_provider)

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