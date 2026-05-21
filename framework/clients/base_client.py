import uuid
import requests

from requests import Response
from tenacity import retry, stop_after_attempt, wait_fixed
from framework.clients.auth_client import AuthClient
from framework.core.exceptions.retry_exceptions import RetryableStatusCodeException
from framework.constants.status_codes import RETRYABLE_STATUS_CODES
from framework.constants.auth_constants import AUTH_RETRY_STATUS_CODES


from framework.utils.config_loader import ConfigLoader
from framework.utils.logger import LoggerManager


class BaseClient:
    """
    Base API client.

    Responsibilities:
    - HTTP transport handling
    - Retry handling
    - Authentication handling
    - Session management
    - Request/response logging
    """

    def __init__(self):

        self.config = ConfigLoader.load_config()

        self.logger = LoggerManager.get_logger()

        self.auth_client = AuthClient()

        self.base_url = self.config.get("base_url")

        self.timeout = self.config.get("timeout", 30)

        self.retry_count = self.config.get("retry_count", 3)

        self.retryable_status_codes = RETRYABLE_STATUS_CODES

        self.session = requests.Session()


    def _build_url(self, endpoint: str) -> str:
        """
        Build complete request URL.
        """

        return f"{self.base_url}{endpoint}"


    def _build_headers(self, headers: dict = None,
                       add_idempotency_key: bool = False) -> dict:
        """
        Build request headers.
        """

        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Correlation-ID": str(uuid.uuid4())
        }

        if add_idempotency_key:
            default_headers["Idempotency-Key"] = str(uuid.uuid4())

        auth_headers = self.auth_client.get_auth_headers()

        default_headers.update(auth_headers)

        if headers:
            default_headers.update(headers)

        return default_headers


    def _handle_retryable_status_codes(self, response: Response):
        """
        Retry for configured retryable status codes.
        """

        if response.status_code in self.retryable_status_codes:

            self.logger.warning(
                f"Retryable status code received: "
                f"{response.status_code}"
            )

            raise RetryableStatusCodeException(
                f"Retryable status code: {response.status_code}"
            )


    def _handle_auth_failure(self, response: Response):
        """
        Handle authentication failures.
        """

        if response.status_code in AUTH_RETRY_STATUS_CODES:
            self.logger.warning(
                "Authentication failure detected. "
                "Refreshing token and retrying request."
            )

            self.auth_client.refresh_token()

            raise RetryableStatusCodeException(
                "Retrying request after token refresh"
            )


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        reraise=True
    )
    def get(
            self,
            endpoint: str,
            headers: dict = None,
            params: dict = None
    ) -> Response:
        """
        Execute GET request.
        """

        url = self._build_url(endpoint)

        request_headers = self._build_headers(headers)

        self.logger.info(f"GET Request -> {url}")

        response = self.session.get(
            url=url,
            headers=request_headers,
            params=params,
            timeout=self.timeout
        )

        self._handle_auth_failure(response)
        self._handle_retryable_status_codes(response)

        self.logger.info(
            f"GET Response <- "
            f"Status: {response.status_code} | "
            f"URL: {url}"
        )

        return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        reraise=True
    )
    def post(
            self,
            endpoint: str,
            payload: dict = None,
            headers: dict = None,
            params: dict = None
    ) -> Response:
        """
        Execute POST request.
        """

        url = self._build_url(endpoint)

        request_headers = self._build_headers(headers, add_idempotency_key=True)

        self.logger.info( f"POST Request -> URL: {url} | Payload: {payload}")

        response = self.session.post(
            url=url,
            headers=request_headers,
            json=payload,
            params=params,
            timeout=self.timeout
        )

        self._handle_auth_failure(response)
        self._handle_retryable_status_codes(response)

        self.logger.info(
            f"POST Response <- "
            f"Status: {response.status_code} | "
            f"URL: {url}"
        )

        return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        reraise=True
    )
    def put(
            self,
            endpoint: str,
            payload: dict = None,
            headers: dict = None
    ) -> Response:
        """
        Execute PUT request.
        """

        url = self._build_url(endpoint)

        request_headers = self._build_headers(headers, add_idempotency_key=True)

        self.logger.info(
            f"PUT Request -> URL: {url} | Payload: {payload}"
        )

        response = self.session.put(
            url=url,
            headers=request_headers,
            json=payload,
            timeout=self.timeout
        )

        self._handle_auth_failure(response)
        self._handle_retryable_status_codes(response)

        self.logger.info(
            f"PUT Response <- "
            f"Status: {response.status_code} | "
            f"URL: {url}"
        )

        return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        reraise=True
    )
    def delete(
            self,
            endpoint: str,
            headers: dict = None
    ) -> Response:
        """
        Execute DELETE request.
        """

        url = self._build_url(endpoint)

        request_headers = self._build_headers(headers)

        self.logger.info(f"DELETE Request -> {url}")

        response = self.session.delete(
            url=url,
            headers=request_headers,
            timeout=self.timeout
        )

        self._handle_auth_failure(response)
        self._handle_retryable_status_codes(response)

        self.logger.info(
            f"DELETE Response <- "
            f"Status: {response.status_code} | "
            f"URL: {url}"
        )

        return response