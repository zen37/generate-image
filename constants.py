#common
SERVICE_AZURE = "azure"
SERVICE_STABILITY = "stability"

IMAGE_SERVICE = "image_service"

SERVICES = [IMAGE_SERVICE]

SERVICE_KEY_MAPPING = {
    IMAGE_SERVICE: "API_KEY_IMAGE",
}

DIR_CONFIG = "config"
FILE_COMMON_CONFIG = "_config.json"

#FORMAT_TIME = "%Y%m%d%H%M%S"
FORMAT_TIME = "%Y%m%d%H%M"

ENCODING = 'UTF-8'

# HTTP request timeout
TIMEOUT_SECONDS = 10

#images
DIR_IMAGES = 'files/images'
FILE_NAME_SEP = '_'
FILE_IMAGE_EXT  = 'png'

#logs
DEFAULT_LOG_DIR = 'logs'
DEFAULT_LOG_FILE_NAME = 'log.txt'
LOG_SEP = '|'