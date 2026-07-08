from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self, TypeVar

from pydantic import BaseModel, PrivateAttr

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient
    from ..client.sync_client import Client as SyncClient


ListModelT = TypeVar("ModelT", bound=BaseModel)


# ========== Synchronous Resource Models ==========#


class BaseResource(BaseModel, ABC):
    _client: "SyncClient | AsyncClient" = PrivateAttr()

    @classmethod
    def _from_model(cls, client: "SyncClient | AsyncClient", model: BaseModel) -> Self:
        obj = cls.model_validate(model.model_dump())
        obj._client = client
        return obj

    @classmethod
    def _parse_model(cls, payload: dict) -> Self:
        return cls.model_validate(payload)

    @classmethod
    def _parse_list(cls, payload: list[Any], list_model_type: type[ListModelT]) -> list[ListModelT]:
        return [list_model_type.model_validate(item) for item in payload]


class BaseConfigResource(BaseResource, ABC):

    @classmethod
    @abstractmethod
    def _build_list_request(
        self, facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def _build_get_request(self, facility_id: str, resource_id: str) -> dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def _build_create_request(self, facility_id: str, create_model: BaseModel) -> dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def _build_delete_request(self, facility_id: str, resource_id: str) -> dict[str, Any]:
        pass


class BaseConfigResourceSync(BaseConfigResource, ABC):

    @classmethod
    def _do_list_resources(
        cls,
        client: "SyncClient",
        facility_id: str,
        list_model_type: type[ListModelT],
        name: str | None = None,
        component_count: int | None = None,
    ) -> list[ListModelT]:
        """Helper to fetch and parse list of resources with a specific model class."""
        request = cls._build_list_request(facility_id, name, component_count)
        response = client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._parse_list(payload, list_model_type)

    @classmethod
    def _get_resource(cls, client: "SyncClient", facility_id: str, resource_id: str) -> Self:
        request = cls._build_get_request(facility_id, resource_id)
        response = client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))

    @classmethod
    def _create_resource(cls, client: "SyncClient", facility_id: str, create_model: BaseModel) -> Self:
        request = cls._build_create_request(facility_id, create_model)
        response = client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))

    @classmethod
    def _delete_resource(cls, client: "SyncClient", facility_id: str, resource_id: str) -> None:
        request = cls._build_delete_request(facility_id, resource_id)
        response = client._request(request)
        client._handle_response(response.status_code, response.text, client._maybe_json(response))


class BaseConfigResourceAsync(BaseConfigResource, ABC):

    @classmethod
    async def _do_list_resources_async(
        cls,
        client: "AsyncClient",
        facility_id: str,
        list_model_type: type[ListModelT],
        name: str | None = None,
        component_count: int | None = None,
    ) -> list[ListModelT]:
        request = cls._build_list_request(facility_id, name, component_count)
        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._parse_list(payload, list_model_type)

    @classmethod
    async def _get_resource_async(cls, client: "AsyncClient", facility_id: str, resource_id: str) -> Self:
        request = cls._build_get_request(facility_id, resource_id)
        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))

    @classmethod
    async def _create_resource_async(cls, client: "AsyncClient", facility_id: str, create_model: BaseModel) -> Self:
        request = cls._build_create_request(facility_id, create_model)
        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._from_model(client, cls._parse_model(payload))

    @classmethod
    async def _delete_resource_async(cls, client: "AsyncClient", facility_id: str, resource_id: str) -> None:
        request = cls._build_delete_request(facility_id, resource_id)
        response = await client._request(request)
        client._handle_response(response.status_code, response.text, client._maybe_json(response))
