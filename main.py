import logging, argparse

from factory import get_image_instance
from utils import configure_logging, load_environment_variables, get_config, get_config_prompt, generate_unique_id

from constants import FILE_NAME_SEP, LOG_SEP

def create_image(correlation_id, prompt, filename_prefix):

    config = get_config()
    image = get_image_instance(config)
    image.create(correlation_id, prompt, filename_prefix)


def init():
    configure_logging()
    load_environment_variables()


def main():
    try:
        correlation_id = generate_unique_id()
        init()
        parser = argparse.ArgumentParser(description='Create greeting card image.')

        parser.add_argument('name', default='', nargs='?', help='Name to be included in the greeting card')
        parser.add_argument('background', default=[], nargs='*', help='Background theme for the greeting card image')
        parser.add_argument('-f', help='Filename')
        parser.add_argument('-p', help='Full prompt for the image')

        args = parser.parse_args()

        # If -p is provided, use it; otherwise, build the prompt from the json file
        if args.p:
            text_prompt = args.p
        else:
            # Use prompt data from _prompt.json
            prompt_data = get_config_prompt()
            text_prompt = prompt_data["text"].format(args.name, ' '.join(args.background))
            name = args.name

        # Use the provided or generated arguments
        prefix = args.f if args.f else FILE_NAME_SEP.join(name.split())
        prefix_filename = FILE_NAME_SEP.join([correlation_id, prefix])

        logging.info(f"{correlation_id}{LOG_SEP}{text_prompt}")
        create_image(correlation_id, text_prompt, prefix_filename)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()