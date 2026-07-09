from typing import TYPE_CHECKING

from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.simulate_models import (
    FlashInlineRequestModel,
    FlashMeasuredModel,
    FlashSimulationRequestModel,
    FlashSimulationResponseModel,
    FlashWeightsModel,
)

if TYPE_CHECKING:
    from ...client.async_client import AsyncClient
    from ...client.sync_client import Client as SyncClient


class SimulationsManager:
    def __init__(self, client: "SyncClient"):
        self._client = client

    def run_flash(
        self,
        eos: EOSData,
        molar_composition: list[float],
        temperatures: list[float],
        pressures: list[float],
        measured: FlashMeasuredModel | None = None,
        weights: FlashWeightsModel | None = None,
    ) -> FlashSimulationResponseModel:
        """Run a flash simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            temperatures: List of temperatures in °C to perform simulation calculations at.
            pressures: List of pressures in bara to perform simulation calculations at.
            measured: Optional measured Flash values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured Flash property.

        Returns:
            The flash simulation results as FlashSimulationResponseModel.
        """
        request = FlashInlineRequestModel(
            eos_data=eos,
            parameters=FlashSimulationRequestModel(
                molar_composition=molar_composition,
                temperatures=temperatures,
                pressures=pressures,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/flash",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FlashSimulationResponseModel.model_validate(payload)


class AsyncSimulationsManager:
    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def run_flash(
        self,
        eos: EOSData,
        molar_composition: list[float],
        temperatures: list[float],
        pressures: list[float],
        measured: FlashMeasuredModel | None = None,
        weights: FlashWeightsModel | None = None,
    ) -> FlashSimulationResponseModel:
        """Run a flash simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            temperatures: List of temperatures in °C to perform simulation calculations at.
            pressures: List of pressures in bara to perform simulation calculations at.
            measured: Optional measured Flash values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured Flash property.

        Returns:
            The flash simulation results as FlashSimulationResponseModel.
        """
        request = FlashInlineRequestModel(
            eos_data=eos,
            parameters=FlashSimulationRequestModel(
                molar_composition=molar_composition,
                temperatures=temperatures,
                pressures=pressures,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/flash",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FlashSimulationResponseModel.model_validate(payload)
