from pydantic import BaseModel, model_validator

from .eos_data import EOSData


class PVTData(BaseModel):
    """Model containing PVT simulation parameters."""

    eos_model: EOSData
    molarcomp: list[float]
    temperatures: list[float]
    pressures: list[float]
    measured: dict[str, list[float]] | None = None
    weights: dict[str, float] | None = None

    @property
    def stages(self) -> int:
        return len(self.temperatures)

    @model_validator(mode="after")
    def model_validation(self):
        if len(self.temperatures) != len(self.pressures):
            raise ValueError("Inconsistent stage count on input data.")
        if len(self.molarcomp) != len(self.eos_model.component_names):
            raise ValueError("Component count in molar composition does not match EOS model.")
        return self
