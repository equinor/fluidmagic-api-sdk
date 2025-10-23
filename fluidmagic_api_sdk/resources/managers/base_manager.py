from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...client.sync_client import Client as SyncClient

from abc import ABC


class BaseManager(ABC):
    def __init__(self, client: "SyncClient", facility_id: str):
        self._client = client
        self._facility_id = facility_id
