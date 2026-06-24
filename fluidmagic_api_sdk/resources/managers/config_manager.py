from fluidmagic_api_sdk.models.config_models import ConfigModel, MolesToVolCreateModel, RateToMolesCreateModel
from fluidmagic_api_sdk.resources.config import Config
from fluidmagic_api_sdk.resources.managers.base_manager import BaseManager


class ConfigManager(BaseManager):

    def list(self, name: str | None = None, component_count: int | None = None) -> list[ConfigModel]:
        """Get a list of Config models for this facility.

        Args:
            name: Optional name filter for Config models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Config models.

        Returns:
            List of Config models.
        """
        return Config._list_resources(self._client, self._facility_id, name, component_count)

    def get(self, config_id: str) -> "Config":
        """Get a specific Config model for this facility.

        Args:
            config_id: The ID of the Config model to retrieve.

        Returns:
            Config resource.
        """
        return Config._get_resource(self._client, self._facility_id, config_id)

    def create_rate_to_moles(self, config_model: RateToMolesCreateModel) -> "Config":
        """Create a new Rate to Moles Config model for this facility.

        Args:
            config_model: The configuration model for the new Config.

        Returns:
            The created Config resource.
        """
        return Config._create_resource(self._client, self._facility_id, config_model)

    def create_moles_to_vol(self, config_model: MolesToVolCreateModel) -> "Config":
        """Create a new Moles to Volume Config model for this facility.

        Args:
            config_model: The configuration model for the new Config.

        Returns:
            The created Config resource.
        """
        return Config._create_resource(self._client, self._facility_id, config_model)

    def delete(self, config_id: str) -> None:
        """Delete a specific Config model for this facility.

        Args:
            config_id: The ID of the Config model to delete.
        """
        Config._delete_resource(self._client, self._facility_id, config_id)
