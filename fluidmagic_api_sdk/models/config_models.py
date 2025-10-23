"""Collection of config entities used in the api."""

from abc import ABC
from enum import auto
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .data_models.frame_data import MolToVolFrameData, RateToMolFrameData
from .enums import NoCasingEnum
from .eos_models import EOSModel, EOSOverviewModel
from .fluid_models import FluidModel, FluidOverviewModel
from .process_models import ProcessModel, ProcessOverviewModel


class ConfigType(NoCasingEnum):
    """Configuration types."""

    RATE_TO_MOLES = auto()
    MOLES_TO_VOL = auto()


class FluidFilterType(NoCasingEnum):
    """Filter types for rate-to-moles conversion results."""

    NET = "net"
    TOTAL = "total"
    ALL = "all"


class ConfigModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of config.")
    description: str = Field(..., description="Description of config.")
    config_type: ConfigType = Field(..., description="Type of config.")
    eos_id: str = Field(..., description="Unique identifier of the EOS model.")
    process_id: str | None = Field(None, description="Unique identifier of the process model.")
    fluid_id: str | None = Field(None, description="Unique identifier of the fluid.")
    created_by: str = Field(..., description="User or application that created config.")
    created_date: str = Field(..., description="Date model was created.")

    @model_validator(mode="after")
    def model_validation(self) -> Self:
        """Run checks after model creation."""
        if self.config_type == ConfigType.RATE_TO_MOLES and self.fluid_id is None:
            raise ValueError("Fluid file is required for RATE_TO_MOLES config type.")
        if self.config_type == ConfigType.MOLES_TO_VOL and self.process_id is None:
            raise ValueError("Process model is required for MOLES_TO_VOL config type.")
        return self

    @staticmethod
    def from_return_model(config_return_model: "ConfigReturnModel") -> "ConfigModel":
        item = config_return_model.model_dump()

        item["eos_id"] = config_return_model.eos.id
        item["process_id"] = config_return_model.process.id if config_return_model.process else None
        item["fluid_id"] = config_return_model.fluid.id if config_return_model.fluid else None

        return ConfigModel(**item)


class ConfigReturnModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of configuration.")
    description: str = Field(..., description="Description of configuration.")
    config_type: ConfigType = Field(..., description="Type of configuration.")
    eos: EOSOverviewModel = Field(..., description="EOS model overview.")
    process: ProcessOverviewModel | None = Field(None, description="Process model overview.")
    fluid: FluidOverviewModel | None = Field(None, description="Unique identifier of the fluid.")
    created_by: str = Field(..., description="User or application that created config.")
    created_date: str = Field(..., description="Date model was created.")

    @staticmethod
    def create_from_models(
        config_model: ConfigModel,
        eos_model: EOSModel,
        process_model: ProcessModel | None,
        fluid_model: FluidModel | None = None,
    ) -> "ConfigReturnModel":
        if config_model.config_type == ConfigType.RATE_TO_MOLES and fluid_model is None:
            raise ValueError("Fluid model is required for RATE_TO_MOLES config type.")
        item = config_model.model_dump()

        item["eos"] = EOSOverviewModel.create_from_eos_model(eos_model).model_dump()

        item["process"] = (
            ProcessOverviewModel.create_from_process_model(process_model).model_dump() if process_model else None
        )
        item["fluid"] = FluidOverviewModel.create_from_fluid_model(fluid_model).model_dump() if fluid_model else None

        return ConfigReturnModel(**item)


class BaseConfigCreateModel(BaseModel, ABC, extra="ignore"):
    name: str = Field(..., description="Name of config.")
    description: str = Field(..., description="Description of config.")
    eos_id: str = Field(..., description="Unique identifier of the EOS model.")


class RateToMolesCreateModel(BaseConfigCreateModel):
    process_id: str | None = Field(None, description="Unique identifier of the process model.")
    fluid_id: str = Field(..., description="Unique identifier of the fluid.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Config 1",
                "description": "Config 1 description",
                "eos_id": "9ae8e4f1-3e70-458e-84d6-547a67958983",
                "process_id": "879ed814-a9e9-41cc-a849-8eb9784b2afe",
                "fluid_id": "14fb137d-5746-4da0-88cd-c7973252f931",
            }
        }
    )


class MolesToVolCreateModel(BaseConfigCreateModel):
    process_id: str = Field(..., description="Unique identifier of the process model.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "facility_id": "facility_1",
                "name": "Config 1",
                "description": "Config 1 description",
                "eos_id": "9ae8e4f1-3e70-458e-84d6-547a67958983",
                "process_id": "879ed814-a9e9-41cc-a849-8eb9784b2afe",
            }
        }
    )


# Type alias for output filter specification in moles-to-vol conversion
OutputFilterDict = dict[str, list[str] | None]


class MolesToVolRunInput(BaseModel):
    """Input and output filter specification for moles-to-vol conversion.

    The `output` field allows specifying outputs to include from each tank. Use tank names as keys and lists of desired
    outputs as values.

    Wildcard Usage:
    - Use "*" as the only item in the list to include all columns associated with a tank. For example, {"OIL1": ["*"]}
    will include all columns for OIL1.
    - You can also use a string ending with "*" (e.g., "net_molarstream_*") to match all columns starting with that
    header. This is mostly used to catch headers suffixed with component names, such as: "net_molarstream_n2",
    "net_molarstream_co2", ...

    Key Features:
    - Specify outputs for each tank using tank names as keys and lists of desired outputs as values.
    - An empty list for a tank will result in no data being included for that tank.
    - The wildcard "*" makes it explicit to include all columns for the specified tank, or all columns starting with a
    given prefix if used as a suffix (e.g., "net_molarstream_*").
    """

    input: MolToVolFrameData
    output: OutputFilterDict | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "input": {
                    "data": [[0.6, 0.3, 0.1]],
                    "headers": ["molarstream_c1", "molarstream_c2", "molarstream_c3"],
                    "index": [],
                    "units": ["kgmol/d", "kgmol/d", "kgmol/d"],
                },
                "output": {
                    "OIL1": ["oil_vol", "oil_mass", "oil_moles"],
                    "GAS1": ["*"],
                    "NGL1": ["ngl_vol", "ngl_mass"],
                    "SEP1": ["net_molarstream_*"],
                },
            }
        }
    )


class RateToMolesRunInput(BaseModel):
    input: RateToMolFrameData
    output: FluidFilterType | None = None
