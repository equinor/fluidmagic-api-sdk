from abc import ABC
from typing import TYPE_CHECKING, Any

from fluidmagic_api_sdk.models.data_models.calculated import FlashCalculated
from fluidmagic_api_sdk.models.eos_models import EOSCreateModel, EOSModel, EOSOverviewModel
from fluidmagic_api_sdk.models.simulate_models import FlashCalculationRequestModel
from fluidmagic_api_sdk.resources.base_resource import (
    BaseConfigResource,
    BaseConfigResourceAsync,
    BaseConfigResourceSync,
)

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient
    from ..client.sync_client import Client as SyncClient


class BaseEOS(EOSModel, BaseConfigResource, ABC):

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
            "path": f"/facilities/{facility_id}/eos",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/eos/{id}",
        }

    @classmethod
    def _build_create_request(cls, facility_id: str, eos: EOSCreateModel) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/eos",
            "body": eos.model_dump(),
        }

    @classmethod
    def _build_delete_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "DELETE",
            "path": f"/facilities/{facility_id}/eos/{id}",
        }

    @classmethod
    def _build_simulate_flash_request(
        cls, facility_id: str, eos_id: str, input_data: FlashCalculationRequestModel
    ) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/eos/{eos_id}/simulate-flash",
            "body": input_data.model_dump(),
        }

    @classmethod
    def _parse_flash_result(cls, payload: dict) -> FlashCalculated:
        return FlashCalculated.model_validate(payload)


class EOS(BaseEOS, BaseConfigResourceSync):

    @classmethod
    def _list_resources(
        cls, client: "SyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[EOSOverviewModel]:
        """List EOS models as overview models."""
        return cls._do_list_resources(client, facility_id, EOSOverviewModel, name, component_count)

    # ========= Public API methods ========= #

    def delete(self) -> None:
        """Delete this EOS model."""
        EOS._delete_resource(self._client, self.facility_id, self.id)

    def simulate_flash(
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

        request = self._build_simulate_flash_request(self.facility_id, self.id, input_data)
        response = self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return self._parse_flash_result(payload)


class EOSAsync(BaseEOS, BaseConfigResourceAsync):

    @classmethod
    async def _list_resources_async(
        cls, client: "AsyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[EOSOverviewModel]:
        """List EOS models as overview models asynchronously."""
        return await cls._do_list_resources_async(client, facility_id, EOSOverviewModel, name, component_count)

    async def delete(self) -> None:
        """Delete this EOS model asynchronously."""
        await EOSAsync._delete_resource_async(self._client, self.facility_id, self.id)

    async def simulate_flash(
        self, molar_composition: list[float], temperature_conditions: list[float], pressure_conditions: list[float]
    ) -> FlashCalculated:
        """Simulate a flash calculation asynchronously using this EOS model."""

        input_data = FlashCalculationRequestModel(
            molar_composition=molar_composition,
            temperatures=temperature_conditions,
            pressures=pressure_conditions,
        )

        request = self._build_simulate_flash_request(self.facility_id, self.id, input_data)
        response = await self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return self._parse_flash_result(payload)
