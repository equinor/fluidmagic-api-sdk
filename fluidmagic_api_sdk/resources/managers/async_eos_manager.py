from fluidmagic_api_sdk.models.eos_models import EOSCreateModel, EOSOverviewModel
from fluidmagic_api_sdk.resources.eos import EOSAsync
from fluidmagic_api_sdk.resources.managers.async_base_manager import AsyncBaseManager


class AsyncEOSManager(AsyncBaseManager):

    async def list(self, name: str | None = None, component_count: int | None = None) -> list[EOSOverviewModel]:
        """Get a list of EOS models for this facility.

        Args:
            name: Optional name filter for EOS models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for EOS models.

        Returns:
            List of EOS overview models.
        """
        return await EOSAsync._list_resources_async(self._client, self._facility_id, name, component_count)

    async def get(self, eos_id: str) -> "EOSAsync":
        """Get a specific EOS model for this facility.

        Args:
            eos_id: The ID of the EOS model to retrieve.

        Returns:
            EOS resource.
        """
        return await EOSAsync._get_resource_async(self._client, self._facility_id, eos_id)

    async def create(self, eos: "EOSCreateModel") -> "EOSAsync":
        """Create a new EOS model for this facility.

        Args:
            eos: The EOS model to create.

        Returns:
            The created EOS resource.
        """
        return await EOSAsync._create_resource_async(self._client, self._facility_id, eos)

    async def delete(self, eos_id: str) -> None:
        """Delete a specific EOS model for this facility.

        Args:
            eos_id: The ID of the EOS model to delete.
        """
        await EOSAsync._delete_resource_async(self._client, self._facility_id, eos_id)
