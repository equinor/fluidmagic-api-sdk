from abc import ABC
from typing import Any

import httpx
from azure.identity import ClientSecretCredential, DeviceCodeCredential, InteractiveBrowserCredential

from ..config import settings
from ..errors import ApiError


class BaseClient(ABC):

    def __init__(
        self,
        base_url: str = None,
        headers: dict[str, str] = {},
        timeout: httpx.Timeout = httpx.Timeout(15),
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        httpx_args: dict[str, Any] = {},
        environment: str = "prod",
    ):
        self._headers = headers
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._follow_redirects = follow_redirects
        self._httpx_args = httpx_args

        if environment == "prod":
            self._base_url = settings.url_prod if base_url is None else base_url
            self._resource_id = settings.resource_id_prod
        else:
            self._base_url = settings.url_dev if base_url is None else base_url
            self._resource_id = settings.resource_id_dev

        self._tenant_id = settings.tenant_id
        self._scope = f"api://{self._resource_id}/.default"

        self._http_client: httpx.Client | httpx.AsyncClient
        self._credentials: ClientSecretCredential | DeviceCodeCredential | InteractiveBrowserCredential = None

    def _init_using_client_credentials(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = None,
        environment: str = "prod",
        headers: dict[str, str] = {},
        timeout: httpx.Timeout = httpx.Timeout(15),
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        httpx_args: dict[str, Any] = {},
    ) -> None:
        BaseClient.__init__(
            self,
            base_url=base_url,
            environment=environment,
            headers=headers,
            timeout=timeout,
            verify_ssl=verify_ssl,
            follow_redirects=follow_redirects,
            httpx_args=httpx_args,
        )
        self._credentials = ClientSecretCredential(
            tenant_id=self._tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

    def _init_using_interactive_login(
        self,
        client_id: str,
        base_url: str = None,
        redirect_uri: str = "http://localhost:8400",
        environment: str = "prod",
        headers: dict[str, str] = {},
        timeout: httpx.Timeout = httpx.Timeout(15),
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        httpx_args: dict[str, Any] = {},
    ) -> None:
        BaseClient.__init__(
            self,
            base_url=base_url,
            environment=environment,
            headers=headers,
            timeout=timeout,
            verify_ssl=verify_ssl,
            follow_redirects=follow_redirects,
            httpx_args=httpx_args,
        )
        self._credentials = InteractiveBrowserCredential(
            tenant_id=self._tenant_id,
            client_id=client_id,
            redirect_uri=redirect_uri,
        )

    def _get_token(self) -> str:
        """Return the token and refresh if timed out."""
        return self._credentials.get_token(self._scope).token

def _auth_header(self) -> dict[str, str] | None:
    """Return the authorization header."""
    token = self._get_token()
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}
    def _merge_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        """Merge the default headers with the provided headers.
        Always include Accept: application/json and Authorization if token exists.
        Args:
            headers: Headers to merge with default headers.

        Returns:
            Merged headers."""
        merged_headers = self._headers.copy()
        merged_headers["Accept"] = "application/json"

        auth_header = self._auth_header()
        if auth_header:
            merged_headers.update(auth_header)

        if headers:
            merged_headers.update(headers)

        return merged_headers

    def _maybe_json(self, r: httpx.Response) -> dict[str, Any] | None:
        """Return the JSON content if the response is JSON, else None."""
        return r.json() if r.headers.get("Content-Type") == "application/json" else None

    def _handle_response(self, status_code: int, text: str, json: dict[str, Any] | None) -> Any:
        """Handle the response from the API.
        Args:
            status_code: The status code of the response.
            text: The text content of the response.
            json: The JSON content of the response, if any.

        Returns:
            The JSON content of the response, if any.

        Raises:
            httpx.HTTPStatusError: If the response status code indicates an error.
        """
        if 200 <= status_code < 300:
            return json

        message = (json or {}).get("message") or text
        raise ApiError(status_code, message, json)
