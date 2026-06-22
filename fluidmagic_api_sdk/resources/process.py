from typing import Any, ClassVar

from pydantic import BaseModel

from fluidmagic_api_sdk.models.process_models import ProcessCreateModel, ProcessModel, ProcessOverviewModel
from fluidmagic_api_sdk.resources.base import BaseConfigResource


class Process(ProcessModel, BaseConfigResource):
    _list_model: ClassVar[BaseModel] = ProcessOverviewModel

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
            "path": f"/facilities/{facility_id}/processes",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/processes/{id}",
        }

    @classmethod
    def _build_create_request(cls, facility_id: str, process_model: ProcessCreateModel) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/processes",
            "body": process_model.model_dump(),
        }

    @classmethod
    def _build_delete_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "DELETE",
            "path": f"/facilities/{facility_id}/processes/{id}",
        }

    # ======== Public API methods ========= #

    def delete(self) -> None:
        """Delete this Process model."""
        Process._delete_resource(self._client, self.facility_id, self.id)
