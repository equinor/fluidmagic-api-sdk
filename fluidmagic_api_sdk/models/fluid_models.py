"""Models for Fluid entities."""

from pydantic import BaseModel, ConfigDict, Field

from .data_models.frame_data import FluidLibFrameData


class FluidCreateModel(BaseModel):
    """Model for creating a new fluid entry."""

    fluid: FluidLibFrameData = Field(..., description=FluidLibFrameData.__doc__)
    name: str = Field(..., description="Name of the fluid.")
    description: str | None = Field(None, description="Description of the fluid.")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Black Oil Sample",
                "description": "Reservoir fluid composition sample",
                "fluid": {
                    "headers": [
                        "fluid_id",
                        "reservoir_temp",
                        "experiment-type",
                        "molarstream_n2",
                        "molarstream_co2",
                        "molarstream_c1",
                    ],
                    "units": ["string", "c", "string", "kgmol/d", "kgmol/d", "kgmol/d"],
                    "index": [0],
                    "data": [["fluid1", 90, "cme", 0.351757, 0.361807, 42.834]],
                },
            }
        }
    )


class FluidModel(BaseModel):
    """Model for fluid data."""

    id: str = Field(..., description="Unique identifier of the fluid.")
    facility_id: str = Field(..., description="Identifier of the facility.")
    name: str = Field(..., description="Name of the fluid.")
    description: str | None = Field(None, description="Description of the fluid.")
    fluid: FluidLibFrameData = Field(..., description="Fluid data model containing headers, units, index, and data.")
    created_by: str = Field(..., description="User who created the fluid model.")
    created_date: str = Field(..., description="Date the fluid model was created.")

    def get_component_names(self) -> list[str]:
        """Get a list of unique components in the fluid model."""
        return self.fluid.get_component_names()

    def get_component_count(self) -> int:
        """Get the number of components in the fluid model."""
        return self.fluid.get_component_count()


class FluidReturnModel(BaseModel):
    """Model for returning fluid data."""

    id: str = Field(..., description="Unique identifier of the fluid.")
    facility_id: str = Field(..., description="Identifier of the facility.")
    name: str = Field(..., description="Name of the fluid.")
    description: str | None = Field(None, description="Description of the fluid.")
    headers: list[str] = Field(..., description="List of headers.")
    fluid_names: list[str] = Field(..., description="List of unique fluid names.")
    component_count: int = Field(..., description="Number of components.")
    component_names: list[str] = Field(..., description="List of component names.")
    fluid: FluidLibFrameData = Field(..., description="Fluid data model containing headers, units, index, and data.")
    created_by: str = Field(..., description="User who created the fluid model.")
    created_date: str = Field(..., description="Date the fluid model was created.")

    @classmethod
    def create_from_fluid_model(cls, fluid_model: FluidModel) -> "FluidReturnModel":
        """Construct a FluidReturnModel from a FluidModel."""
        return cls(
            id=fluid_model.id,
            facility_id=fluid_model.facility_id,
            name=fluid_model.name,
            description=fluid_model.description,
            headers=fluid_model.fluid.headers,
            fluid_names=fluid_model.fluid.get_fluid_names(),
            component_count=fluid_model.get_component_count(),
            component_names=fluid_model.get_component_names(),
            fluid=fluid_model.fluid,
            created_by=fluid_model.created_by,
            created_date=fluid_model.created_date,
        )


class FluidOverviewModel(BaseModel):
    """Model for returning a summary of fluid data."""

    id: str = Field(..., description="Unique identifier of the fluid.")
    name: str = Field(..., description="Name of the fluid.")
    description: str | None = Field(None, description="Description of the fluid.")
    headers: list[str] = Field(..., description="List of headers in the fluid data.")
    fluid_names: list[str] | list[None] = Field(default_factory=list, description="List of unique fluid names.")
    component_count: int = Field(..., description="Number of components.")
    component_names: list[str] = Field(..., description="List of component names.")

    @classmethod
    def create_from_fluid_model(cls, fluid_model: FluidModel) -> "FluidOverviewModel":
        """Construct a FluidOverviewModel from a FluidModel."""
        return cls(
            id=fluid_model.id,
            name=fluid_model.name,
            headers=fluid_model.fluid.headers,
            fluid_names=fluid_model.fluid.get_fluid_names(),
            component_count=fluid_model.get_component_count(),
            component_names=fluid_model.get_component_names(),
            description=fluid_model.description,
        )
