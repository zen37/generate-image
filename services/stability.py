# stability.py

import base64
import requests
import logging

from interface import ImageInterface
from utils import get_api_key, save, display_image
from constants import IMAGE_SERVICE
from services.stability_constants import DEFAULT_IMAGES_TO_GENERATE

class StabilityImageService(ImageInterface):
    def __init__(self, config):
        self.config = config
        self.api_key = get_api_key(IMAGE_SERVICE)


    def _generate_image(self, prompt):
        url = self.config["endpoint"]

        body = {
            "steps": 40,
            "width": 512,
            "height": 512,
            "seed": 0,
            "cfg_scale": 5,
            "samples": DEFAULT_IMAGES_TO_GENERATE,
            "text_prompts": [
                {
                    "text": f'{prompt}',
                    "weight": 1
                },
                {
                    "text": "blurry, bad",
                    "weight": -1
                }
            ],
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(url, headers=headers, json=body)
        logging.info("HTTP Request: POST %s, Response: HTTP/%s %d %s", url, response.raw.version, response.status_code, response.reason)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        if data is not None:
            generated_image = data["artifacts"][0] #because we ask only for one image
            return generated_image
        else:
            logging.info("data = response.json() is None")
            return None


    def create(self, prompt, filename_prefix):
        try:
            image = self._generate_image(prompt)
            if image:
                filename_middle = self.config['model_image']
                image_path = save(image, filename_prefix, filename_middle, True)
                if image_path:
                    display_image(image_path)
        except Exception as e:
            logging.error(f"An error occurred: {e}")