from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from fluidmagic_api_sdk.resources.managers.config_manager import ConfigManager
from fluidmagic_api_sdk.resources.managers.eos_manager import EOSManager
from fluidmagic_api_sdk.resources.managers.fluid_manager import FluidManager
from fluidmagic_api_sdk.resources.managers.process_manager import ProcessManager

from ..models.facility_models import FacilityModel
from ..resources.base import BaseResource

if TYPE_CHECKING:
    from ..client.sync_client import Client as SyncClient


class Facility(FacilityModel, BaseResource):
    @cached_property
    def eos(self):
        return EOSManager(self._client, self.id)

    @cached_property
    def processes(self):
        return ProcessManager(self._client, self.id)

    @cached_property
    def fluids(self):
        return FluidManager(self._client, self.id)

    @cached_property
    def configs(self):
        return ConfigManager(self._client, self.id)

    @classmethod
    def _build_list_request(cls, name: str | None = None, component_count: int | None = None) -> dict[str, Any]:
        params = {}
        if name is not None:
            params["name"] = name
        if component_count is not None:
            params["component_count"] = component_count

        return {
            "method": "GET",
            "path": "/facilities",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}",
        }

    @classmethod
    def _list_resources(
        cls, client: "SyncClient", name: str | None = None, component_count: int | None = None
    ) -> list[Self]:
        request = cls._build_list_request(name, component_count)
        response = client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return [cls._from_model(client, item) for item in cls._parse_list(payload)]

    @classmethod
    def _get_resource(cls, client: "SyncClient", facility_id: str) -> Self:
        request = cls._build_get_request(facility_id)
        response = client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))
