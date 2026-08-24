from functools import cached_property
from typing import Any

import httpx

from ..resources.facility import Facility
from ..resources.managers.conversions_manager import ConversionsManager
from ..resources.managers.eos_development_manager import EOSDevelopmentManager
from ..resources.managers.simulations_manager import SimulationsManager
from .base_client import BaseClient


class Client(BaseClient):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "Use Client.using_client_credentials() or Client.using_interactive_login() to construct a Client instance."
        )

    @classmethod
    def using_client_credentials(
        cls,
        client_id: str,
        client_secret: str,
        base_url: str = None,
        environment: str = "prod",
        headers: dict[str, str] = None,
        timeout: httpx.Timeout = httpx.Timeout(15),
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        httpx_args: dict[str, Any] = None,
    ):
        if headers is None:
            headers = {}
        if httpx_args is None:
            httpx_args = {}

        self = cls.__new__(cls)
        self._init_using_client_credentials(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            environment=environment,
            headers=headers,
            timeout=timeout,
            verify_ssl=verify_ssl,
            follow_redirects=follow_redirects,
            httpx_args=httpx_args,
        )
        self._http_client = httpx.Client(
            base_url=self._base_url,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )

        return self

    @classmethod
    def using_interactive_login(
        cls,
        client_id: str,
        base_url: str = None,
        redirect_uri: str = "http://localhost:8400",
        environment: str = "prod",
        headers: dict[str, str] = None,
        timeout: httpx.Timeout = httpx.Timeout(15),
        verify_ssl: bool = True,
        follow_redirects: bool = True,
        httpx_args: dict[str, Any] = None,
    ):
        if headers is None:
            headers = {}
        if httpx_args is None:
            httpx_args = {}

        self = cls.__new__(cls)
        self._init_using_interactive_login(
            client_id=client_id,
            base_url=base_url,
            redirect_uri=redirect_uri,
            environment=environment,
            headers=headers,
            timeout=timeout,
            verify_ssl=verify_ssl,
            follow_redirects=follow_redirects,
            httpx_args=httpx_args,
        )
        self._http_client = httpx.Client(
            base_url=self._base_url,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )
        return self

    def _close(self) -> None:
        """Close the underlying HTTP client."""
        self._http_client.close()

    def __enter__(self) -> "Client":
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc: The exception instance.
            tb: The traceback object.
        """
        self._close()

    def _request(self, request_dict: dict[str, Any]) -> httpx.Response:
        """Make a request to the API.

        Args:
            request_dict: Dictionary containing request parameters.

        Returns:
            httpx.Response: The response from the API.
        """
        return self._http_client.request(
            method=request_dict.get("method"),
            url=request_dict.get("path"),
            headers=self._merge_headers(request_dict.get("headers")),
            params=request_dict.get("params"),
            json=request_dict.get("body"),
        )

    @cached_property
    def conversions(self) -> ConversionsManager:
        return ConversionsManager(self)

    @cached_property
    def simulations(self) -> SimulationsManager:
        return SimulationsManager(self)

    @cached_property
    def eos(self) -> EOSDevelopmentManager:
        return EOSDevelopmentManager(self)

    # Public API methods
    def list_facilities(self) -> list[Facility]:
        """Get a list of facilities.

        Returns:
            List of facility resources.
        """
        return Facility._list_resources(self)

    def get_facility(self, facility_id: str) -> Facility:
        """Get a facility by ID.

        Args:
            facility_id: The ID of the facility to retrieve.

        Returns:
            Facility: The facility resource.
        """
        return Facility._get_resource(self, facility_id)
