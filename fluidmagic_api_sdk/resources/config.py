from typing import TYPE_CHECKING, Any, Self

from fluidmagic_api_sdk.models.config_models import (
    ConfigModel,
    ConfigReturnModel,
    ConfigType,
    MolesToVolCreateModel,
    MolesToVolRunInput,
    RateToMolesCreateModel,
    RateToMolesRunInput,
)
from fluidmagic_api_sdk.models.data_models.frame_data import FrameData
from fluidmagic_api_sdk.resources.base_resource import BaseConfigResource

if TYPE_CHECKING:
    from ..client.sync_client import Client as SyncClient


class Config(ConfigModel, BaseConfigResource):

    @classmethod
    def _list_resources(
        cls, client: "SyncClient", facility_id: str, name: str | None = None, component_count: int | None = None
    ) -> list[ConfigModel]:
        """List Config models."""
        return cls._do_list_resources(client, facility_id, ConfigModel, name, component_count)

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
        elif isinstance(config_model, MolesToVolCreateModel):
            return cls._build_create_moles_to_vol_request(facility_id, config_model)
        else:
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
    def _parse_run_result(cls, payload: dict) -> dict:
        return FrameData.model_validate(payload)

    # ======== Public API methods ========= #

    def delete(self) -> None:
        """Delete this Config model."""
        Config._delete_resource(self._client, self.facility_id, self.id)

    def run_rate_to_moles(self, input: RateToMolesRunInput) -> FrameData:
        """Run a Rate to Moles conversion using this Config model.

        Args:
            input: The input data for the conversion.

        Returns:
            The conversion results as FrameData.
        """
        if self.config_type != ConfigType.RATE_TO_MOLES:
            raise ValueError("Config model is not of type RATE_TO_MOLES")

        request = self._build_run_rate_to_moles_request(self.facility_id, self.id, input)
        response = self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return Config._parse_run_result(payload)

    def run_moles_to_vol(self, input: MolesToVolRunInput) -> FrameData:
        """Run a Moles to Volume conversion using this Config model.

        Args:
            input: The input data for the conversion.

        Returns:
            The conversion results as FrameData.
        """
        if self.config_type != ConfigType.MOLES_TO_VOL:
            raise ValueError("This Config model is not of type MOLES_TO_VOL.")

        request = self._build_run_moles_to_vol_request(self.facility_id, self.id, input)
        response = self._client._request(request)
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return Config._parse_run_result(payload)
