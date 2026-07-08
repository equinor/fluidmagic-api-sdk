from abc import ABC
from typing import TYPE_CHECKING, Any, Self

from fluidmagic_api_sdk.models.config_models import (
    ConfigModel,
    ConfigReturnModel,
    ConfigType,
    FluidFilterType,
    MolesToVolCreateModel,
    MolesToVolRunInput,
    OutputFilterDict,
    RateToMolesCreateModel,
    RateToMolesRunInput,
)
from fluidmagic_api_sdk.models.data_models.frame_data import FrameData, MolToVolFrameData, RateToMolFrameData
from fluidmagic_api_sdk.resources.base_resource import (
    BaseConfigResource,
    BaseConfigResourceAsync,
    BaseConfigResourceSync,
)

if TYPE_CHECKING:
    from ..client.async_client import AsyncClient
    from ..client.sync_client import Client as SyncClient


class BaseConfig(ConfigModel, BaseConfigResource, ABC):

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
            "path": f"/facilities/{facility_id}/configs",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/configs/{id}",
        }

    @classmethod
    def _build_create_request(cls, facility_id: str, config_model: ConfigModel) -> dict[str, Any]:
        if isinstance(config_model, RateToMolesCreateModel):
            return cls._build_create_rate_to_moles_request(facility_id, config_model)
        if isinstance(config_model, MolesToVolCreateModel):
            return cls._build_create_moles_to_vol_request(facility_id, config_model)
        raise ValueError("Invalid config model type")

    @classmethod
    def _build_create_rate_to_moles_request(
        cls, facility_id: str, config_model: RateToMolesCreateModel
    ) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/configs/rate-to-moles",
            "body": config_model.model_dump(),
        }

    @classmethod
    def _build_create_moles_to_vol_request(
        cls, facility_id: str, config_model: MolesToVolCreateModel
    ) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/configs/moles-to-vol",
            "body": config_model.model_dump(),
        }

    @classmethod
    def _parse_model(cls, payload: dict) -> Self:
        return ConfigModel.from_return_model(ConfigReturnModel.model_validate(payload))

    @classmethod
    def _build_delete_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "DELETE",
            "path": f"/facilities/{facility_id}/configs/{id}",
        }

    @classmethod
    def _build_run_rate_to_moles_request(
        cls, facility_id: str, config_id: str, run: RateToMolesRunInput
    ) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/configs/rate-to-moles/{config_id}/run",
            "body": run.model_dump(),
        }

    @classmethod
    def _build_run_moles_to_vol_request(
        cls, facility_id: str, config_id: str, run: MolesToVolRunInput
    ) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/configs/moles-to-vol/{config_id}/run",
            "body": run.model_dump(),
        }

    @classmethod
    def _parse_run_result(cls, payload: dict) -> FrameData:
        return FrameData.model_validate(payload)


class Config(BaseConfig, BaseConfigResourceSync):

    @classmethod
    def _list_resources(
        cls, client: "SyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[ConfigModel]:
        """List Config models."""
        return cls._do_list_resources(client, facility_id, ConfigModel, name, component_count)

    def delete(self) -> None:
        """Delete this Config model."""
        Config._delete_resource(self._client, self.facility_id, self.id)

    def run_rate_to_moles(self, input: RateToMolFrameData, output: FluidFilterType = FluidFilterType.ALL) -> FrameData:
        """Run a Rate to Moles conversion using this Config model.

        Args:
            input: The input frame data for the conversion.
            output: The output filter type (default: FluidFilterType.ALL).

        Returns:
            The conversion results as FrameData.
        """
        if self.config_type != ConfigType.RATE_TO_MOLES:
            raise ValueError("Config model is not of type RATE_TO_MOLES")

        run_input = RateToMolesRunInput(input=input, output=output)
        request = self._build_run_rate_to_moles_request(self.facility_id, self.id, run_input)
        response = self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return Config._parse_run_result(payload)

    def run_moles_to_vol(self, input: MolToVolFrameData, output: OutputFilterDict | None = None) -> FrameData:
        """Run a Moles to Volume conversion using this Config model.

        Args:
            input: The input frame data for the conversion.
            output: The output filter configuration (optional).

        Returns:
            The conversion results as FrameData.
        """
        if self.config_type != ConfigType.MOLES_TO_VOL:
            raise ValueError("This Config model is not of type MOLES_TO_VOL.")

        run_input = MolesToVolRunInput(input=input, output=output)
        request = self._build_run_moles_to_vol_request(self.facility_id, self.id, run_input)
        response = self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return Config._parse_run_result(payload)


class ConfigAsync(BaseConfig, BaseConfigResourceAsync):

    @classmethod
    async def _list_resources_async(
        cls,
        client: "AsyncClient",
        facility_id: str,
        name: str | None = None,
        component_count: int | None = None,
        config_type: ConfigType | None = None,
    ) -> list[ConfigModel]:
        """List Config models asynchronously."""
        request = cls._build_list_request(facility_id, name, component_count)
        if config_type is not None:
            request["params"] = request.get("params") or {}
            request["params"]["config_type"] = config_type

        response = await client._request(request)
        payload = client._handle_response(response.status_code, response.text, client._maybe_json(response))

        return cls._parse_list(payload, ConfigModel)

    async def delete_async(self) -> None:
        """Delete this Config model asynchronously."""
        await ConfigAsync._delete_resource_async(self._client, self.facility_id, self.id)

    async def run_rate_to_moles(
        self, input: RateToMolFrameData, output: FluidFilterType = FluidFilterType.ALL
    ) -> FrameData:
        """Run a Rate to Moles conversion asynchronously using this Config model."""
        if self.config_type != ConfigType.RATE_TO_MOLES:
            raise ValueError("Config model is not of type RATE_TO_MOLES")

        run_input = RateToMolesRunInput(input=input, output=output)
        request = self._build_run_rate_to_moles_request(self.facility_id, self.id, run_input)
        response = await self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return ConfigAsync._parse_run_result(payload)

    async def run_moles_to_vol(self, input: MolToVolFrameData, output: OutputFilterDict | None = None) -> FrameData:
        """Run a Moles to Volume conversion asynchronously using this Config model."""
        if self.config_type != ConfigType.MOLES_TO_VOL:
            raise ValueError("This Config model is not of type MOLES_TO_VOL.")

        run_input = MolesToVolRunInput(input=input, output=output)
        request = self._build_run_moles_to_vol_request(self.facility_id, self.id, run_input)
        response = await self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return ConfigAsync._parse_run_result(payload)
