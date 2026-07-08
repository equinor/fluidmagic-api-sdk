from pydantic import BaseModel, ConfigDict, Field

from fluidmagic_api_sdk.models.config_models import MolesToVolRunInput, RateToMolesRunInput
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.frame_data import FluidLibFrameData, FrameData
from fluidmagic_api_sdk.models.data_models.process_data import ProcessData


class RateToMolesRequestModel(BaseModel):
    """Model for requesting a rate to moles conversion."""

    eos: EOSData = Field(..., description="Data that defines the EOS model to use for conversion.")
    process: ProcessData | None = Field(None, description="Optional process model data to use for conversion.")
    fluid: FluidLibFrameData = Field(..., description="Data that defines the fluid to use for conversion.")
    input_data: RateToMolesRunInput = Field(..., description="Input data for rate-to-moles conversion.")


class MolesToVolumeRequestModel(BaseModel):
    """Model for requesting a moles to volume conversion."""

    eos: EOSData = Field(..., description="Data that defines the EOS model to use for conversion.")
    process: ProcessData = Field(..., description="Data that defines the process model to use for conversion.")
    input_data: MolesToVolRunInput = Field(..., description="Input data for moles-to-vol conversion.")


class LabToEosMolesRequestModel(BaseModel):
    """Model for requesting a lab-to-EOS-moles conversion.

    Converts uncharacterized laboratory compositions (lab_N2, lab_CO2, lab_C1, …,
    lab_Cnp + plus-fraction `MWp` / `Alpha`) into characterized molar compositions
    described by the supplied EOS model. The input is row-indexed (no date column);
    each row represents one lab sample identified by `ID`.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "input_data": {
                    "headers": [
                        "ID",
                        "lab_N2",
                        "lab_CO2",
                        "lab_C1",
                        "lab_C2",
                        "lab_C3",
                        "lab_iC4",
                        "lab_C4",
                        "lab_iC5",
                        "lab_C5",
                        "lab_C6",
                        "lab_C7",
                        "lab_C8",
                        "lab_C9",
                        "lab_C10p",
                        "MWp",
                        "Alpha",
                    ],
                    "units": [
                        "String",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kgmol/d",
                        "kg/kgmol",
                        "Real",
                    ],
                    "index": [1],
                    "data": [
                        [
                            "33_9_12",
                            3.518e-03,
                            3.618e-03,
                            4.2834e-01,
                            7.2763e-02,
                            6.1005e-02,
                            1.0251e-02,
                            3.0854e-02,
                            1.1256e-02,
                            1.6181e-02,
                            2.201e-02,
                            3.3668e-02,
                            4.0e-02,
                            2.4824e-02,
                            2.41712e-01,
                            2.82681e02,
                            1.0e-01,
                        ],
                    ],
                },
                "eos": "<EOSData payload this is retrieved by calling — GET /facilities/{facility_id}/eos/{eos_id}> and then use response.EOSData ",
            }
        },
    )

    eos: EOSData = Field(..., description="Data that defines the EOS model to characterize the lab compositions with.")
    input_data: FrameData = Field(
        ...,
        description=(
            "Uncharacterized lab composition data. Must use an integer row index "
            "(no `date` column); requires `lab_<comp>` columns in kgmol/d plus the "
            "plus-fraction `MWp` (kg/kgmol) and `Alpha` columns."
        ),
    )
