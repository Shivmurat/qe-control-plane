from requests import Response

from framework.clients.base_client import BaseClient

class ReqresClient(BaseClient):
    """
    Reqres service client.
    """

    USER_ENDPOINT = "/api/users"

    LOGIN_ENDPOINT = "/api/login"

    REGISTER_ENDPOINT = "/api/register"

    def get_user(self, page: int = 2) -> Response:
        """
        Fetch users list.
        """

        params = {
            "page": page
        }

        return self.get(endpoint=self.USER_ENDPOINT, params=params)

    def get_signle_user(self, user_id: int) -> Response:
        """
        Fetch single user.
        """

        return self.get(endpoint=f"{self.USER_ENDPOINT}/{user_id}")

    def create_user(self, payload: dict) -> Response:
        """
        Create new user
        """

        return self.post(endpoint=self.USER_ENDPOINT, payload=payload)

    def update_user(self, user_id: int, payload: dict) -> Response:
        """
        Updating existing user.
        """

        return self.put(endpoint=f"{self.USER_ENDPOINT}/{user_id}",
                        payload=payload
        )


    def delete_user(self, user_id: int)-> Response:
        """
        Delete User
        """

        return self.delete(endpoint=f"{self.USER_ENDPOINT}/{user_id}")


    def login_user(self, payload: dict)-> Response:
        """
        Login user
        """

        return self.post(endpoint=self.LOGIN_ENDPOINT, payload=payload)

    def register_user(self, payload: dict) -> Response:
        """
        Register user.
        """

        return self.post(endpoint=self.REGISTER_ENDPOINT, payload=payload)



