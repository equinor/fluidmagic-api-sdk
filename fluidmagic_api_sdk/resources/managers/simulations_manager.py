from typing import TYPE_CHECKING

from fluidmagic_api_sdk.models.data_models.calculated import (
    CMECalculated,
    CVDCalculated,
    DLECalculated,
    SeparatorCalculated,
)
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.process_data import ProcessData
from fluidmagic_api_sdk.models.simulate_models import (
    CMEInlineRequestModel,
    CMEMeasuredModel,
    CMESimulationRequestModel,
    CMEWeightsModel,
    CVDInlineRequestModel,
    CVDMeasuredModel,
    CVDSimulationRequestModel,
    CVDWeightsModel,
    DLEInlineRequestModel,
    DLEMeasuredModel,
    DLESimulationRequestModel,
    DLEWeightsModel,
    FlashInlineRequestModel,
    FlashMeasuredModel,
    FlashSimulationRequestModel,
    FlashSimulationResponseModel,
    FlashWeightsModel,
    ProcessInlineRequestModel,
    ProcessSimulationRequestModel,
    ProcessSimulationResponseModel,
    PsatInlineRequestModel,
    PsatMeasuredModel,
    PsatSimulationRequestModel,
    PsatSimulationResponseModel,
    PsatWeightsModel,
    SEPInlineRequestModel,
    SEPMeasuredModel,
    SEPSimulationRequestModel,
    SEPWeightsModel,
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

    def run_cme(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: CMEMeasuredModel | None = None,
        weights: CMEWeightsModel | None = None,
    ) -> CMECalculated:
        """Run a CME (Constant Molar Expansion) simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured CME values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured CME property.

        Returns:
            The CME simulation results as CMECalculated.
        """
        request = CMEInlineRequestModel(
            eos_data=eos,
            parameters=CMESimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/cme",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "cme_calculated" in payload:
            return CMECalculated.model_validate(payload["cme_calculated"])
        return CMECalculated.model_validate(payload)

    def run_cvd(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: CVDMeasuredModel | None = None,
        weights: CVDWeightsModel | None = None,
    ) -> CVDCalculated:
        """Run a CVD (Constant Volume Depletion) simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured CVD values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured CVD property.

        Returns:
            The CVD simulation results as CVDCalculated.
        """
        request = CVDInlineRequestModel(
            eos_data=eos,
            parameters=CVDSimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/cvd",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "cvd_calculated" in payload:
            return CVDCalculated.model_validate(payload["cvd_calculated"])
        return CVDCalculated.model_validate(payload)

    def run_dle(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: DLEMeasuredModel | None = None,
        weights: DLEWeightsModel | None = None,
    ) -> DLECalculated:
        """Run a DLE (Differential Liberation) simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured DLE values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured DLE property.

        Returns:
            The DLE simulation results as DLECalculated.
        """
        request = DLEInlineRequestModel(
            eos_data=eos,
            parameters=DLESimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/dle",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "dle_calculated" in payload:
            return DLECalculated.model_validate(payload["dle_calculated"])
        return DLECalculated.model_validate(payload)

    def run_sep(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperatures: list[float],
        measured: SEPMeasuredModel | None = None,
        weights: SEPWeightsModel | None = None,
    ) -> SeparatorCalculated:
        """Run a separator (SEP) simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of stage pressures in bara (monotonically decreasing).
            temperatures: List of stage temperatures in °C.
            measured: Optional measured SEP values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured SEP property.

        Returns:
            The SEP simulation results as SeparatorCalculated.
        """
        request = SEPInlineRequestModel(
            eos_data=eos,
            parameters=SEPSimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperatures=temperatures,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/sep",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "sep_calculated" in payload:
            return SeparatorCalculated.model_validate(payload["sep_calculated"])
        if "separator_calculated" in payload:
            return SeparatorCalculated.model_validate(payload["separator_calculated"])
        return SeparatorCalculated.model_validate(payload)

    def run_psat(
        self,
        eos: EOSData,
        molar_composition: list[float],
        temperature: float,
        measured: PsatMeasuredModel | None = None,
        weights: PsatWeightsModel | None = None,
    ) -> PsatSimulationResponseModel:
        """Run a saturation-pressure (PSAT) simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            temperature: Isothermal temperature in °C.
            measured: Optional measured saturation pressure for sum-of-squares evaluation.
            weights: Optional regression weight for measured saturation pressure.

        Returns:
            The PSAT simulation results as PsatSimulationResponseModel.
        """
        request = PsatInlineRequestModel(
            eos_data=eos,
            parameters=PsatSimulationRequestModel(
                molar_composition=molar_composition,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/psat",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return PsatSimulationResponseModel.model_validate(payload)

    def run_process(
        self,
        eos: EOSData,
        molar_stream: list[float],
        process: ProcessData,
    ) -> ProcessSimulationResponseModel:
        """Run a surface process simulation.

        Args:
            eos: EOS model data to use for simulation.
            molar_stream: Inlet stream in kg-moles per component.
            process: Process definition (tanks, conditions, and routing).

        Returns:
            Per-tank simulation outputs as ProcessSimulationResponseModel.
        """
        request = ProcessInlineRequestModel(
            eos_data=eos,
            parameters=ProcessSimulationRequestModel(
                molar_stream=molar_stream,
                process=process,
            ),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/simulate/process",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "process_simulation" in payload:
            return ProcessSimulationResponseModel.model_validate(payload["process_simulation"])
        return ProcessSimulationResponseModel.model_validate(payload)


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

    async def run_cme(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: CMEMeasuredModel | None = None,
        weights: CMEWeightsModel | None = None,
    ) -> CMECalculated:
        """Run a CME (Constant Molar Expansion) simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured CME values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured CME property.

        Returns:
            The CME simulation results as CMECalculated.
        """
        request = CMEInlineRequestModel(
            eos_data=eos,
            parameters=CMESimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/cme",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "cme_calculated" in payload:
            return CMECalculated.model_validate(payload["cme_calculated"])
        return CMECalculated.model_validate(payload)

    async def run_cvd(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: CVDMeasuredModel | None = None,
        weights: CVDWeightsModel | None = None,
    ) -> CVDCalculated:
        """Run a CVD (Constant Volume Depletion) simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured CVD values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured CVD property.

        Returns:
            The CVD simulation results as CVDCalculated.
        """
        request = CVDInlineRequestModel(
            eos_data=eos,
            parameters=CVDSimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/cvd",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "cvd_calculated" in payload:
            return CVDCalculated.model_validate(payload["cvd_calculated"])
        return CVDCalculated.model_validate(payload)

    async def run_dle(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperature: float,
        measured: DLEMeasuredModel | None = None,
        weights: DLEWeightsModel | None = None,
    ) -> DLECalculated:
        """Run a DLE (Differential Liberation) simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of pressures in bara (monotonically decreasing).
            temperature: Isothermal temperature in °C.
            measured: Optional measured DLE values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured DLE property.

        Returns:
            The DLE simulation results as DLECalculated.
        """
        request = DLEInlineRequestModel(
            eos_data=eos,
            parameters=DLESimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/dle",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "dle_calculated" in payload:
            return DLECalculated.model_validate(payload["dle_calculated"])
        return DLECalculated.model_validate(payload)

    async def run_sep(
        self,
        eos: EOSData,
        molar_composition: list[float],
        pressures: list[float],
        temperatures: list[float],
        measured: SEPMeasuredModel | None = None,
        weights: SEPWeightsModel | None = None,
    ) -> SeparatorCalculated:
        """Run a separator (SEP) simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            pressures: List of stage pressures in bara (monotonically decreasing).
            temperatures: List of stage temperatures in °C.
            measured: Optional measured SEP values used for sum-of-squares evaluation.
            weights: Optional regression weights per measured SEP property.

        Returns:
            The SEP simulation results as SeparatorCalculated.
        """
        request = SEPInlineRequestModel(
            eos_data=eos,
            parameters=SEPSimulationRequestModel(
                molar_composition=molar_composition,
                pressures=pressures,
                temperatures=temperatures,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/sep",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "sep_calculated" in payload:
            return SeparatorCalculated.model_validate(payload["sep_calculated"])
        if "separator_calculated" in payload:
            return SeparatorCalculated.model_validate(payload["separator_calculated"])
        return SeparatorCalculated.model_validate(payload)

    async def run_psat(
        self,
        eos: EOSData,
        molar_composition: list[float],
        temperature: float,
        measured: PsatMeasuredModel | None = None,
        weights: PsatWeightsModel | None = None,
    ) -> PsatSimulationResponseModel:
        """Run a saturation-pressure (PSAT) simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_composition: Molar composition for each component.
            temperature: Isothermal temperature in °C.
            measured: Optional measured saturation pressure for sum-of-squares evaluation.
            weights: Optional regression weight for measured saturation pressure.

        Returns:
            The PSAT simulation results as PsatSimulationResponseModel.
        """
        request = PsatInlineRequestModel(
            eos_data=eos,
            parameters=PsatSimulationRequestModel(
                molar_composition=molar_composition,
                temperature=temperature,
                measured=measured,
                weights=weights,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/psat",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return PsatSimulationResponseModel.model_validate(payload)

    async def run_process(
        self,
        eos: EOSData,
        molar_stream: list[float],
        process: ProcessData,
    ) -> ProcessSimulationResponseModel:
        """Run a surface process simulation asynchronously.

        Args:
            eos: EOS model data to use for simulation.
            molar_stream: Inlet stream in kg-moles per component.
            process: Process definition (tanks, conditions, and routing).

        Returns:
            Per-tank simulation outputs as ProcessSimulationResponseModel.
        """
        request = ProcessInlineRequestModel(
            eos_data=eos,
            parameters=ProcessSimulationRequestModel(
                molar_stream=molar_stream,
                process=process,
            ),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/simulate/process",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        if "process_simulation" in payload:
            return ProcessSimulationResponseModel.model_validate(payload["process_simulation"])
        return ProcessSimulationResponseModel.model_validate(payload)
