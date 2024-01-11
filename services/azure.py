# azure.py

import logging
import json
import requests

from openai import AzureOpenAI

from constants import IMAGE_SERVICE, TIMEOUT_SECONDS
from services.azure_constants import DEFAULT_IMAGE_QUALITY, DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_STYLE
from interface import ImageInterface
from utils import get_api_key, save, display_image

class AzureImageService(ImageInterface):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            api_version=self.config["api_version_image"],
            api_key=get_api_key(IMAGE_SERVICE),
            azure_endpoint=self.config["endpoint"],
        )

    def _generate_image(self, prompt):
        image_size = self.config.get("image_size", DEFAULT_IMAGE_SIZE)
        image_quality = self.config.get("image_quality", DEFAULT_IMAGE_QUALITY)
        image_style = self.config.get("image_style", DEFAULT_IMAGE_STYLE)

        try:
            result = self.client.images.generate(
                model=self.config["model_image"],
                prompt=prompt,
                n=1,
                size=image_size,
                quality=image_quality,
                style=image_style
            )

            result_data = json.loads(result.model_dump_json())["data"]
            if not result_data:
                logging.error("Unexpected response format: Missing 'data' key.")
                return None

            image_url = result_data[0]["url"]
            if image_url is None:
                logging.error("Image URL is not available.")
                return None

            try:
                generated_image = requests.get(image_url, timeout=TIMEOUT_SECONDS).content
            except requests.exceptions.HTTPError as e:
                logging.error(f"HTTP error while downloading the image: {e}")
                return None
            except requests.exceptions.Timeout as e:
                logging.error(f"Timeout error while downloading the image: {e}")
                return None
            except requests.exceptions.RequestException as e:
                logging.error(f"Error downloading the image: {e}")
                return None

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {e}")
            return None

        return generated_image


    def _generate_images(self, prompt):
        image_size = self.config.get("image_size", DEFAULT_IMAGE_SIZE)
        image_quality = self.config.get("image_quality", DEFAULT_IMAGE_QUALITY)
        image_style = self.config.get("image_style", DEFAULT_IMAGE_STYLE)

        try:
            result = self.client.images.generate(
                model=self.config["model_image"],
                prompt=prompt,
                n=2,  # Change to 2 for generating two images
                size=image_size,
                quality=image_quality,
                style=image_style
            )

            result_data = json.loads(result.model_dump_json())["data"]
            if not result_data:
                logging.error("Unexpected response format: Missing 'data' key.")
                return None

            generated_images = []

            for item in result_data:
                image_url = item["url"]
                if image_url is not None:
                    try:
                        generated_image = requests.get(image_url, timeout=TIMEOUT_SECONDS).content
                        generated_images.append(generated_image)
                    except requests.exceptions.HTTPError as e:
                        logging.error(f"HTTP error while downloading the image: {e}")
                    except requests.exceptions.Timeout as e:
                        logging.error(f"Timeout error while downloading the image: {e}")
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Error downloading the image: {e}")

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {e}")
            return None

        return generated_images


    def create(self, prompt, filename_prefix):
        try:
            image = self._generate_image(prompt)
            if image:
                filename_middle = self.config['model_image']
                image_path = save(image, filename_prefix, filename_middle)
                if image_path:
                    display_image(image_path)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
