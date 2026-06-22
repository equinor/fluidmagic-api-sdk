from fluidmagic_api_sdk.models.fluid_models import FluidCreateModel
from fluidmagic_api_sdk.resources.fluid import Fluid
from fluidmagic_api_sdk.resources.managers.base_manager import BaseManager


class FluidManager(BaseManager):
    def list(self, name: str | None = None, component_count: int | None = None) -> list["Fluid"]:
        """Get a list of Fluid models for this facility.

        Args:
            name: Optional name filter for Fluid models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Fluid models.

        Returns:
            List of Fluid resources.
        """
        return Fluid._list_resources(self._client, self._facility_id, name, component_count)

    def get(self, fluid_id: str) -> "Fluid":
        """Get a specific Fluid model for this facility.

        Args:
            fluid_id: The ID of the Fluid model to retrieve.

        Returns:
            Fluid resource.
        """
        return Fluid._get_resource(self._client, self._facility_id, fluid_id)

    def create(self, create_model: FluidCreateModel) -> "Fluid":
        """Create a new Fluid model for this facility.

        Args:
            create_model: The FluidCreateModel instance containing the data for the new Fluid model.

        Returns:
            Fluid resource.
        """
        return Fluid._create_resource(self._client, self._facility_id, create_model)

    def delete(self, fluid_id: str) -> None:
        """Delete a specific Fluid model for this facility.

        Args:
            fluid_id: The ID of the Fluid model to delete.
        """
        Fluid._delete_resource(self._client, self._facility_id, fluid_id)
