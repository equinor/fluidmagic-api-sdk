from pydantic import BaseModel, ConfigDict, Field

from fluidmagic_api_sdk.models.config_models import MolesToVolRunInput, RateToMolesRunInput
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.frame_data import FluidLibFrameData, FrameData
from fluidmagic_api_sdk.models.data_models.process_data import ProcessData
from fluidmagic_api_sdk.models.enums import MoleOrMass


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


class VolumeToMolesRequestModel(BaseModel):
    """Model for requesting an inline volume-to-moles conversion.

    All models required by the converter (EOS, process, BOC tables) are
    supplied directly in the request payload; nothing is read from the
    database.
    """

    eos: EOSData = Field(..., description="Data that defines the EOS model to use for conversion.")
    process: ProcessData = Field(..., description="Data that defines the process model to use for conversion.")
    boc: FrameData = Field(
        ...,
        description=(
            "Black-oil to compositional (BOC) PVT tables. Rows are grouped by "
            "`pvtnum`; each group carries saturation pressure, oil/gas formation "
            "volume factors, solution GOR/OGR, densities and per-component molar "
            "compositions (headers starting with `x` and `y`, or `oil-` and `gas-`)."
        ),
    )
    input_data: FrameData = Field(
        ...,
        description=(
            "Stream frame carrying per-well production volumes. Must include at least "
            "a `well` identifier, a `pvtnum` column matching the BOC tables, and "
            "`oil_vol` / `gas_vol` in `sm3/d`. Additional columns such as `water_vol`, "
            "`reservoir_pres`, `injtrace_fraction` and `avg_ginj` are consumed by the "
            "converter when present."
        ),
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "eos": {},
                "process": {},
                "boc": {
                    "headers": [
                        "pvtnum",
                        "psat",
                        "temperature",
                        "gor",
                        "bo",
                        "oil_density",
                        "gas_density",
                        "x_c1",
                        "x_c2",
                        "x_c3",
                        "y_c1",
                        "y_c2",
                        "y_c3",
                    ],
                    "units": [
                        "integer",
                        "bar",
                        "c",
                        "sm3/sm3",
                        "rm3/sm3",
                        "kg/m3",
                        "kg/m3",
                        "real",
                        "real",
                        "real",
                        "real",
                        "real",
                        "real",
                    ],
                    "index": [0],
                    "data": [[1, 250.0, 90.0, 180.0, 1.35, 720.0, 1.2, 0.55, 0.25, 0.20, 0.85, 0.10, 0.05]],
                },
                "input_data": {
                    "headers": [
                        "date",
                        "well",
                        "pvtnum",
                        "oil_vol",
                        "gas_vol",
                        "water_vol",
                        "reservoir_pres",
                    ],
                    "units": ["date", "string", "integer", "sm3/d", "sm3/d", "sm3/d", "bar"],
                    "index": ["2021-01-11 00:00:00"],
                    "data": [["2021-01-11 00:00:00", "prod-1", 1, 278.75, 40749.5, 1721.25, 311.44]],
                },
            }
        }
    )


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


class LabToEosMolesResponseModel(BaseModel):
    """Separated response for lab-to-EOS conversion.

    Keeps the original input payload untouched and returns the converted
    EOS-basis molar stream in a dedicated field for easier extraction.
    """

    input_data: FrameData = Field(..., description="Original uncharacterized lab composition payload.")
    characterized_fluid: FrameData = Field(
        ...,
        description="Converted EOS-basis molar stream (only `molarstream_*` columns).",
    )


class MolesToMassRequestModel(BaseModel):
    """Model for requesting a moles-to-mass (or mass-to-moles) conversion using an inline EOS.

    The `convert_method` field selects the direction:

    - `mole_to_mass` — convert molar streams (kgmol/d) to mass streams (kg/d).
    - `mass_to_mole` — convert mass streams (kg/d) to molar streams (kgmol/d).

    The input frame's composition columns must match the EOS components and must
    be prefixed `molarstream_` for both directions. Units determine interpretation:
    `kgmol/d` for `mole_to_mass` inputs and `kg/d` for `mass_to_mole` inputs.
    """

    model_config = ConfigDict(extra="forbid")

    eos: EOSData = Field(..., description="EOS model whose components describe the stream composition.")
    input_data: FrameData = Field(
        ...,
        description=(
            "Stream frame to convert. Component columns must be prefixed "
            "`molarstream_` for both directions. Use `kgmol/d` values for "
            "`mole_to_mass` inputs and `kg/d` values for `mass_to_mole` inputs. "
            "Column names after the prefix must match the components of `eos`."
        ),
    )
    convert_method: MoleOrMass = Field(
        MoleOrMass.MOLE_TO_MASS,
        description=(
            "Direction of the conversion. `mole_to_mass` converts molar streams "
            "(kgmol/d) to mass streams (kg/d); `mass_to_mole` converts mass streams "
            "(kg/d) to molar streams (kgmol/d). Defaults to `mole_to_mass`."
        ),
    )
