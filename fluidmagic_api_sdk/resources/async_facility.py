from functools import cached_property
from typing import TYPE_CHECKING, Self

from fluidmagic_api_sdk.resources.facility import Facility
from fluidmagic_api_sdk.resources.managers.async_config_manager import AsyncConfigManager
from fluidmagic_api_sdk.resources.managers.async_eos_manager import AsyncEOSManager
from fluidmagic_api_sdk.resources.managers.async_fluid_manager import AsyncFluidManager
from fluidmagic_api_sdk.resources.managers.async_process_manager import AsyncProcessManager

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient


class AsyncFacility(Facility):
    @cached_property
    def eos(self) -> AsyncEOSManager:
        return AsyncEOSManager(self._client, self.id)

    @cached_property
    def processes(self) -> AsyncProcessManager:
        return AsyncProcessManager(self._client, self.id)

    @cached_property
    def fluids(self) -> AsyncFluidManager:
        return AsyncFluidManager(self._client, self.id)

    @cached_property
    def configs(self) -> AsyncConfigManager:
        return AsyncConfigManager(self._client, self.id)

    @classmethod
    async def _list_resources_async(
        cls, client: "AsyncClient", name: str | None = None, component_count: int | None = None
    ) -> list[Self]:
        request = cls._build_list_request(name, component_count)
        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return [cls._from_model(client, item) for item in cls._parse_list(payload)]

    @classmethod
    async def _get_resource_async(cls, client: "AsyncClient", facility_id: str) -> Self:
        request = cls._build_get_request(facility_id)
        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))
