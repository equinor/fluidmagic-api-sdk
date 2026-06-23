from fluidmagic_api_sdk.models.process_models import ProcessCreateModel, ProcessOverviewModel
from fluidmagic_api_sdk.resources.managers.base_manager import BaseManager
from fluidmagic_api_sdk.resources.process import Process


class ProcessManager(BaseManager):

    def list(self, name: str | None = None, component_count: int | None = None) -> list[ProcessOverviewModel]:
        """Get a list of Process models for this facility.

        Args:
            name: Optional name filter for Process models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Process models.

        Returns:
            List of Process resources.
        """
        return Process._list_resources(self._client, self._facility_id, name, component_count)

    def get(self, process_id: str) -> "Process":
        """Get a specific Process model for this facility.

        Args:
            process_id: The ID of the Process model to retrieve.

        Returns:
            Process resource.
        """
        return Process._get_resource(self._client, self._facility_id, process_id)

    def create(self, process: "ProcessCreateModel") -> "Process":
        """Create a new Process model for this facility.

        Args:
            process: The Process model to create.

        Returns:
            The created Process resource.
        """
        return Process._create_resource(self._client, self._facility_id, process)

    def delete(self, process_id: str) -> None:
        """Delete a specific Process model for this facility.

        Args:
            process_id: The ID of the Process model to delete.
        """
        Process._delete_resource(self._client, self._facility_id, process_id)
