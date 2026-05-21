from framework.clients.reqres_client import ReqresClient
from framework.core.assertions.assertion_engine import AssertionEngine
from framework.models.requests.reqres_request import CreateUserRequest
from framework.models.responses.reqres_response import CreateUserResponse
from framework.schemas.reqres.create_user_schema import CREATE_USER_SCHEMA
from framework.utils.data_generator import DataGenerator
from framework.utils.logger import LoggerManager
from framework.constants.status_codes import HTTP_CREATED


logger = LoggerManager.get_logger()


class TestCreateUser:

    def test_create_user(self, reqres_client):

        logger.info("Starting create user smoke test")

     #   client = ReqresClient()

        generated_payload = DataGenerator.generate_user_payload()

        request_model = CreateUserRequest(**generated_payload)

        response = reqres_client.create_user(request_model.model_dump())

        AssertionEngine.assert_status_code(response.status_code, HTTP_CREATED)

        response_json = response.json()

        AssertionEngine.assert_response_not_empty(response_json)

        AssertionEngine.assert_schema(response_json, CREATE_USER_SCHEMA)

        parsed_response = CreateUserResponse(**response_json)

        AssertionEngine.assert_response_field(
            parsed_response.name,
            request_model.name,
            "name"
        )

        AssertionEngine.assert_response_field(
            parsed_response.job,
            request_model.job,
            "job"
        )

        logger.info("Create user smoke test completed successfully")