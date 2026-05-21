from jsonschema import validate
from jsonschema.exceptions import ValidationError

from framework.utils.logger import LoggerManager

class SchemaValidator:
    """
    Centralised schema validator.
    """

    logger = LoggerManager.get_logger()

    @classmethod
    def validate_schema(cls, response_json: dict, schema: dict):
        """
        Validate response against JSON schema.
        """
        cls.logger.info("Starting JSON schema validation")

        try:
            validate(instance=response_json, schema=schema)

            cls.logger.info("JSON schema validation successful")

        except ValidationError as error:
            cls.logger.error(f"Schema validation failed: {error.message} ")
            raise


