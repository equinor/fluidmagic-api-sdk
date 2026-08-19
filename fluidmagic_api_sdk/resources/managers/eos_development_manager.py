from typing import TYPE_CHECKING, Any

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

    def generate_default_eos(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a default EOS model.

        Planned endpoint: POST /eos/default
        """
        raise NotImplementedError("generate_default_eos is not implemented yet.")

    def tune_eos(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Tune an EOS model.

        Planned endpoint: POST /eos/tune
        """
        raise NotImplementedError("tune_eos is not implemented yet.")


class AsyncEOSDevelopmentManager:
    """Async manager for EOS development endpoints.

    Endpoints (planned):
    - POST /eos/default
    - POST /eos/tune
    """

    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def generate_default_eos(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a default EOS model asynchronously.

        Planned endpoint: POST /eos/default
        """
        raise NotImplementedError("generate_default_eos is not implemented yet.")

    async def tune_eos(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Tune an EOS model asynchronously.

        Planned endpoint: POST /eos/tune
        """
        raise NotImplementedError("tune_eos is not implemented yet.")
