from utils import get_config_service
from constants import SERVICE_AZURE, SERVICE_STABILITY


def get_image_instance(config):

    service = config.get("image_service", "").lower()
    config_service = get_config_service(service)

    if service == SERVICE_AZURE:
        from services.azure import AzureImageService
        return AzureImageService(config_service)
    elif service == SERVICE_STABILITY:
        from services.stability import StabilityImageService
        return StabilityImageService(config_service)
    else:
        raise ValueError("Invalid image service specified in the config.")

