import os, logging, argparse, json

from factory import get_image_instance
from utils import configure_logging, load_environment_variables, get_config

from constants import FILE_NAME_SEP

def create_image(prompt, filename_prefix):

    config = get_config()
    image = get_image_instance(config)
    image.create(prompt, filename_prefix)

def init():
    configure_logging()
    load_environment_variables()


def main():
    try:
        init()
        parser = argparse.ArgumentParser(description='Create greeting card image.')

        # Get the path to the _prompt.json file in the config directory
        prompt_file_path = os.path.join('config', '_prompt.json')

        # Load prompts from _prompt.json
        with open(prompt_file_path, 'r') as prompt_file:
            prompt_data = json.load(prompt_file)

        parser.add_argument('name', help='Name to be included in the greeting card')
        parser.add_argument('background', nargs='+', help='Background theme for the greeting card image')

        args = parser.parse_args()

        args = parser.parse_args()
        #print(f"Received arguments: {args}")

        # Use prompt data from _prompt.json
        text_prompt = prompt_data["text"].format(args.name, ' '.join(args.background))
        prefix_filename = FILE_NAME_SEP.join(args.name.split())
        #logging.info(f"prefix_filename: {prefix_filename}")
        #return
        logging.info(f"prompt: {text_prompt}")
        create_image(text_prompt, prefix_filename)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()