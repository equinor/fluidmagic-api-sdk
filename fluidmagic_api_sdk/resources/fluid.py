from typing import Any, ClassVar

from pydantic import BaseModel

from fluidmagic_api_sdk.models.fluid_models import FluidCreateModel, FluidModel, FluidOverviewModel
from fluidmagic_api_sdk.resources.base import BaseConfigResource


class Fluid(FluidModel, BaseConfigResource):
    _list_model: ClassVar[BaseModel] = FluidOverviewModel

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
            "path": f"/facilities/{facility_id}/fluids",
            "params": params if params else None,
        }

    @classmethod
    def _build_get_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "GET",
            "path": f"/facilities/{facility_id}/fluids/{id}",
        }

    @classmethod
    def _build_create_request(self, facility_id: str, create_model: FluidCreateModel) -> dict[str, Any]:
        return {
            "method": "POST",
            "path": f"/facilities/{facility_id}/fluids",
            "body": create_model.model_dump(),
        }

    @classmethod
    def _build_delete_request(cls, facility_id: str, id: str) -> dict[str, Any]:
        return {
            "method": "DELETE",
            "path": f"/facilities/{facility_id}/fluids/{id}",
        }

    # ======== Public API methods ========= #

    def delete(self) -> None:
        """Delete this Fluid model."""
        Fluid._delete_resource(self._client, self.facility_id, self.id)
