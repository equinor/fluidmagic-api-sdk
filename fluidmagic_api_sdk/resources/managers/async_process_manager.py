from fluidmagic_api_sdk.models.process_models import ProcessCreateModel, ProcessOverviewModel
from fluidmagic_api_sdk.resources.managers.async_base_manager import AsyncBaseManager
from fluidmagic_api_sdk.resources.process import ProcessAsync


class AsyncProcessManager(AsyncBaseManager):

    async def list(self, name: str | None = None, component_count: int | None = None) -> list[ProcessOverviewModel]:
        """Get a list of Process models for this facility.

        Args:
            name: Optional name filter for Process models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Process models.

        Returns:
            List of Process overview models.
        """
        return await ProcessAsync._list_resources_async(self._client, self._facility_id, name, component_count)

    async def get(self, process_id: str) -> "ProcessAsync":
        """Get a specific Process model for this facility.

        Args:
            process_id: The ID of the Process model to retrieve.

        Returns:
            Process resource.
        """
        return await ProcessAsync._get_resource_async(self._client, self._facility_id, process_id)

    async def create(self, process: "ProcessCreateModel") -> "ProcessAsync":
        """Create a new Process model for this facility.

        Args:
            process: The Process model to create.

        Returns:
            The created Process resource.
        """
        return await ProcessAsync._create_resource_async(self._client, self._facility_id, process)

    async def delete(self, process_id: str) -> None:
        """Delete a specific Process model for this facility.

        Args:
            process_id: The ID of the Process model to delete.
        """
        await ProcessAsync._delete_resource_async(self._client, self._facility_id, process_id)
