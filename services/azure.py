# azure.py

from openai import AzureOpenAI
import logging
import requests
from PIL import Image
import json

from interface import ImageInterface
from constants import (
    IMAGE_SERVICE, DEFAULT_IMAGE_QUALITY, DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_STYLE
)
from utils import get_api_key, get_image_path

class AzureImageService(ImageInterface):
    def __init__(self, config):
        self.config = config
        self.client = AzureOpenAI(
            api_version=self.config["api_version_image"],
            api_key=get_api_key(IMAGE_SERVICE),
            azure_endpoint=self.config["endpoint_image"],
        )

    def _generate_image_data(self, prompt):
        image_size = self.config.get("image_size", DEFAULT_IMAGE_SIZE)
        image_quality = self.config.get("image_quality", DEFAULT_IMAGE_QUALITY)
        image_style = self.config.get("image_style", DEFAULT_IMAGE_STYLE)

        result = self.client.images.generate(
            model=self.config["model_image"],
            prompt=prompt,
            n=1,
            size=image_size,
            quality=image_quality,
            style=image_style
        )

        #print(result)
        return json.loads(result.model_dump_json())["data"][0]["url"]

    def _save_image(self, image_url, filename_prefix):

        filename_middle = self.config['model_image']
        image_path = get_image_path(filename_prefix, filename_middle)

        try:
            generated_image = requests.get(image_url).content
            with open(image_path, "wb") as image_file:
                image_file.write(generated_image)
        except requests.RequestException as e:
            logging.error(f"Error downloading the image: {e}")
            return None

        return image_path

    def _display_image(self, image_path):
        try:
            image = Image.open(image_path)
            image.show()
        except Exception as e:
            logging.error(f"Error opening the image: {e}")

    def create(self, prompt, filename_prefix):
        image_url = self._generate_image_data(prompt)
        if image_url:
            image_path = self._save_image(image_url, filename_prefix)
            if image_path:
                self._display_image(image_path)

        return image_path if image_path else None