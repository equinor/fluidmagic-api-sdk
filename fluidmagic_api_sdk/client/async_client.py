from functools import cached_property
from typing import Any, Self

import httpx

from fluidmagic_api_sdk.resources.async_facility import AsyncFacility

from ..resources.managers.conversions_manager import AsyncConversionsManager
from ..resources.managers.simulations_manager import AsyncSimulationsManager
from .base_client import BaseClient


class AsyncClient(BaseClient):

    def __init__(self):
        raise NotImplementedError(
            """Use AsyncClient.using_client_credentials() or AsyncClient.using_interactive_login()
            to construct a Client instance."""
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
        self._http_client = httpx.AsyncClient(
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
        self._http_client = httpx.AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )
        return self

    async def __aenter__(self) -> Self:
        """Enter the runtime context related to this object."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc: The exception instance.
            tb: The traceback object.
        """
        await self.aclose()

    async def _request(self, request_dict: dict[str, Any]) -> httpx.Response:
        """Make an async request to the API.

        Args:
            request_dict: Dictionary containing request parameters.

        Returns:
            httpx.Response: The response from the API.
        """
        return await self._http_client.request(
            method=request_dict.get("method"),
            url=request_dict.get("path"),
            headers=self._merge_headers(request_dict.get("headers")),
            params=request_dict.get("params"),
            json=request_dict.get("body"),
        )

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self._http_client.aclose()

    @cached_property
    def conversions(self) -> AsyncConversionsManager:
        return AsyncConversionsManager(self)

    @cached_property
    def simulations(self) -> AsyncSimulationsManager:
        return AsyncSimulationsManager(self)

    # Public API methods
    async def list_facilities(self) -> list[AsyncFacility]:
        """Get a list of facilities.

        Returns:
            List of facility resources.
        """
        return await AsyncFacility._list_resources_async(self)

    async def get_facility(self, facility_id: str):
        """Get a facility by ID.

        Args:
            facility_id: The ID of the facility to retrieve.

        Returns:
            Facility: The facility resource.
        """
        return await AsyncFacility._get_resource_async(self, facility_id)
