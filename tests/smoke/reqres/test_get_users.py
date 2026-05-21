#from framework.clients.reqres_client import ReqresClient
from framework.core.assertions.assertion_engine import AssertionEngine
from framework.models.responses.reqres_response import UsersListResponse
from framework.schemas.reqres.user_schema import GET_USERS_SCHEMA
from framework.utils.logger import LoggerManager
from framework.reporting.allure.allure_helper import AllureHelper
from framework.constants.status_codes import HTTP_OK

logger = LoggerManager.get_logger()

class TestGetUsers:
    """
    Smoke tests for get users API
    """

    def test_get_users(self, reqres_client):

        logger.info("Starting get users smoke test")

      #  client = ReqresClient()

        response = reqres_client.get_user(page=2)

        AssertionEngine.assert_status_code(response.status_code, HTTP_OK)

        response_json = response.json()

        AllureHelper.attach_json(
            response_json,
            "Get Users Response"
        )

        AssertionEngine.assert_response_not_empty(response_json)

        AssertionEngine.assert_schema(response_json, GET_USERS_SCHEMA)

        parsed_response = UsersListResponse(**response_json)

        AssertionEngine.assert_response_field(
            parsed_response.page, 2, "page")

        AssertionEngine.assert_response_field(
            parsed_response.data[0].id, 7, "first_user_id")

        logger.info("Get users smoke test completed successfully")