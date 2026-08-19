from typing import TYPE_CHECKING

from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.eos_models import DefaultEOSCreateModel, EOSTuneModel, EOSTuneResultModel

if TYPE_CHECKING:
    from ...client.async_client import AsyncClient
    from ...client.sync_client import Client as SyncClient


class EOSDevelopmentManager:
    """Manager for EOS development endpoints.

    Endpoints (planned):
    - POST /eos/default
    - POST /eos/tune
    """

    def __init__(self, client: "SyncClient"):
        self._client = client

    def generate_default_eos(self, input_data: DefaultEOSCreateModel) -> EOSData:
        """Generate a default EOS model.

        Endpoint: POST /eos/default
        """
        response = self._client._request(
            {
                "method": "POST",
                "path": "/eos/default",
                "body": input_data.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return EOSData.model_validate(payload)

    def tune_eos(self, input_data: EOSTuneModel) -> EOSTuneResultModel:
        """Tune an EOS model.

        Endpoint: POST /eos/tune
        """
        response = self._client._request(
            {
                "method": "POST",
                "path": "/eos/tune",
                "body": input_data.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return EOSTuneResultModel.model_validate(payload)


class AsyncEOSDevelopmentManager:
    """Async manager for EOS development endpoints.

    Endpoints (planned):
    - POST /eos/default
    - POST /eos/tune
    """

    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def generate_default_eos(self, input_data: DefaultEOSCreateModel) -> EOSData:
        """Generate a default EOS model asynchronously.

        Endpoint: POST /eos/default
        """
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/eos/default",
                "body": input_data.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return EOSData.model_validate(payload)

    async def tune_eos(self, input_data: EOSTuneModel) -> EOSTuneResultModel:
        """Tune an EOS model asynchronously.

        Endpoint: POST /eos/tune
        """
        response = await self._client._request(
            {
                "method": "POST",
                "path": "/eos/tune",
                "body": input_data.model_dump(),
            }
        )
        payload = self._client._handle_response(response.status_code, response.text, self._client._maybe_json(response))
        return EOSTuneResultModel.model_validate(payload)
