from framework.utils.config_loader import ConfigLoader

from framework.utils.logger import LoggerManager

#config = ConfigLoader.load_config()

def test_config_loader():
    base_url = ConfigLoader.get("base_url", "")

    timeout = ConfigLoader.get("timeout", 0)

    print(f"base_url is {base_url}")
    print(f"timeout is {timeout}")


def test_logger():
    logger = LoggerManager.get_logger()

    logger.info("Framework execution started")
    logger.error("API request failed")