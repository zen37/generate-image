# stability.py

import base64
import requests
import os, logging

from interface import ImageInterface
from utils import get_api_key
from constants import IMAGE_SERVICE

class StabilityImageService(ImageInterface):
    def __init__(self, config):
        self.api_key = get_api_key(IMAGE_SERVICE)

    def create(self, text):
        url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        #logging.info("endpoint: %s", url)

        body = {
            "steps": 40,
            "width": 512,
            "height": 512,
            "seed": 0,
            "cfg_scale": 5,
            "samples": 1,
            "text_prompts": [
                {
                    "text": f'{text}',
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

        # make sure the out directory exists
        if not os.path.exists("./out"):
            os.makedirs("./out")

        for i, image in enumerate(data["artifacts"]):
            with open(f'./files/images/stability_{image["seed"]}.png', "wb") as f:
                f.write(base64.b64decode(image["base64"]))
