from typing import TYPE_CHECKING

from fluidmagic_api_sdk.models.config_models import (
    FluidFilterType,
    MolesToVolRunInput,
    OutputFilterDict,
    RateToMolesRunInput,
)
from fluidmagic_api_sdk.models.convert_models import (
    LabToEosMolesRequestModel,
    LabToEosMolesResponseModel,
    MolesToVolumeRequestModel,
    RateToMolesRequestModel,
)
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.frame_data import (
    FluidLibFrameData,
    FrameData,
    MolToVolFrameData,
    RateToMolFrameData,
)
from fluidmagic_api_sdk.models.data_models.process_data import ProcessData

if TYPE_CHECKING:
    from ...client.async_client import AsyncClient
    from ...client.sync_client import Client as SyncClient


class ConversionsManager:
    def __init__(self, client: "SyncClient"):
        self._client = client

    def run_rate_to_moles(
        self,
        eos: EOSData,
        fluid: FluidLibFrameData,
        input: RateToMolFrameData,
        output: FluidFilterType = FluidFilterType.ALL,
        process: ProcessData | None = None,
    ) -> FrameData:
        """Run an inline Rate to Moles conversion without requiring pre-uploaded resources.

        Args:
            eos: EOS model data to use for conversion.
            fluid: Fluid data to use for conversion.
            input: Rate data to convert.
            output: Filter type for the conversion output. Defaults to ALL.
            process: Optional process model data to use for conversion.

        Returns:
            The conversion results as FrameData.
        """
        request = RateToMolesRequestModel(
            eos=eos,
            process=process,
            fluid=fluid,
            input_data=RateToMolesRunInput(input=input, output=output),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/convert/rate-to-moles",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FrameData.model_validate(payload)

    def run_moles_to_volume(
        self,
        eos: EOSData,
        process: ProcessData,
        input: MolToVolFrameData,
        output: OutputFilterDict | None = None,
    ) -> FrameData:
        """Run an inline Moles to Volume conversion without requiring pre-uploaded resources.

        Args:
            eos: EOS model data to use for conversion.
            process: Process model data to use for conversion.
            input: Molar data to convert.
            output: Optional output filter specifying which tank outputs to include.

        Returns:
            The conversion results as FrameData.
        """
        request = MolesToVolumeRequestModel(
            eos=eos,
            process=process,
            input_data=MolesToVolRunInput(input=input, output=output),
        )
        response = self._client._request(
            {
                "method": "POST",
                "path": "/convert/moles-to-volume",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FrameData.model_validate(payload)

    def run_characterize_fluid_to_eos(
        self,
        eos: EOSData,
        input_data: FrameData,
    ) -> LabToEosMolesResponseModel:
        """Run an inline lab-to-EOS-moles characterization without requiring pre-uploaded resources.

        Converts uncharacterized laboratory compositions into characterized molar compositions.

        Args:
            eos: EOS model data to characterize the lab compositions with.
            input_data: Lab composition data with lab_* columns plus MWp and Alpha columns.

        Returns:
            The characterized composition results as LabToEosMolesResponseModel.
        """
        request = LabToEosMolesRequestModel(eos=eos, input_data=input_data)
        response = self._client._request(
            {
                "method": "POST",
                "path": "/convert/characterize-fluid-to-eos",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return LabToEosMolesResponseModel.model_validate(payload)


class AsyncConversionsManager:
    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def run_rate_to_moles(
        self,
        eos: EOSData,
        fluid: FluidLibFrameData,
        input: RateToMolFrameData,
        output: FluidFilterType = FluidFilterType.ALL,
        process: ProcessData | None = None,
    ) -> FrameData:
        """Run an inline Rate to Moles conversion without requiring pre-uploaded resources.

        Args:
            eos: EOS model data to use for conversion.
            fluid: Fluid data to use for conversion.
            input: Rate data to convert.
            output: Filter type for the conversion output. Defaults to ALL.
            process: Optional process model data to use for conversion.

        Returns:
            The conversion results as FrameData.
        """
        request = RateToMolesRequestModel(
            eos=eos,
            process=process,
            fluid=fluid,
            input_data=RateToMolesRunInput(input=input, output=output),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/convert/rate-to-moles",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FrameData.model_validate(payload)

    async def run_characterize_fluid_to_eos(
        self,
        eos: EOSData,
        input_data: FrameData,
    ) -> FrameData:
        """Run an inline lab-to-EOS-moles characterization without requiring pre-uploaded resources.

        Converts uncharacterized laboratory compositions into characterized molar compositions.

        Args:
            eos: EOS model data to characterize the lab compositions with.
            input_data: Lab composition data with lab_* columns plus MWp and Alpha columns.

        Returns:
            The characterized composition results as FrameData.
        """
        request = LabToEosMolesRequestModel(eos=eos, input_data=input_data)
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/convert/characterize-fluid-to-eos",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FrameData.model_validate(payload["characterized_fluid"])

    async def run_moles_to_volume(
        self,
        eos: EOSData,
        process: ProcessData,
        input: MolToVolFrameData,
        output: OutputFilterDict | None = None,
    ) -> FrameData:
        """Run an inline Moles to Volume conversion without requiring pre-uploaded resources.

        Args:
            eos: EOS model data to use for conversion.
            process: Process model data to use for conversion.
            input: Molar data to convert.
            output: Optional output filter specifying which tank outputs to include.

        Returns:
            The conversion results as FrameData.
        """
        request = MolesToVolumeRequestModel(
            eos=eos,
            process=process,
            input_data=MolesToVolRunInput(input=input, output=output),
        )
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/convert/moles-to-volume",
                "body": request.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return FrameData.model_validate(payload)
