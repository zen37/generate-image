#common
SERVICE_AZURE = "azure"
SERVICE_STABILITY = "stability"

IMAGE_SERVICE       = "image_service"

SERVICES = [IMAGE_SERVICE]

SERVICE_KEY_MAPPING = {
    IMAGE_SERVICE: "API_KEY_IMAGE",
}

DIR_CONFIG = "config"
FILE_COMMON_CONFIG = "_config.json"
FILE_AZURE_CONFIG = "azure.json"

#FORMAT_TIME = "%Y%m%d%H%M%S"
FORMAT_TIME = "%Y%m%d%H%M"

#text

EMOJI_ENCODINGS = ('UTF-8', 'UTF-16', 'UTF-32')

ENCODING = 'UTF-8'

TIMEOUT_SECONDS = 10 #for calling translator resource

#images
DIR_IMAGES = 'files/images'
FILE_NAME_SEP = '_'
FILE_IMAGE_EXT  = 'png'


# supported values are “1792x1024”, “1024x1024” and “1024x1792”
DEFAULT_IMAGE_SIZE = '1024x1024'
# options are “hd” and “standard”; defaults to standard
DEFAULT_IMAGE_QUALITY = 'standard'
# options are “natural” and “vivid”; defaults to “vivid”
DEFAULT_IMAGE_STYLE = 'natural'