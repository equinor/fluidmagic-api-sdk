from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client.async_client import AsyncClient

from abc import ABC


class AsyncBaseManager(ABC):
    def __init__(self, client: "AsyncClient", facility_id: str):
        self._client = client
        self._facility_id = facility_id
