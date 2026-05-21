import base64
from datetime import datetime, timedelta

import requests

from framework.utils.config_loader import ConfigLoader
from framework.utils.logger import LoggerManager


class AuthClient:
    """
    Centralized authentication manager.

    Responsibilities:
    - Authentication handling
    - Token lifecycle management
    - API key handling
    - Basic auth handling
    - Auth header generation
    """

    _token = None
    _token_expiry = None

    def __init__(self):

        self.config = ConfigLoader.load_config()

        self.logger = LoggerManager.get_logger()

        auth_config = self.config.get("auth", {})

        self.auth_enabled = auth_config.get("enabled", False)

        self.auth_type = auth_config.get("type", "none")

        self.auth_url = auth_config.get("auth_url")

        self.username = auth_config.get("username")

        self.password = auth_config.get("password")

        self.api_key = auth_config.get("api_key")

        self.api_key_header = auth_config.get(
            "api_key_header",
            "x-api-key"
        )

        self.token_expiry_buffer = auth_config.get(
            "token_expiry_buffer",
            60
        )

        self.base_url = self.config.get("base_url")

        self.timeout = self.config.get("timeout", 30)

    def authenticate(self):
        """
        Authenticate and fetch bearer token.
        """

        if self.auth_type != "bearer":
            return

        url = f"{self.base_url}{self.auth_url}"

        payload = {
            "email": self.username,
            "password": self.password
        }

        self.logger.info(f"Authenticating user: {self.username}")

        response = requests.post(
            url=url,
            json=payload,
            timeout=self.timeout
        )

        response.raise_for_status()

        response_data = response.json()

        token = response_data.get("token")

        if not token:
            raise Exception("Authentication token missing in response")

        self._token = token

        # ReqRes does not provide token expiry.
        # Simulating expiry handling for framework design.

        self._token_expiry = datetime.utcnow() + timedelta(minutes=30)

        self.logger.info("Authentication successful")

    def is_token_expired(self) -> bool:
        """
        Check whether token is expired.
        """

        if not self._token:
            return True

        if not self._token_expiry:
            return True

        current_time = datetime.utcnow()

        buffer_time = self._token_expiry - timedelta(
            seconds=self.token_expiry_buffer
        )

        return current_time >= buffer_time

    def get_valid_token(self) -> str:
        """
        Return valid token.
        Re-authenticate if needed.
        """

        if self.is_token_expired():

            self.logger.info(
                "Token expired or unavailable. Re-authenticating..."
            )

            self.authenticate()

        return self._token

    def get_auth_headers(self) -> dict:
        """
        Return authentication headers based on auth type.
        """

        if not self.auth_enabled:
            return {}

        if self.auth_type == "none":
            return {}

        if self.auth_type == "bearer":

            token = self.get_valid_token()

            return {
                "Authorization": f"Bearer {token}"
            }

        if self.auth_type == "api_key":

            if not self.api_key:

                self.logger.warning(
                    "API key authentication enabled but API key missing"
                )

                return {}

            return {
                self.api_key_header: self.api_key
            }

        if self.auth_type == "basic":

            credentials = f"{self.username}:{self.password}"

            encoded_credentials = base64.b64encode(
                credentials.encode()
            ).decode()

            return {
                "Authorization": f"Basic {encoded_credentials}"
            }

        self.logger.warning(
            f"Unsupported auth type configured: {self.auth_type}"
        )

        return {}

    def refresh_token(self):
        """
        Placeholder for future refresh token support.
        """

        self.logger.info("Refreshing token...")

        self.authenticate()