from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self, TypeVar

from pydantic import BaseModel, PrivateAttr

from ..client.core import requests, responses
from ..models.data_models.calculated import FlashCalculated
from ..models.eos_models import EOSCreateModel, EOSModel
from ..models.facility_models import FacilityModel
from ..models.simulate_models import FlashCalculationRequestModel

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient
    from ..client.sync_client import Client as SyncClient


ListModelT = TypeVar("ModelT", bound=BaseModel)


# ========== Synchronous Resource Models ==========#


class BaseResource(BaseModel, ABC):
    _client: "SyncClient" = PrivateAttr()

    @classmethod
    def _from_model(cls, client: "SyncClient", model: BaseModel) -> Self:
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


# ========== Asynchronous Resource Models ==========#


class AsyncBaseResource(BaseModel):
    _client: "AsyncClient" = PrivateAttr()

    @classmethod
    def _from_model(cls, client: "AsyncClient", model: BaseModel):
        obj = cls.model_validate(model.model_dump())
        obj._client = client
        return obj


class AsyncFacilityResource(FacilityModel, AsyncBaseResource):
    async def get_eoses(self, name: str | None = None, component_count: int | None = None) -> list["AsyncEOSResource"]:
        """Get all EOS models for this facility."""
        response = await self._client._request(requests.build_list_eoses(self.id, name, component_count))
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))

        return [AsyncEOSResource._from_model(self._client, item) for item in responses.parse_eos_list(payload)]

    async def get_eos(self, eos_id: str) -> "AsyncEOSResource":
        """Get a specific EOS model by ID for this facility."""
        response = await self._client._request(requests.build_get_eos(self.id, eos_id))
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))

        return AsyncEOSResource._from_model(self._client, responses.parse_eos(payload))

    async def create_eos(self, eos_create_model: "EOSCreateModel") -> "AsyncEOSResource":
        """Create a new EOS model for this facility."""
        request = requests.build_create_eos(self.id, eos_create_model)
        response = await self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))

        return AsyncEOSResource._from_model(self._client, responses.parse_eos(payload))

    async def delete_eos(self, eos_id: str) -> None:
        """Delete a specific EOS model by ID for this facility."""
        request = requests.build_delete_eos(self.id, eos_id)
        response = await self._client._request(request)
        self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))


class AsyncEOSResource(EOSModel, AsyncBaseResource):
    async def delete(self) -> None:
        """Delete this EOS model."""
        request = requests.build_delete_eos(self.facility_id, self.id)
        response = await self._client._request(request)
        self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))

    async def simulate_flash(
        self, molar_composition: list[float], temperature_conditions: list[float], pressure_conditions: list[float]
    ) -> FlashCalculated:
        """Simulate a flash calculation using this EOS model.

        Args:
            molar_compositions: Molar composition of feed fluid.
            temperature_conditions: Temperature conditions to simulate at.
            pressure_conditions: Pressure conditions to simulate at.

        Returns:
            dict: The result of the flash calculation.
        """
        input_data = FlashCalculationRequestModel(
            molar_composition=molar_composition,
            temperatures=temperature_conditions,
            pressures=pressure_conditions,
        )

        request = requests.build_simulate_flash(
            self.facility_id,
            self.id,
            input_data.model_dump(),
        )
        response = await self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return responses.parse_flash_result(payload)
