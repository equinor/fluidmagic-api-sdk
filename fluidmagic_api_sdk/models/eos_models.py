"""Collection of EOS entities used in the api."""

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from fluidmagic_api_sdk.models.enums import CriticalVolumeOption, EOSType, LumpingOption
from fluidmagic_api_sdk.models.simulate_models import (
    CMESimulationRequestModel,
    CVDSimulationRequestModel,
    DLESimulationRequestModel,
    FlashSimulationRequestModel,
    PsatSimulationRequestModel,
    SEPSimulationRequestModel,
)

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


class EOSOverviewModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    eos_type: str = Field(..., description="The type of equation of state used.")
    component_count: int = Field(..., description="Number of components.")
    component_names: list[str] = Field(..., description="Component names. N2, CO2, C1,...")
    molecular_weights: list[float] = Field(..., description="Molecular weights.")


class DefaultEOSCreateModel(BaseModel):
    """Request body for generating a default (characterized) EOS.

    Wraps `fluidmagic.eoslib.characterization.EosChar`. `eos_name`, `eos_type`,
    `plus_fraction_molecular_weight`, and `plus_fraction_density` are required;
    all other fields use the same defaults as `EosChar.__init__`.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "eos_name": "default_srk",
                "eos_type": "SRK",
                "plus_fraction_molecular_weight": 220.0,
                "plus_fraction_density": 850.0,
                "plus_fraction_carbon_number": 7,
                "number_of_pseudo_fractions": 5,
                "plus_lumping_option": "gaussian_quadrature",
                "plus_critical_volumes_option": "katz_firoozabadi",
            }
        },
    )

    eos_name: str = Field(..., description="Name of the generated EOS characterization.")
    eos_type: EOSType = Field(..., description="EOS type.")
    plus_fraction_molecular_weight: float = Field(
        ..., ge=100.0, le=500.0, description="Molecular weight of the plus fraction [kg/kgmol]."
    )
    plus_fraction_density: float = Field(..., ge=650.0, le=1000.0, description="Density of the plus fraction [kg/m3].")
    plus_fraction_carbon_number: int = Field(7, ge=7, le=10, description="Carbon number of the plus fraction (7..10).")
    number_of_pseudo_fractions: int = Field(5, ge=2, le=70, description="Number of lumped pseudo components (2..70).")
    plus_fraction_gamma_parameters: tuple[float, float] | None = Field(
        None, description="Optional (alpha, mw0) for the gamma distribution. Defaults are used when omitted."
    )
    plus_lumping_option: LumpingOption = Field(
        LumpingOption.GAUSSIAN_QUADRATURE, description="Method used to lump plus pseudo-fractions."
    )
    plus_critical_volumes_option: CriticalVolumeOption = Field(
        CriticalVolumeOption.KATZ_FIROOZABADI,
        description="Method used to compute pseudo-component critical volumes.",
    )
    acentric_factor_matching_boiling_temperature: bool | None = Field(
        None,
        description=(
            "If True, adjusts pseudo-component acentric factors to match boiling temperatures. "
            "Defaults to True for PR and False otherwise."
        ),
    )


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


class _BaseTuneSimulationItem(BaseModel):
    """Shared plumbing for tune simulation items."""

    model_config = ConfigDict(extra="forbid")


class FlashTuneItem(_BaseTuneSimulationItem):
    name: Literal["flash"] = Field(..., description="Simulation type discriminator.")
    parameters: FlashSimulationRequestModel = Field(
        ..., description="Flash simulation request used to build the experiment."
    )


class CMETuneItem(_BaseTuneSimulationItem):
    name: Literal["cme"] = Field(..., description="Simulation type discriminator.")
    parameters: CMESimulationRequestModel = Field(
        ..., description="CME simulation request used to build the experiment."
    )


class CVDTuneItem(_BaseTuneSimulationItem):
    name: Literal["cvd"] = Field(..., description="Simulation type discriminator.")
    parameters: CVDSimulationRequestModel = Field(
        ..., description="CVD simulation request used to build the experiment."
    )


class DLETuneItem(_BaseTuneSimulationItem):
    name: Literal["dle"] = Field(..., description="Simulation type discriminator.")
    parameters: DLESimulationRequestModel = Field(
        ..., description="DLE simulation request used to build the experiment."
    )


class SEPTuneItem(_BaseTuneSimulationItem):
    name: Literal["sep"] = Field(..., description="Simulation type discriminator.")
    parameters: SEPSimulationRequestModel = Field(
        ..., description="Separator simulation request used to build the experiment."
    )


class PsatTuneItem(_BaseTuneSimulationItem):
    name: Literal["psat"] = Field(..., description="Simulation type discriminator.")
    parameters: PsatSimulationRequestModel = Field(
        ..., description="Saturation-pressure simulation request used to build the experiment."
    )


# Discriminated union — FastAPI / Pydantic v2 select the right item by the `name` field.
TuneSimulationItem = Annotated[
    Union[FlashTuneItem, CMETuneItem, CVDTuneItem, DLETuneItem, SEPTuneItem, PsatTuneItem],
    Field(discriminator="name"),
]


class EOSTuneModel(BaseModel):
    """Request body for the EOS-tuning endpoint.

    The endpoint takes the EOS to tune directly from `eos_data`, builds a PVT
    experiment from each entry in `simulations` and passes the whole list to
    `fluidmagic.eoslib.regression.tune_eos` in a single combined regression
    that minimises the sum-of-squares across every experiment at once.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "method_preset": "mix_1",
                "eos_data": {
                    "eos_type": "SRK",
                    "component_names": ["N2", "CO2", "C1", "C2", "C3", "C4+"],
                    "critical_temperatures": [126.2, 304.2, 190.6, 305.4, 369.8, 425.2],
                    "critical_pressures": [33.9, 73.8, 45.99, 48.72, 41.94, 37.96],
                    "acentric_factors": [0.04, 0.225, 0.008, 0.098, 0.152, 0.199],
                    "binary_interaction_parameters": [[0.0] * 6 for _ in range(6)],
                    "volume_shifts": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                    "molecular_weights": [28.01, 44.01, 16.04, 30.07, 44.1, 58.12],
                },
                "simulations": [
                    {
                        "name": "psat",
                        "parameters": {
                            "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                            "temperature": 100.0,
                            "measured": {"saturation_pressure": 113.4},
                            "weights": {"saturation_pressure": 1.0},
                        },
                    },
                    {
                        "name": "flash",
                        "parameters": {
                            "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                            "pressures": [100.0, 50.0],
                            "temperatures": [100.0, 30.0],
                            "measured": {
                                "gas_oil_ratio": [84.62648865, 707.617734],
                                "oil_density": [707.6, 766.5],
                                "gas_density": [84.6, 44.0],
                            },
                            "weights": {"gas_oil_ratio": 1.0, "oil_density": 1.0, "gas_density": 1.0},
                        },
                    },
                ],
            }
        },
    )

    eos_data: EOSData = Field(..., description="EOS model to tune. Supplied by the caller; not persisted.")
    method_preset: Literal[
        "critical_pressure_temperature",
        "critical_pressure_temperature_all",
        "omegas",
        "acentric_factor",
        "liquid_density",
        "molecular_weight",
        "molecular_weight_all",
        "binary_interaction_parameter",
        "mix_1",
        "mix_2",
        "mix_3",
        "mix_4",
        "all",
    ] = Field(
        "mix_1",
        description=(
            "Name of a `fluidmagic.eoslib.regression.methods.Presets` preset that "
            "selects which EOS parameters the regression is allowed to modify."
        ),
    )
    simulations: list[TuneSimulationItem] = Field(
        ...,
        min_length=1,
        description="Ordered list of simulations to tune the EOS against.",
    )


class EOSTuneResultModel(BaseModel):
    """Response body for the EOS-tuning endpoint."""

    initial_sum_of_squares: float = Field(
        ..., description="Weighted sum-of-squares across all experiments before tuning."
    )
    final_sum_of_squares: float = Field(
        ..., description="Weighted sum-of-squares across all experiments after the last regression pass."
    )
    improvement: float = Field(
        ...,
        description=("`1 - final_ssq / initial_ssq`. 0 means no improvement, 1 means the residual was driven to zero."),
    )
    parameters_used: list[float] = Field(
        ..., description="Optimal regression parameters returned by the last `tune_eos` pass."
    )
    tuned_eos_data: EOSData = Field(..., description="EOS data after tuning (not persisted).")
