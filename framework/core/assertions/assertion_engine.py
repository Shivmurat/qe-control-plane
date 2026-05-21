from framework.utils.logger import LoggerManager
from framework.utils.schema_validator import SchemaValidator

class AssertionEngine:
    """
    Centralized assertion engine.
    """

    logger = LoggerManager.get_logger()

    @classmethod
    def assert_status_code(
            cls,
            actual_status_code: int,
            expected_status_code: int
    ):

        cls.logger.info(
            f"Asserting status code |"
            f"Expected: {expected_status_code} |"
            f"Actual: {expected_status_code} |"
        )

        assert actual_status_code == expected_status_code, (
            f"Status code assertion failed | "
            f"Expected: {expected_status_code} | "
            f"Actual: {actual_status_code}"
        )

    @classmethod
    def assert_response_field(
            cls,
            actual_value,
            expected_value,
            field_name: str
    ):
        cls.logger.info(
            f"Asserting response field '{field_name}'"
        )

        assert actual_value == expected_value, (
            f"Field assertion failed for '{field_name}' | "
            f"Expected: {expected_value} | "
            f"Actual: {actual_value}"
        )

    @classmethod
    def assert_schema(
            cls,
            response_json: dict,
            schema: dict
    ):
        cls.logger.info("Starting schema assertion")

        SchemaValidator.validate_schema(
            response_json=response_json,
            schema=schema)

        cls.logger.info("Schema assertion successful")

    @classmethod
    def assert_response_not_empty(
            cls,
            response_json: dict
    ):
        cls.logger.info("Validating response is not empty")

        assert response_json, "Response validation failed | Response is empty"