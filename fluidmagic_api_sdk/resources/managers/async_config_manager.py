from fluidmagic_api_sdk.models.config_models import BaseConfigCreateModel, ConfigModel, ConfigType
from fluidmagic_api_sdk.resources.config import ConfigAsync
from fluidmagic_api_sdk.resources.managers.async_base_manager import AsyncBaseManager


class AsyncConfigManager(AsyncBaseManager):

    async def list(
        self, name: str | None = None, component_count: int | None = None, config_type: ConfigType | None = None
    ) -> list[ConfigModel]:
        """Get a list of Config models for this facility.

        Args:
            name: Optional name filter for Config models. Entire or partial name, case insensitive.
            component_count: Optional component count filter for Config models.
            config_type: Optional filter by config type.

        Returns:
            List of Config models.
        """
        return await ConfigAsync._list_resources_async(
            self._client,
            self._facility_id,
            name,
            component_count,
            config_type,
        )

    async def get(self, config_id: str) -> "ConfigAsync":
        """Get a specific Config model for this facility.

        Args:
            config_id: The ID of the Config model to retrieve.

        Returns:
            Config resource.
        """
        return await ConfigAsync._get_resource_async(self._client, self._facility_id, config_id)

    async def create(self, config: "BaseConfigCreateModel") -> "ConfigAsync":
        """Create a new Config model for this facility.

        Args:
            config: The Config model to create.

        Returns:
            The created Config resource.
        """
        return await ConfigAsync._create_resource_async(self._client, self._facility_id, config)

    async def delete(self, config_id: str) -> None:
        """Delete a specific Config model for this facility.

        Args:
            config_id: The ID of the Config model to delete.
        """
        await ConfigAsync._delete_resource_async(self._client, self._facility_id, config_id)
