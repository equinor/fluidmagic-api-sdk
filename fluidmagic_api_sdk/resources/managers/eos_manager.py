from fluidmagic_api_sdk.models.eos_models import EOSCreateModel, EOSOverviewModel
from fluidmagic_api_sdk.resources.eos import EOS
from fluidmagic_api_sdk.resources.managers.base_manager import BaseManager


class EOSManager(BaseManager):

    def list(self, name: str | None = None, component_count: int | None = None) -> list[EOSOverviewModel]:
        """Get a list of EOS models for this facility.

        Args:
            name: Optional name filter for EOS models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for EOS models.

        Returns:
            List of EOS overview models.
        """
        return EOS._list_resources(self._client, self._facility_id, name, component_count)

    def get(self, eos_id: str) -> "EOS":
        """Get a specific EOS model for this facility.

        Args:
            eos_id: The ID of the EOS model to retrieve.

        Returns:
            EOS resource.
        """
        return EOS._get_resource(self._client, self._facility_id, eos_id)

    def create(self, eos: "EOSCreateModel") -> "EOS":
        """Create a new EOS model for this facility.

        Args:
            eos: The EOS model to create.

        Returns:
            The created EOS resource.
        """
        return EOS._create_resource(self._client, self._facility_id, eos)

    def delete(self, eos_id: str) -> None:
        """Delete a specific EOS model for this facility.

        Args:
            eos_id: The ID of the EOS model to delete.
        """
        EOS._delete_resource(self._client, self._facility_id, eos_id)
