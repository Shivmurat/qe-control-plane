import allure
import json

class AllureHelper:
    """
    Centralized Allure attachment helper.
    """

    @staticmethod
    def attach_json(data: dict, name: str):

        allure.attach(
            body=json.dumps(data, indent=4),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )


    @staticmethod
    def attach_text(data: str, name: str):
        allure.attach(
            body=data,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )