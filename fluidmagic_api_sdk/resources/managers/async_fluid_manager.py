from fluidmagic_api_sdk.models.fluid_models import FluidCreateModel, FluidOverviewModel
from fluidmagic_api_sdk.resources.fluid import FluidAsync
from fluidmagic_api_sdk.resources.managers.async_base_manager import AsyncBaseManager


class AsyncFluidManager(AsyncBaseManager):

    async def list(self, name: str | None = None, component_count: int | None = None) -> list[FluidOverviewModel]:
        """Get a list of Fluid models for this facility.

        Args:
            name: Optional name filter for Fluid models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Fluid models.

        Returns:
            List of Fluid overview models.
        """
        return await FluidAsync._list_resources_async(self._client, self._facility_id, name, component_count)

    async def get(self, fluid_id: str) -> "FluidAsync":
        """Get a specific Fluid model for this facility.

        Args:
            fluid_id: The ID of the Fluid model to retrieve.

        Returns:
            Fluid resource.
        """
        return await FluidAsync._get_resource_async(self._client, self._facility_id, fluid_id)

    async def create(self, create_model: FluidCreateModel) -> "FluidAsync":
        """Create a new Fluid model for this facility.

        Args:
            create_model: The FluidCreateModel instance containing the data for the new Fluid model.

        Returns:
            Fluid resource.
        """
        return await FluidAsync._create_resource_async(self._client, self._facility_id, create_model)

    async def delete(self, fluid_id: str) -> None:
        """Delete a specific Fluid model for this facility.

        Args:
            fluid_id: The ID of the Fluid model to delete.
        """
        await FluidAsync._delete_resource_async(self._client, self._facility_id, fluid_id)
