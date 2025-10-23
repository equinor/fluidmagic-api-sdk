"""Collection of EOS entities used in the api."""

from pydantic import BaseModel, ConfigDict, Field

from .data_models.eos_data import EOSData


class EOSModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    eos_data: EOSData = Field(..., description="Data that defines the EOS model.")
    created_by: str = Field(..., description="User or application that created model.")
    created_date: str = Field(..., description="Date model was created.")

    def get_component_count(self) -> int:
        """Get the number of components in the EOS model."""
        return len(self.eos_data.component_names)


class EOSReturnModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    eos_type: str = Field(..., description="The type of equation of state used.")
    component_count: int = Field(..., description="Number of components.")
    component_names: list[str] = Field(..., description="Component names. N2, CO2, C1,...")
    molecular_weights: list[float] = Field(..., description="Molecular weights.")
    eos_data: EOSData = Field(..., description="Data that defines the EOS model.")
    created_by: str = Field(..., description="User or application that created model.")
    created_date: str = Field(..., description="Date model was created.")

    @staticmethod
    def create_from_eos_model(eos_model: "EOSModel") -> "EOSReturnModel":
        item = eos_model.model_dump()

        item["eos_type"] = eos_model.eos_data.eos_type
        item["component_count"] = eos_model.get_component_count()
        item["component_names"] = [name.lower() for name in eos_model.eos_data.component_names]
        item["molecular_weights"] = eos_model.eos_data.molecular_weights

        return EOSReturnModel(**item)


class EOSOverviewModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    eos_type: str = Field(..., description="The type of equation of state used.")
    component_count: int = Field(..., description="Number of components.")
    component_names: list[str] = Field(..., description="Component names. N2, CO2, C1,...")
    molecular_weights: list[float] = Field(..., description="Molecular weights.")

    @staticmethod
    def create_from_eos_model(eos_model: "EOSModel") -> "EOSOverviewModel":
        item = eos_model.model_dump()

        item["eos_type"] = eos_model.eos_data.eos_type
        item["component_count"] = eos_model.get_component_count()
        item["component_names"] = [name.lower() for name in eos_model.eos_data.component_names]
        item["molecular_weights"] = eos_model.eos_data.molecular_weights

        return EOSOverviewModel(**item)


class EOSCreateModel(BaseModel, extra="ignore"):
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    eos_data: EOSData = Field(..., description="Data that defines the EOS model.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "eos_model_1",
                "description": "Example minimal EOS model.",
                "eos_data": {
                    "eos_type": "SRK",
                    "component_names": ["C1", "C2", "C3-C4"],
                    "critical_temperatures": [190.6, 305.4, 369.8],
                    "critical_pressures": [45.99, 48.72, 41.94],
                    "acentric_factors": [0.00, 0.0, 0.0],
                    "binary_interaction_parameters": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                    "volume_shifts": [0.0, 0.0, 0.0],
                    "molecular_weights": [16.04, 30.07, 44.1],
                },
            }
        }
    )
