"""Models for Simulation entities, including Flash Experiment."""

from pydantic import BaseModel, ConfigDict, Field, model_validator

from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.pvt_data import PVTData


class FlashCalculationRequestModel(BaseModel):
    """Model for requesting a flash calculation."""

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(..., description="List of pressures in bara to perform flash calculations at.")
    temperatures: list[float] = Field(..., description="List of temperatures in °C to perform flash calculations at.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [100.0, 200.0, 300.0],
                "temperatures": [60.0, 60.0, 60.0],
            }
        }
    )

    @model_validator(mode="after")
    def validate_simulation_condition_consistency(self):
        """Validate that the simulation conditions have consistent lengths."""
        if len(self.pressures) != len(self.temperatures):
            raise ValueError("Pressures and temperatures must have the same length")

        return self

    def to_pvt_data(self, eos_data: EOSData) -> PVTData:
        return PVTData(
            eos_model=eos_data,
            molarcomp=self.molar_composition,
            temperatures=self.temperatures,
            pressures=self.pressures,
        )
