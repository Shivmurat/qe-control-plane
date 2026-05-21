import pytest

from framework.clients.reqres_client import ReqresClient
from framework.utils.logger import LoggerManager

logger = LoggerManager.get_logger()

@pytest.fixture(scope="session")
def reqres_client():
    """
    Shared reqres client fixture.
    """

    logger.info("Initializing ReqRes client fixture")

    return ReqresClient()