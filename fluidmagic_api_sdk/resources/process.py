from abc import ABC
from typing import TYPE_CHECKING, Any

from fluidmagic_api_sdk.models.process_models import ProcessCreateModel, ProcessModel, ProcessOverviewModel
from fluidmagic_api_sdk.resources.base_resource import (
    BaseConfigResource,
    BaseConfigResourceAsync,
    BaseConfigResourceSync,
)

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient
    from ..client.sync_client import Client as SyncClient


class BaseProcess(ProcessModel, BaseConfigResource, ABC):

    @classmethod
    def _build_list_request(
        cls, facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> dict[str, Any]:
        params = {}
        if name is not None:
            params["name"] = name
        if component_count is not None:
            params["component_count"] = component_count

        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/processes",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/processes/{id}",
        }

    @classmethod
    def _build_create_request(cls, facility_id: str, process_model: ProcessCreateModel) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/processes",
            "body": process_model.model_dump(),
        }

    @classmethod
    def _build_delete_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "DELETE",
            "path": f"/facilities/{facility_id}/processes/{id}",
        }


class Process(BaseProcess, BaseConfigResourceSync):

    @classmethod
    def _list_resources(
        cls, client: "SyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[ProcessOverviewModel]:
        """List Process models as overview models."""
        return cls._do_list_resources(client, facility_id, ProcessOverviewModel, name, component_count)

    def delete(self) -> None:
        """Delete this Process model."""
        Process._delete_resource(self._client, self.facility_id, self.id)


class ProcessAsync(BaseProcess, BaseConfigResourceAsync):

    @classmethod
    async def _list_resources_async(
        cls, client: "AsyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[ProcessOverviewModel]:
        """List Process models as overview models asynchronously."""
        return await cls._do_list_resources_async(client, facility_id, ProcessOverviewModel, name, component_count)

    async def delete_async(self) -> None:
        """Delete this Process model asynchronously."""
        await ProcessAsync._delete_resource_async(self._client, self.facility_id, self.id)
