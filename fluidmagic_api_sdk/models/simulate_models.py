"""Models for Simulation entities, including Flash Experiment."""

from typing import Annotated, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

from fluidmagic_api_sdk.models.constants.headers import PVTHeaders
from fluidmagic_api_sdk.models.data_models.calculated import FlashCalculated, SaturationPressureCalculated
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.data_models.process_data import ProcessData
from fluidmagic_api_sdk.models.data_models.pvt_data import PVTData

# Sentinel strings accepted in measured-value lists to mean "no measurement at
# this stage". They are coerced to None on input, and `_build_measured_dict`
# then turns the resulting None into NaN, which fluidmagic's regression layer
# already skips via `np.isnan(...)`. This lets callers send the magic-file
# convention (`"*"`) or the human-friendly string `"null"` instead of JSON
# `null`.
_NULL_SENTINELS: frozenset[str] = frozenset({"null", "*"})


def _coerce_null_sentinels(value):
    """Map sentinel strings in a list to None so float validation still passes."""
    if isinstance(value, list):
        return [None if isinstance(item, str) and item.strip().lower() in _NULL_SENTINELS else item for item in value]
    return value


# Reusable type for an optional per-stage measured series. Accepts JSON `null`,
# the strings `"null"` / `"*"` (case-insensitive), or numeric values per stage.
MeasuredSeries = Annotated[list[float | None] | None, BeforeValidator(_coerce_null_sentinels)]


class _BaseSimulationRequestModel(BaseModel):
    """Shared plumbing for the three simulation request models.

    Subclasses declare their own `measured` and `weights` nested-model fields
    (with experiment-specific properties), set `_FIELD_TO_MAGIC` to the
    field-name -> `PVTHeaders.magic_name` mapping, and override
    `_pvt_temperatures` to return the temperatures list aligned with
    `pressures` (Flash uses a per-stage list; CME/CVD broadcast a single
    isothermal value).
    """

    # Subclasses populate this. Empty default keeps the base model usable for
    # tests that exercise the helpers directly.
    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {}

    @model_validator(mode="after")
    def _validate_measured_lengths(self):
        """Each provided measured series must match the pressure stage count."""
        measured = getattr(self, "measured", None)
        if measured is None:
            return self
        stage_count = len(self.pressures)
        for field_name in self._FIELD_TO_MAGIC:
            values = getattr(measured, field_name, None)
            if values is not None and len(values) != stage_count:
                raise ValueError(
                    f"Measured `{field_name}` has {len(values)} values but there are "
                    f"{stage_count} pressure stages; lengths must match."
                )
        return self

    def _build_measured_dict(self) -> dict[str, list[float]] | None:
        """Convert `measured` payload to the dict keyed by fluidmagic magic_name.

        Missing per-stage values (`None`) are encoded as NaN, which `PVTData`
        accepts and `BasePVTExperiment.calculate_sum_of_squares` skips via
        `np.isnan(...)`.
        """
        measured = getattr(self, "measured", None)
        if measured is None:
            return None
        result: dict[str, list[float]] = {}
        for field_name, magic_name in self._FIELD_TO_MAGIC.items():
            values = getattr(measured, field_name)
            if values is None:
                continue
            result[magic_name] = [v if v is not None else float("nan") for v in values]
        return result or None

    def _build_weights_dict(self) -> dict[str, float] | None:
        """Convert `weights` payload to the dict keyed by fluidmagic magic_name."""
        weights = getattr(self, "weights", None)
        if weights is None:
            return None
        result: dict[str, float] = {}
        for field_name, magic_name in self._FIELD_TO_MAGIC.items():
            value = getattr(weights, field_name)
            if value is not None:
                result[magic_name] = value
        return result or None

    def _pvt_temperatures(self) -> list[float]:
        """Subclasses return the temperatures list aligned with `pressures`."""
        raise NotImplementedError

    def to_pvt_data(self, eos_data):
        return PVTData(
            eos_model=eos_data,
            molarcomp=self.molar_composition,
            temperatures=self._pvt_temperatures(),
            pressures=self.pressures,
            measured=self._build_measured_dict(),
            weights=self._build_weights_dict(),
        )


class FlashMeasuredModel(BaseModel):
    """Optional measured Flash values used for regression / sum-of-squares.

    Each list, when provided, must have the same length as the request's
    `pressures` / `temperatures`. For stages where the value was not
    measured, send JSON `null` or the string `"null"` / `"*"`; these are
    converted to NaN before regression.
    """

    # Reject unknown keys so a typo (e.g. `gar`) returns a 422 instead of
    # being silently dropped.
    model_config = ConfigDict(extra="forbid")

    gas_oil_ratio: MeasuredSeries = Field(None, description="Gas-oil ratio per stage in m³/sm³ (magic column `gor`).")
    oil_density: MeasuredSeries = Field(None, description="Oil density per stage in kg/m³ (magic column `deno`).")
    gas_density: MeasuredSeries = Field(None, description="Gas density per stage in kg/m³ (magic column `deng`).")


class FlashWeightsModel(BaseModel):
    """Optional regression weights per Flash measured property.
    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares. Higher weights give the corresponding measured
    property more influence during regression.
    """

    model_config = ConfigDict(extra="forbid")

    gas_oil_ratio: float | None = Field(None, ge=0, description="Weight for `gas_oil_ratio`.")
    oil_density: float | None = Field(None, ge=0, description="Weight for `oil_density`.")
    gas_density: float | None = Field(None, ge=0, description="Weight for `gas_density`.")


class FlashSimulationRequestModel(_BaseSimulationRequestModel):
    """Model for requesting a flash simulation calculation."""

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(..., description="List of pressures in bara to perform simulation calculations at.")
    temperatures: list[float] = Field(
        ..., description="List of temperatures in °C to perform simulation calculations at."
    )
    measured: FlashMeasuredModel | None = Field(
        None,
        description=(
            "Optional measured Flash values used for sum-of-squares evaluation. "
            "Each provided list must match the length of `pressures`; use null "
            "for stages where no measurement is available."
        ),
    )
    weights: FlashWeightsModel | None = Field(
        None,
        description="Optional regression weights per measured Flash property.",
    )

    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {
        "gas_oil_ratio": PVTHeaders.GAS_OIL_RATIO.magic_name,
        "oil_density": PVTHeaders.OIL_DENSITY.magic_name,
        "gas_density": PVTHeaders.GAS_DENSITY.magic_name,
    }

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [100.0, 50.0],
                "temperatures": [100.0, 30.0],
                "measured": {
                    "gas_oil_ratio": [84.62648865, 707.617734],
                    "oil_density": [707.6, 766.5],
                    "gas_density": [84.6, 44.0],
                },
                "weights": {
                    "gas_oil_ratio": 1.0,
                    "oil_density": 1.0,
                    "gas_density": 1.0,
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_simulation_condition_consistency(self):
        """Validate that the simulation conditions have consistent lengths."""
        if len(self.pressures) != len(self.temperatures):
            raise ValueError("Pressures and temperatures must have the same length")
        return self

    def _pvt_temperatures(self) -> list[float]:
        return self.temperatures


class FlashSimulationResponseModel(BaseModel):
    """Response wrapper for the flash simulation endpoint.

    `sum_of_squares` is the weighted regression objective computed by
    `FlashExperiment.calculate_sum_of_squares` using the request's `measured`
    and `weights`. It is `0.0` when no weights (or only zero weights) were
    supplied, so callers tuning the EOS can vary `weights` and observe the
    SSQ react.
    """

    flash_calculated: FlashCalculated = Field(..., description="Flash phase / property results per stage.")
    sum_of_squares: float = Field(
        ...,
        ge=0.0,
        description=(
            "Weighted sum-of-squares between the supplied `measured` values and the "
            "calculated values. Returns 0.0 when no `weights` were provided."
        ),
    )


class FlashInlineRequestModel(BaseModel):
    """Request body for the inline flash endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the flash calculation. Not persisted.")
    parameters: FlashSimulationRequestModel = Field(..., description="Flash calculation parameters.")


class CMEMeasuredModel(BaseModel):
    """Optional measured CME values used for regression / sum-of-squares.

    Each list, when provided, must have the same length as the request's
    `pressures`. For stages where the value was not measured, send JSON
    `null` or the string `"null"` / `"*"`; these are converted to NaN
    before regression.
    """

    # Reject unknown keys so a typo (e.g. `y_factior`) returns a 422 instead of
    # being silently dropped and producing a regression that ignores the column.
    model_config = ConfigDict(extra="forbid")

    relative_total_volume: MeasuredSeries = Field(
        None, description="Relative total volume per stage (magic column `vrt`)."
    )
    compressibility: MeasuredSeries = Field(
        None, description="Compressibility per stage in 1/bar (magic column `compr`)."
    )
    y_factor: MeasuredSeries = Field(None, description="Y-factor per stage (magic column `y-fac`).")
    density: MeasuredSeries = Field(None, description="Single-phase density per stage in kg/m³ (magic column `den`).")
    liquid_volume: MeasuredSeries = Field(
        None, description="Relative liquid volume per stage in % (magic column `liq-vol`)."
    )
    z_factor: MeasuredSeries = Field(None, description="Gas Z-factor per stage (magic column `z-fac`).")


class CMEWeightsModel(BaseModel):
    """Optional regression weights per CME measured property.

    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares. Higher weights give the corresponding measured
    property more influence during regression.
    """

    # Reject unknown keys (e.g. `densty`) so they fail validation rather than
    # being silently dropped.
    model_config = ConfigDict(extra="forbid")

    # Negative weights would be silently ignored by the SSQ loop, which is
    # misleading; reject them up front.
    relative_total_volume: float | None = Field(None, ge=0, description="Weight for `relative_total_volume`.")
    compressibility: float | None = Field(None, ge=0, description="Weight for `compressibility`.")
    y_factor: float | None = Field(None, ge=0, description="Weight for `y_factor`.")
    density: float | None = Field(None, ge=0, description="Weight for `density`.")
    liquid_volume: float | None = Field(None, ge=0, description="Weight for `liquid_volume`.")
    z_factor: float | None = Field(None, ge=0, description="Weight for `z_factor`.")


class CMESimulationRequestModel(_BaseSimulationRequestModel):
    """Model for requesting a Constant Mass Expansion (CME) simulation.

    A CME experiment is run along a single isotherm: one temperature is held
    constant while the pressure is reduced through a series of stages. The
    pressure stages must therefore be monotonically decreasing.
    """

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(
        ...,
        description=(
            "Pressure stages in bara, in monotonically decreasing order, " "to perform the CME simulation at."
        ),
    )
    temperature: float = Field(..., description="Isothermal temperature in °C to perform the CME simulation at.")
    measured: CMEMeasuredModel | None = Field(
        None,
        description=(
            "Optional measured CME values used for sum-of-squares evaluation. "
            "Each provided list must match the length of `pressures`; use null "
            "for stages where no measurement is available."
        ),
    )
    weights: CMEWeightsModel | None = Field(
        None,
        description="Optional regression weights per measured CME property.",
    )

    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {
        "relative_total_volume": PVTHeaders.RELATIVE_TOTAL_VOLUME.magic_name,
        "compressibility": PVTHeaders.COMPRESSIBILITY.magic_name,
        "y_factor": PVTHeaders.Y_FACTOR.magic_name,
        "density": PVTHeaders.DENSITY.magic_name,
        "liquid_volume": PVTHeaders.LIQUID_VOLUME.magic_name,
        "z_factor": PVTHeaders.Z_FACTOR.magic_name,
    }

    model_config = ConfigDict(
        # Reject unknown top-level keys on the CME request so typos fail loudly
        # and the user gets immediate feedback, rather than being silently ignored.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [300.0, 250.0, 225.0, 204.99, 200.0, 175.0, 150.0, 100.0, 50.0, 20.0],
                "temperature": 100.0,
                "measured": {
                    "relative_total_volume": [
                        0.9786,
                        0.9891,
                        0.9949,
                        1.0000,
                        1.0081,
                        1.0595,
                        1.1368,
                        1.4563,
                        2.6104,
                        6.6119,
                    ],
                    "compressibility": [1.99e-4, 2.28e-4, 2.45e-4, 2.61e-4, None, None, None, None, None, None],
                    "y_factor": [None, None, None, None, 3.10, 2.88, 2.68, 2.30, 1.92, 1.65],
                    "density": [666.878513, 659.8171507, 655.9286849, 652.6158943, None, None, None, None, None, None],
                    "liquid_volume": [None, None, None, 100.00, 99.12, 95.11, 91.53, 84.97, 78.00, 71.68],
                    "z_factor": [None, None, None, None, None, None, None, None, None, None],
                },
                "weights": {
                    "relative_total_volume": 1.0,
                    "compressibility": 1.0,
                    "y_factor": 1.0,
                    "density": 1.0,
                    "liquid_volume": 1.0,
                    "z_factor": 0.0,
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_pressure_stages(self):
        """Validate that pressures are non-empty and monotonically decreasing."""
        if not self.pressures:
            raise ValueError("At least one pressure stage is required.")
        if any(p2 >= p1 for p1, p2 in zip(self.pressures, self.pressures[1:])):
            raise ValueError("Pressure stages must be monotonically decreasing for a CME simulation.")
        return self

    def _pvt_temperatures(self) -> list[float]:
        # CMEExperiment is isothermal but PVTData requires temperatures and
        # pressures to be the same length; broadcast the single value.
        return [self.temperature] * len(self.pressures)


class CVDMeasuredModel(BaseModel):
    """Optional measured CVD values used for regression / sum-of-squares.

    Each list, when provided, must have the same length as the request's
    `pressures`. For stages where the value was not measured, send JSON
    `null` or the string `"null"` / `"*"`; these are converted to NaN
    before regression.
    """

    # Reject unknown keys so a typo returns a 422 instead of being silently
    # dropped and producing a regression that ignores the column.
    model_config = ConfigDict(extra="forbid")

    liquid_volume: MeasuredSeries = Field(
        None, description="Relative liquid volume per stage in % (magic column `liq-vol`)."
    )
    moles_gas_produced: MeasuredSeries = Field(
        None, description="Cumulative moles of gas produced per stage in % (magic column `np`)."
    )
    z_factor: MeasuredSeries = Field(None, description="Gas Z-factor per stage (magic column `z-fac`).")
    two_phase_z_factor: MeasuredSeries = Field(
        None, description="Two-phase Z-factor per stage (magic column `z-fac2`)."
    )
    oil_formation_volume_factor: MeasuredSeries = Field(
        None, description="Oil formation volume factor per stage (magic column `bo`)."
    )
    solution_gas_oil_ratio: MeasuredSeries = Field(
        None, description="Solution gas-to-oil ratio per stage (magic column `rs`)."
    )
    gas_formation_volume_factor: MeasuredSeries = Field(
        None, description="Gas formation volume factor per stage (magic column `bg`)."
    )
    oil_density: MeasuredSeries = Field(None, description="Oil density per stage in kg/m³ (magic column `deno`).")
    gas_specific_gravity: MeasuredSeries = Field(
        None, description="Gas specific gravity per stage (magic column `sg`)."
    )


class CVDWeightsModel(BaseModel):
    """Optional regression weights per CVD measured property.

    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares. Higher weights give the corresponding measured
    property more influence during regression.
    """

    # Reject unknown keys so they fail validation rather than being silently dropped.
    model_config = ConfigDict(extra="forbid")

    # Negative weights would be silently ignored by the SSQ loop, which is
    # misleading; reject them up front.
    liquid_volume: float | None = Field(None, ge=0, description="Weight for `liquid_volume`.")
    moles_gas_produced: float | None = Field(None, ge=0, description="Weight for `moles_gas_produced`.")
    z_factor: float | None = Field(None, ge=0, description="Weight for `z_factor`.")
    two_phase_z_factor: float | None = Field(None, ge=0, description="Weight for `two_phase_z_factor`.")
    oil_formation_volume_factor: float | None = Field(
        None, ge=0, description="Weight for `oil_formation_volume_factor`."
    )
    solution_gas_oil_ratio: float | None = Field(None, ge=0, description="Weight for `solution_gas_oil_ratio`.")
    gas_formation_volume_factor: float | None = Field(
        None, ge=0, description="Weight for `gas_formation_volume_factor`."
    )
    oil_density: float | None = Field(None, ge=0, description="Weight for `oil_density`.")
    gas_specific_gravity: float | None = Field(None, ge=0, description="Weight for `gas_specific_gravity`.")


class CMEInlineRequestModel(BaseModel):
    """Request body for the inline CME endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the CME calculation. Not persisted.")
    parameters: CMESimulationRequestModel = Field(..., description="CME calculation parameters.")


class CVDSimulationRequestModel(_BaseSimulationRequestModel):
    """Model for requesting a Constant Volume Depletion (CVD) simulation.

    A CVD experiment is run along a single isotherm: one temperature is held
    constant while the pressure is reduced through a series of stages and gas
    is removed at each stage to keep the cell volume constant. The pressure
    stages must therefore be monotonically decreasing.

    The optional `measured` and `weights` fields mirror the table columns of
    the `simulate_cvd.magic` demo and are forwarded to the underlying
    `CVDExperiment` for regression / sum-of-squares evaluation.
    """

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(
        ...,
        description=(
            "Pressure stages in bara, in monotonically decreasing order, " "to perform the CVD simulation at."
        ),
    )
    temperature: float = Field(..., description="Isothermal temperature in °C to perform the CVD simulation at.")
    measured: CVDMeasuredModel | None = Field(
        None,
        description=(
            "Optional measured CVD values used for sum-of-squares evaluation. "
            "Each provided list must match the length of `pressures`; use null "
            "for stages where no measurement is available."
        ),
    )
    weights: CVDWeightsModel | None = Field(
        None,
        description="Optional regression weights per measured CVD property.",
    )

    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {
        "liquid_volume": PVTHeaders.LIQUID_VOLUME.magic_name,
        "moles_gas_produced": PVTHeaders.MOLES_GAS_PRODUCED.magic_name,
        "z_factor": PVTHeaders.Z_FACTOR.magic_name,
        "two_phase_z_factor": PVTHeaders.TWO_PHASE_Z_FACTOR.magic_name,
        "oil_formation_volume_factor": PVTHeaders.OIL_FORMATION_VOLUME_FACTOR.magic_name,
        "solution_gas_oil_ratio": PVTHeaders.SOLUTION_GAS_OIL_RATIO.magic_name,
        "gas_formation_volume_factor": PVTHeaders.GAS_FORMATION_VOLUME_FACTOR.magic_name,
        "oil_density": PVTHeaders.OIL_DENSITY.magic_name,
        "gas_specific_gravity": PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name,
    }

    model_config = ConfigDict(
        # Reject unknown top-level keys so typos fail loudly.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [300.0, 250.0, 225.0, 204.99, 200.0, 175.0, 150.0, 100.0, 50.0, 20.0],
                "temperature": 100.0,
                "measured": {
                    "liquid_volume": [None, None, None, 0.00, 0.00, 0.67, 1.66, 2.50, 2.11, 1.53],
                    "moles_gas_produced": [None, None, None, 0.00, 2.00, 13.02, 25.26, 51.02, 76.29, 90.46],
                    "z_factor": [0.9371, 0.8789, 0.8539, 0.8370, 0.8333, 0.8230, 0.8254, 0.8556, 0.9124, 0.9580],
                    "two_phase_z_factor": [None, None, None, 0.8370, 0.8333, 0.8215, 0.8194, 0.8335, 0.8611, 0.8564],
                    "gas_specific_gravity": [None, None, None, 0.848, 0.847, 0.838, 0.821, 0.795, 0.793, 0.827],
                    "oil_formation_volume_factor": [None] * 10,
                    "solution_gas_oil_ratio": [None] * 10,
                    "oil_density": [None] * 10,
                    "gas_formation_volume_factor": [None] * 10,
                },
                "weights": {
                    "liquid_volume": 1.0,
                    "moles_gas_produced": 1.0,
                    "z_factor": 1.0,
                    "two_phase_z_factor": 1.0,
                    "gas_specific_gravity": 1.0,
                    "oil_formation_volume_factor": 0.0,
                    "solution_gas_oil_ratio": 0.0,
                    "oil_density": 0.0,
                    "gas_formation_volume_factor": 0.0,
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_pressure_stages(self):
        """Validate that pressures are non-empty and monotonically decreasing."""
        if not self.pressures:
            raise ValueError("At least one pressure stage is required.")
        if any(p2 >= p1 for p1, p2 in zip(self.pressures, self.pressures[1:])):
            raise ValueError("Pressure stages must be monotonically decreasing for a CVD simulation.")
        return self

    def _pvt_temperatures(self) -> list[float]:
        # CVDExperiment is isothermal but PVTData requires temperatures and
        # pressures to be the same length; broadcast the single value.
        return [self.temperature] * len(self.pressures)


class CVDInlineRequestModel(BaseModel):
    """Request body for the inline CVD endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the CVD calculation. Not persisted.")
    parameters: CVDSimulationRequestModel = Field(..., description="CVD calculation parameters.")


class DLEMeasuredModel(BaseModel):
    """Optional measured DLE values used for regression / sum-of-squares.

    Each list, when provided, must have the same length as the request's
    `pressures`. For stages where the value was not measured, send JSON
    `null` or the string `"null"` / `"*"`; these are converted to NaN
    before regression.
    """

    # Reject unknown keys so a typo returns a 422 instead of being silently
    # dropped and producing a regression that ignores the column.
    model_config = ConfigDict(extra="forbid")

    oil_formation_volume_factor_dle: MeasuredSeries = Field(
        None, description="DLE oil formation volume factor per stage (magic column `bod`)."
    )
    solution_gas_oil_ratio_dle: MeasuredSeries = Field(
        None, description="DLE solution gas-to-oil ratio per stage (magic column `rsd`)."
    )
    gas_formation_volume_factor: MeasuredSeries = Field(
        None, description="Gas formation volume factor per stage (magic column `bg`)."
    )
    oil_density: MeasuredSeries = Field(None, description="Oil density per stage in kg/m³ (magic column `deno`).")
    z_factor: MeasuredSeries = Field(None, description="Gas Z-factor per stage (magic column `z-fac`).")
    gas_specific_gravity: MeasuredSeries = Field(
        None, description="Gas specific gravity per stage (magic column `sg`)."
    )
    oil_viscosity: MeasuredSeries = Field(None, description="Oil viscosity per stage in cP (magic column `viso`).")


class DLEWeightsModel(BaseModel):
    """Optional regression weights per DLE measured property.

    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares. Higher weights give the corresponding measured
    property more influence during regression.
    """

    model_config = ConfigDict(extra="forbid")

    # Negative weights would be silently ignored by the SSQ loop, which is
    # misleading; reject them up front.
    oil_formation_volume_factor_dle: float | None = Field(
        None, ge=0, description="Weight for `oil_formation_volume_factor_dle`."
    )
    solution_gas_oil_ratio_dle: float | None = Field(None, ge=0, description="Weight for `solution_gas_oil_ratio_dle`.")
    gas_formation_volume_factor: float | None = Field(
        None, ge=0, description="Weight for `gas_formation_volume_factor`."
    )
    oil_density: float | None = Field(None, ge=0, description="Weight for `oil_density`.")
    z_factor: float | None = Field(None, ge=0, description="Weight for `z_factor`.")
    gas_specific_gravity: float | None = Field(None, ge=0, description="Weight for `gas_specific_gravity`.")
    oil_viscosity: float | None = Field(None, ge=0, description="Weight for `oil_viscosity`.")


class DLESimulationRequestModel(_BaseSimulationRequestModel):
    """Model for requesting a Differential Liberation (DLE) simulation.

    A DLE experiment is run along a single isotherm: one temperature is held
    constant while the pressure is reduced through a series of stages, with
    liberated gas removed at each stage. The pressure stages must therefore
    be monotonically decreasing.
    """

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(
        ...,
        description=(
            "Pressure stages in bara, in monotonically decreasing order, " "to perform the DLE simulation at."
        ),
    )
    temperature: float = Field(..., description="Isothermal temperature in °C to perform the DLE simulation at.")
    measured: DLEMeasuredModel | None = Field(
        None,
        description=(
            "Optional measured DLE values used for sum-of-squares evaluation. "
            "Each provided list must match the length of `pressures`; use null "
            "for stages where no measurement is available."
        ),
    )
    weights: DLEWeightsModel | None = Field(
        None,
        description="Optional regression weights per measured DLE property.",
    )

    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {
        "oil_formation_volume_factor_dle": PVTHeaders.OIL_FORMATION_VOLUME_FACTOR_DLE.magic_name,
        "solution_gas_oil_ratio_dle": PVTHeaders.SOLUTION_GAS_OIL_RATIO_DLE.magic_name,
        "gas_formation_volume_factor": PVTHeaders.GAS_FORMATION_VOLUME_FACTOR.magic_name,
        "oil_density": PVTHeaders.OIL_DENSITY.magic_name,
        "z_factor": PVTHeaders.Z_FACTOR.magic_name,
        "gas_specific_gravity": PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name,
        "oil_viscosity": PVTHeaders.OIL_VISCOSITY.magic_name,
    }

    model_config = ConfigDict(
        # Reject unknown top-level keys so typos fail loudly.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [300.0, 250.0, 225.0, 204.99, 200.0, 175.0, 150.0, 100.0, 50.0, 20.0, 1.01],
                "temperature": 100.0,
                "measured": {
                    "oil_formation_volume_factor_dle": [
                        1.494,
                        1.510,
                        1.519,
                        1.527,
                        1.513,
                        1.451,
                        1.395,
                        1.295,
                        1.200,
                        1.134,
                        1.000,
                    ],
                    "solution_gas_oil_ratio_dle": [
                        150.0,
                        150.0,
                        150.0,
                        150.0,
                        145.3,
                        123.6,
                        103.7,
                        68.2,
                        35.6,
                        15.0,
                        None,
                    ],
                    "gas_formation_volume_factor": [
                        None,
                        None,
                        None,
                        None,
                        0.005515,
                        0.006291,
                        0.007368,
                        0.011330,
                        0.023727,
                        0.061641,
                        None,
                    ],
                    "oil_density": [
                        666.878513,
                        659.8171507,
                        655.9286849,
                        652.6158943,
                        655.2056096,
                        668.0947362,
                        681.0347663,
                        707.4676529,
                        735.7393508,
                        755.9155586,
                        833.9188032,
                    ],
                    "z_factor": [None, None, None, None, 0.8361, 0.8348, 0.8383, 0.8595, 0.8994, 0.9323, None],
                    "gas_specific_gravity": [None, None, None, None, 0.841, 0.813, 0.795, 0.782, 0.829, 1.001, None],
                    "oil_viscosity": [
                        0.7510,
                        0.6762,
                        0.6387,
                        0.6088,
                        0.6289,
                        0.7410,
                        0.8761,
                        1.2422,
                        1.8201,
                        2.4040,
                        None,
                    ],
                },
                "weights": {
                    "oil_formation_volume_factor_dle": 1.0,
                    "solution_gas_oil_ratio_dle": 1.0,
                    "gas_formation_volume_factor": 1.0,
                    "oil_density": 1.0,
                    "z_factor": 1.0,
                    "gas_specific_gravity": 1.0,
                    "oil_viscosity": 0.0,
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_pressure_stages(self):
        """Validate that pressures are non-empty and monotonically decreasing."""
        if not self.pressures:
            raise ValueError("At least one pressure stage is required.")
        if any(p2 >= p1 for p1, p2 in zip(self.pressures, self.pressures[1:])):
            raise ValueError("Pressure stages must be monotonically decreasing for a DLE simulation.")
        return self

    def _pvt_temperatures(self) -> list[float]:
        # DLEExperiment is isothermal but PVTData requires temperatures and
        # pressures to be the same length; broadcast the single value.
        return [self.temperature] * len(self.pressures)


class DLEInlineRequestModel(BaseModel):
    """Request body for the inline DLE endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the DLE calculation. Not persisted.")
    parameters: DLESimulationRequestModel = Field(..., description="DLE calculation parameters.")


class SEPMeasuredModel(BaseModel):
    """Optional measured separator values used for regression / sum-of-squares.

    Each list, when provided, must have the same length as the request's
    `pressures` / `temperatures`. For stages where the value was not
    measured, send JSON `null` or the string `"null"` / `"*"`; these are
    converted to NaN before regression.
    """

    # Reject unknown keys so a typo returns a 422 instead of being silently
    # dropped and producing a regression that ignores the column.
    model_config = ConfigDict(extra="forbid")

    gas_oil_ratio: MeasuredSeries = Field(None, description="Gas-oil ratio per stage in sm³/sm³ (magic column `gor`).")
    total_gas_oil_ratio: MeasuredSeries = Field(
        None, description="Total gas-oil ratio per stage in sm³/sm³ (magic column `tot-gor`)."
    )
    gas_specific_gravity: MeasuredSeries = Field(
        None, description="Gas specific gravity per stage (magic column `sg`)."
    )
    oil_density: MeasuredSeries = Field(None, description="Oil density per stage in kg/m³ (magic column `deno`).")
    oil_formation_volume_factor: MeasuredSeries = Field(
        None, description="Oil formation volume factor per stage (magic column `bo`)."
    )


class SEPWeightsModel(BaseModel):
    """Optional regression weights per separator measured property.

    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares. Higher weights give the corresponding measured
    property more influence during regression.
    """

    model_config = ConfigDict(extra="forbid")

    # Negative weights would be silently ignored by the SSQ loop, which is
    # misleading; reject them up front.
    gas_oil_ratio: float | None = Field(None, ge=0, description="Weight for `gas_oil_ratio`.")
    total_gas_oil_ratio: float | None = Field(None, ge=0, description="Weight for `total_gas_oil_ratio`.")
    gas_specific_gravity: float | None = Field(None, ge=0, description="Weight for `gas_specific_gravity`.")
    oil_density: float | None = Field(None, ge=0, description="Weight for `oil_density`.")
    oil_formation_volume_factor: float | None = Field(
        None, ge=0, description="Weight for `oil_formation_volume_factor`."
    )


class SEPSimulationRequestModel(_BaseSimulationRequestModel):
    """Model for requesting a multi-stage separator (SEP) simulation.

    A separator experiment processes a feed through a sequence of stages with
    their own pressure and temperature. Both lists must have the same length
    and pressures must be monotonically decreasing.
    """

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    pressures: list[float] = Field(
        ...,
        description=(
            "Pressure stages in bara, in monotonically decreasing order, " "to perform the separator simulation at."
        ),
    )
    temperatures: list[float] = Field(
        ..., description="Temperature per stage in °C; must have the same length as `pressures`."
    )
    measured: SEPMeasuredModel | None = Field(
        None,
        description=(
            "Optional measured separator values used for sum-of-squares evaluation. "
            "Each provided list must match the length of `pressures`; use null "
            "for stages where no measurement is available."
        ),
    )
    weights: SEPWeightsModel | None = Field(
        None,
        description="Optional regression weights per measured separator property.",
    )

    _FIELD_TO_MAGIC: ClassVar[dict[str, str]] = {
        "gas_oil_ratio": PVTHeaders.GAS_OIL_RATIO.magic_name,
        "total_gas_oil_ratio": PVTHeaders.TOTAL_GAS_OIL_RATIO.magic_name,
        "gas_specific_gravity": PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name,
        "oil_density": PVTHeaders.OIL_DENSITY.magic_name,
        "oil_formation_volume_factor": PVTHeaders.OIL_FORMATION_VOLUME_FACTOR.magic_name,
    }

    model_config = ConfigDict(
        # Reject unknown top-level keys so typos fail loudly.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "pressures": [205.0, 50.0, 30.0, 1.01],
                "temperatures": [100.0, 50.0, 39.0, 15.0],
                "measured": {
                    "gas_oil_ratio": [None, 4131.7, 29.6, 96.6],
                    "total_gas_oil_ratio": [4257.9, 4257.9, 4257.9, 4257.9],
                    "gas_specific_gravity": [None, 0.728, 0.739, 1.329],
                    "oil_density": [None, 618.6495118, 648.4460708, 729.4458044],
                    "oil_formation_volume_factor": [23.818, 1.480, 1.371, 1.000],
                },
                "weights": {
                    "gas_oil_ratio": 1.0,
                    "total_gas_oil_ratio": 1.0,
                    "gas_specific_gravity": 1.0,
                    "oil_density": 1.0,
                    "oil_formation_volume_factor": 1.0,
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_simulation_condition_consistency(self):
        """Validate that pressures/temperatures match and pressures are monotonically decreasing."""
        if not self.pressures:
            raise ValueError("At least one pressure stage is required.")
        if len(self.pressures) != len(self.temperatures):
            raise ValueError("Pressures and temperatures must have the same length")
        if any(p2 >= p1 for p1, p2 in zip(self.pressures, self.pressures[1:])):
            raise ValueError("Pressure stages must be monotonically decreasing for a separator simulation.")
        return self

    def _pvt_temperatures(self) -> list[float]:
        return self.temperatures


class SEPInlineRequestModel(BaseModel):
    """Request body for the inline SEP endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the separator calculation. Not persisted.")
    parameters: SEPSimulationRequestModel = Field(..., description="Separator calculation parameters.")


# Placeholder pressure used when building `PVTData` for a saturation-pressure
# experiment. `SaturationPressureExperiment.simulate()` ignores `pressures` and
# only reads `temperatures[0]`, but `PVTData` requires both lists to have the
# same length, so we supply a single dummy stage.
_PSAT_PLACEHOLDER_PRESSURE: float = 1.0


class PsatMeasuredModel(BaseModel):
    """Optional measured saturation pressure used for sum-of-squares evaluation.

    Send JSON `null` or the strings `"null"` / `"*"` for "not measured".
    """

    model_config = ConfigDict(extra="forbid")

    saturation_pressure: Annotated[
        float | None,
        BeforeValidator(lambda v: None if isinstance(v, str) and v.strip().lower() in _NULL_SENTINELS else v),
    ] = Field(
        None,
        description="Measured saturation pressure in bara (magic column `psat`).",
    )


class PsatWeightsModel(BaseModel):
    """Optional regression weight for the measured saturation pressure.

    A weight of 0 (or absent) means the measurement is ignored when computing
    the sum-of-squares.
    """

    model_config = ConfigDict(extra="forbid")

    saturation_pressure: float | None = Field(
        None,
        ge=0,
        description="Weight for `saturation_pressure`.",
    )


class PsatSimulationRequestModel(BaseModel):
    """Model for requesting a saturation-pressure (PSAT) simulation.

    A PSAT calculation determines the saturation pressure of a fluid at a single
    isothermal temperature given its molar composition. It also returns the
    incipient equilibrium oil and gas compositions and the fluid type
    (bubble-point vs. dew-point).
    """

    molar_composition: list[float] = Field(..., description="Molar composition for each component.")
    temperature: float = Field(..., description="Isothermal temperature in °C to compute the saturation pressure at.")
    measured: PsatMeasuredModel | None = Field(
        None,
        description="Optional measured saturation pressure used for sum-of-squares evaluation.",
    )
    weights: PsatWeightsModel | None = Field(
        None,
        description="Optional regression weight for the measured saturation pressure.",
    )

    model_config = ConfigDict(
        # Reject unknown top-level keys so typos fail loudly.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_composition": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "temperature": 100.0,
                "measured": {"saturation_pressure": 113.4},
                "weights": {"saturation_pressure": 1.0},
            }
        },
    )

    def _build_measured_dict(self) -> dict[str, list[float]] | None:
        if self.measured is None or self.measured.saturation_pressure is None:
            return None
        return {PVTHeaders.SATURATION_PRESSURE.magic_name: [self.measured.saturation_pressure]}

    def _build_weights_dict(self) -> dict[str, float] | None:
        if self.weights is None or self.weights.saturation_pressure is None:
            return None
        return {PVTHeaders.SATURATION_PRESSURE.magic_name: self.weights.saturation_pressure}

    def to_pvt_data(self, eos_data):
        return PVTData(
            eos_model=eos_data,
            molarcomp=self.molar_composition,
            temperatures=[self.temperature],
            pressures=[_PSAT_PLACEHOLDER_PRESSURE],
            measured=self._build_measured_dict(),
            weights=self._build_weights_dict(),
        )


class PsatSimulationResponseModel(BaseModel):
    """Response wrapper for the saturation-pressure simulation endpoint.

    `sum_of_squares` is the weighted regression objective computed by
    `SaturationPressureExperiment.calculate_sum_of_squares` using the request's
    `measured` and `weights`. It is `0.0` when no weight was provided.
    """

    saturation_pressure_calculated: SaturationPressureCalculated = Field(
        ..., description="Saturation pressure result and equilibrium compositions."
    )
    sum_of_squares: float = Field(
        ...,
        ge=0.0,
        description=(
            "Weighted sum-of-squares between the supplied measured saturation pressure "
            "and the calculated value. Returns 0.0 when no weight was provided."
        ),
    )


class PsatInlineRequestModel(BaseModel):
    """Request body for the inline PSAT endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the PSAT calculation. Not persisted.")
    parameters: PsatSimulationRequestModel = Field(..., description="PSAT calculation parameters.")


class ProcessSimulationRequestModel(BaseModel):
    """Model for requesting a surface-process simulation.

    A process simulation feeds a molar stream into a sequence of tanks
    (flash, volume splitter, recovery-factor, k-value, oil/gas/NGL collector)
    and returns the per-tank oil/gas volumes, moles and compositions.
    """

    molar_stream: list[float] = Field(
        ...,
        description=("Inlet stream in kg-moles per component (length must match the EOS model's " "component count)."),
    )
    process: ProcessData = Field(
        ..., description="Definition of the surface-separation process (name + ordered list of tanks)."
    )

    model_config = ConfigDict(
        # Reject unknown top-level keys so typos fail loudly.
        extra="forbid",
        json_schema_extra={
            "example": {
                "molar_stream": [0.05, 0.5, 0.2, 0.15, 0.06, 0.04],
                "process": {
                    "name": "my_process",
                    "tanks": [
                        {
                            "name": "SEP1",
                            "tank_type": "flash",
                            "pressure": 21.0,
                            "temperature": 65.0,
                            "oil_destination": "SEP2",
                            "gas_destination": "GASTANK",
                        },
                        {
                            "name": "SEP2",
                            "tank_type": "flash",
                            "pressure": 1.013,
                            "temperature": 15.0,
                            "oil_destination": "OILTANK",
                            "gas_destination": "GASTANK",
                        },
                        {"name": "OILTANK", "tank_type": "oiltank", "pressure": 1.013, "temperature": 15.0},
                        {"name": "GASTANK", "tank_type": "gastank", "pressure": 1.013, "temperature": 15.0},
                    ],
                },
            }
        },
    )


class ProcessSimulationResponseModel(BaseModel):
    """Per-tank results from a surface-process simulation.

    Each list has one entry per tank in the request (in declaration order); the
    composition lists have an inner list of length `component_count`.
    """

    tank_names: list[str] = Field(..., description="Names of the tanks (matches request order).")
    oil_volume: list[float] = Field(..., description="Oil volume per tank in m³.")
    gas_volume: list[float] = Field(..., description="Gas volume per tank in m³.")
    oil_moles: list[float] = Field(..., description="Oil moles per tank.")
    gas_moles: list[float] = Field(..., description="Gas moles per tank.")
    oil_compositions: list[list[float]] = Field(..., description="Oil composition per tank.")
    gas_compositions: list[list[float]] = Field(..., description="Gas composition per tank.")


class ProcessInlineRequestModel(BaseModel):
    """Request body for the inline process endpoint.

    Carries the EOS data directly so no facility / EOS lookup is required.
    """

    model_config = ConfigDict(extra="forbid")

    eos_data: EOSData = Field(..., description="EOS model to use for the process simulation. Not persisted.")
    parameters: ProcessSimulationRequestModel = Field(..., description="Process simulation parameters.")
