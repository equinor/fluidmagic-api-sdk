import math
from abc import ABC, abstractmethod
from typing import Any, Self

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, Field

from fluidmagic_api_sdk.models.constants.headers import Headers, PVTHeaders
from fluidmagic_api_sdk.models.enums import PhaseType


class BaseCalculated(BaseModel, ABC):
    """Base class for calculated PVT results."""

    def sanitize_for_serialization(self) -> Self:
        """Sanitize the calculated PVT results for serialization."""
        for field_name in self.__dict__.keys():
            sanitized_value = self._sanitize_float_values(getattr(self, field_name))
            setattr(self, field_name, sanitized_value)
        return self

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    @classmethod
    def _sanitize_float_values(cls, obj):
        """Replace non-JSON-compliant float values (inf, -inf, NaN) with None."""
        if isinstance(obj, float):
            if math.isinf(obj) or math.isnan(obj):
                return None
            return obj
        elif isinstance(obj, dict):
            return {k: cls._sanitize_float_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [cls._sanitize_float_values(item) for item in obj]
        return obj

    @staticmethod
    def _to_list(obj):
        """Convert numpy array or list to list. Handles both numpy arrays and lists."""
        if isinstance(obj, list):
            return obj
        return obj.tolist()


class FlashCalculated(BaseCalculated):
    """Class for flash calculation results."""

    gas_mole_fraction: list[float | None] = Field(..., description="Gas mole fraction.")
    equilibrium_gas_comp: list[list[float | None]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float | None]] = Field(..., description="Equilibrium oil composition.")
    oil_density: list[float | None] = Field(..., description="Oil density.")
    gas_density: list[float | None] = Field(..., description="Gas density.")
    gas_oil_ratio: list[float | None] = Field(..., description="Gas-to-Oil ratio.")
    oil_volume: list[float | None] = Field(..., description="Oil volume.")
    gas_volume: list[float | None] = Field(..., description="Gas volume.")
    oil_molecular_weight: list[float | None] = Field(..., description="Oil molecular weight.")
    gas_molecular_weight: list[float | None] = Field(..., description="Gas molecular weight.")
    oil_viscosity: list[float | None] = Field(..., description="Oil viscosity.")
    gas_viscosity: list[float | None] = Field(..., description="Gas viscosity.")
    interfacial_tension: list[float | None] = Field(..., description="Interfacial tension.")

    def __init__(
        self,
        gas_mole_fraction: npt.NDArray[np.float64] | list[float | None],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[list[float | None]],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[list[float | None]],
        oil_density: npt.NDArray[np.float64] | list[float | None],
        gas_density: npt.NDArray[np.float64] | list[float | None],
        gas_oil_ratio: npt.NDArray[np.float64] | list[float | None],
        oil_volume: npt.NDArray[np.float64] | list[float | None],
        gas_volume: npt.NDArray[np.float64] | list[float | None],
        oil_molecular_weight: npt.NDArray[np.float64] | list[float | None],
        gas_molecular_weight: npt.NDArray[np.float64] | list[float | None],
        oil_viscosity: npt.NDArray[np.float64] | list[float | None],
        gas_viscosity: npt.NDArray[np.float64] | list[float | None],
        interfacial_tension: npt.NDArray[np.float64] | list[float | None],
        **kwargs,
    ):
        super().__init__(
            gas_mole_fraction=self._to_list(gas_mole_fraction),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            oil_density=self._to_list(oil_density),
            gas_density=self._to_list(gas_density),
            gas_oil_ratio=self._to_list(gas_oil_ratio),
            oil_volume=self._to_list(oil_volume),
            gas_volume=self._to_list(gas_volume),
            oil_molecular_weight=self._to_list(oil_molecular_weight),
            gas_molecular_weight=self._to_list(gas_molecular_weight),
            oil_viscosity=self._to_list(oil_viscosity),
            gas_viscosity=self._to_list(gas_viscosity),
            interfacial_tension=self._to_list(interfacial_tension),
            **kwargs,
        )

    def to_dict(self) -> dict[str, npt.NDArray[np.float64]]:
        return {
            PVTHeaders.GAS_MOLE_FRACTION.magic_name: np.array(self.gas_mole_fraction),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
            PVTHeaders.OIL_DENSITY.magic_name: np.array(self.oil_density),
            PVTHeaders.GAS_DENSITY.magic_name: np.array(self.gas_density),
            PVTHeaders.GAS_OIL_RATIO.magic_name: np.array(self.gas_oil_ratio),
            Headers.OIL_VOLUME.name: np.array(self.oil_volume),
            Headers.GAS_VOLUME.name: np.array(self.gas_volume),
            Headers.OIL_MOLECULAR_WEIGHT.name: np.array(self.oil_molecular_weight),
            Headers.GAS_MOLECULAR_WEIGHT.name: np.array(self.gas_molecular_weight),
            PVTHeaders.OIL_VISCOSITY.magic_name: np.array(self.oil_viscosity),
            PVTHeaders.GAS_VISCOSITY.magic_name: np.array(self.gas_viscosity),
            "interfacial_tension": np.array(self.interfacial_tension),
        }


class SaturationPressureCalculated(BaseCalculated):
    """Class for saturation pressure calculation results."""

    saturation_pressure: list[float] = Field(..., description="Saturation pressure.")
    equilibrium_oil_comp: list[float] = Field(..., description="Equilibrium oil composition.")
    equilibrium_gas_comp: list[float] = Field(..., description="Equilibrium gas composition.")
    fluid_type: PhaseType | None = Field(None, description="Fluid type.")

    def __init__(
        self,
        saturation_pressure: list[float],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[float],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[float],
        fluid_type: PhaseType,
        **kwargs,
    ):
        super().__init__(
            saturation_pressure=saturation_pressure,
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            fluid_type=fluid_type,
            **kwargs,
        )

    @property
    def saturation_type(self) -> str:
        return "Bubble-point" if self.fluid_type == PhaseType.OIL else "Dew-point"

    def to_dict(self) -> dict[str, Any]:
        return {
            PVTHeaders.SATURATION_PRESSURE.magic_name: np.array(self.saturation_pressure),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.FLUID_TYPE.magic_name: self.fluid_type,
            PVTHeaders.SATURATION_TYPE.magic_name: str(self.saturation_type),
        }


class CMECalculated(BaseCalculated):
    """Class for CME calculation results."""

    relative_total_volume: list[float] = Field(..., description="Relative total volume.")
    compressibility: list[float] = Field(..., description="Compressibility.")
    y_factor: list[float] = Field(..., description="Y-factor.")
    density: list[float] = Field(..., description="Density.")
    liquid_volume: list[float] = Field(..., description="Liquid volume.")
    z_factor: list[float] = Field(..., description="Z-factor.")
    equilibrium_gas_comp: list[list[float]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float]] = Field(..., description="Equilibrium oil composition.")

    def __init__(
        self,
        relative_total_volume: npt.NDArray[np.float64] | list[float],
        compressibility: npt.NDArray[np.float64] | list[float],
        y_factor: npt.NDArray[np.float64] | list[float],
        density: npt.NDArray[np.float64] | list[float],
        liquid_volume: npt.NDArray[np.float64] | list[float],
        z_factor: npt.NDArray[np.float64] | list[float],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[list[float]],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[list[float]],
        **kwargs,
    ):
        super().__init__(
            relative_total_volume=self._to_list(relative_total_volume),
            compressibility=self._to_list(compressibility),
            y_factor=self._to_list(y_factor),
            density=self._to_list(density),
            liquid_volume=self._to_list(liquid_volume),
            z_factor=self._to_list(z_factor),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            **kwargs,
        )

    def to_dict(self) -> dict[str, npt.NDArray[np.float64]]:
        return {
            PVTHeaders.RELATIVE_TOTAL_VOLUME.magic_name: np.array(self.relative_total_volume),
            PVTHeaders.COMPRESSIBILITY.magic_name: np.array(self.compressibility),
            PVTHeaders.Y_FACTOR.magic_name: np.array(self.y_factor),
            PVTHeaders.DENSITY.magic_name: np.array(self.density),
            PVTHeaders.LIQUID_VOLUME.magic_name: np.array(self.liquid_volume),
            PVTHeaders.Z_FACTOR.magic_name: np.array(self.z_factor),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
        }


class DLECalculated(BaseCalculated):
    """Class for DLE calculation results."""

    oil_formation_volume_factor_dle: list[float] = Field(..., description="Oil formation volume factor (DLE).")
    solution_gas_oil_ratio_dle: list[float] = Field(..., description="Solution gas-to-oil ratio (DLE).")
    gas_formation_volume_factor: list[float] = Field(..., description="Gas formation volume factor.")
    oil_density: list[float] = Field(..., description="Oil density.")
    z_factor: list[float] = Field(..., description="Z-factor.")
    gas_specific_gravity: list[float] = Field(..., description="Gas specific gravity.")
    oil_viscosity: list[float] = Field(..., description="Oil viscosity.")
    equilibrium_gas_comp: list[list[float]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float]] = Field(..., description="Equilibrium oil composition.")

    def __init__(
        self,
        oil_formation_volume_factor_dle: npt.NDArray[np.float64] | list[float],
        solution_gas_oil_ratio_dle: npt.NDArray[np.float64] | list[float],
        gas_formation_volume_factor: npt.NDArray[np.float64] | list[float],
        oil_density: npt.NDArray[np.float64] | list[float],
        z_factor: npt.NDArray[np.float64] | list[float],
        gas_specific_gravity: npt.NDArray[np.float64] | list[float],
        oil_viscosity: npt.NDArray[np.float64] | list[float],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[list[float]],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[list[float]],
        **kwargs,
    ):
        super().__init__(
            oil_formation_volume_factor_dle=self._to_list(oil_formation_volume_factor_dle),
            solution_gas_oil_ratio_dle=self._to_list(solution_gas_oil_ratio_dle),
            gas_formation_volume_factor=self._to_list(gas_formation_volume_factor),
            oil_density=self._to_list(oil_density),
            z_factor=self._to_list(z_factor),
            gas_specific_gravity=self._to_list(gas_specific_gravity),
            oil_viscosity=self._to_list(oil_viscosity),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            **kwargs,
        )

    def to_dict(self) -> dict[str, npt.NDArray[np.float64]]:
        return {
            PVTHeaders.OIL_FORMATION_VOLUME_FACTOR_DLE.magic_name: np.array(self.oil_formation_volume_factor_dle),
            PVTHeaders.SOLUTION_GAS_OIL_RATIO_DLE.magic_name: np.array(self.solution_gas_oil_ratio_dle),
            PVTHeaders.GAS_FORMATION_VOLUME_FACTOR.magic_name: np.array(self.gas_formation_volume_factor),
            PVTHeaders.OIL_DENSITY.magic_name: np.array(self.oil_density),
            PVTHeaders.Z_FACTOR.magic_name: np.array(self.z_factor),
            PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name: np.array(self.gas_specific_gravity),
            PVTHeaders.OIL_VISCOSITY.magic_name: np.array(self.oil_viscosity),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
        }


class SeparatorCalculated(BaseCalculated):
    """Class for separator calculation results."""

    gas_oil_ratio: list[float] = Field(..., description="Gas-to-oil ratio.")
    total_gas_oil_ratio: list[float] = Field(..., description="Total gas-to-oil ratio.")
    gas_specific_gravity: list[float] = Field(..., description="Gas specific gravity.")
    oil_density: list[float] = Field(..., description="Oil density.")
    oil_formation_volume_factor: list[float] = Field(..., description="Oil formation volume factor.")
    equilibrium_gas_comp: list[list[float]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float]] = Field(..., description="Equilibrium oil composition.")

    def __init__(
        self,
        gas_oil_ratio: npt.NDArray[np.float64] | list[float],
        total_gas_oil_ratio: npt.NDArray[np.float64] | list[float],
        gas_specific_gravity: npt.NDArray[np.float64] | list[float],
        oil_density: npt.NDArray[np.float64] | list[float],
        oil_formation_volume_factor: npt.NDArray[np.float64] | list[float],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[list[float]],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[list[float]],
        **kwargs,
    ):
        super().__init__(
            gas_oil_ratio=self._to_list(gas_oil_ratio),
            total_gas_oil_ratio=self._to_list(total_gas_oil_ratio),
            gas_specific_gravity=self._to_list(gas_specific_gravity),
            oil_density=self._to_list(oil_density),
            oil_formation_volume_factor=self._to_list(oil_formation_volume_factor),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            **kwargs,
        )

    def to_dict(self) -> dict[str, npt.NDArray[np.float64]]:
        return {
            PVTHeaders.GAS_OIL_RATIO.magic_name: np.array(self.gas_oil_ratio),
            PVTHeaders.TOTAL_GAS_OIL_RATIO.magic_name: np.array(self.total_gas_oil_ratio),
            PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name: np.array(self.gas_specific_gravity),
            PVTHeaders.OIL_DENSITY.magic_name: np.array(self.oil_density),
            PVTHeaders.OIL_FORMATION_VOLUME_FACTOR.magic_name: np.array(self.oil_formation_volume_factor),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
        }


class CVDCalculated(BaseCalculated):
    """Class for CVD calculation results."""

    liquid_volume: list[float] = Field(..., description="Liquid volume.")
    moles_gas_produced: list[float] = Field(..., description="Moles of gas produced.")
    z_factor: list[float] = Field(..., description="Z-factor.")
    two_phase_z_factor: list[float] = Field(..., description="Two-phase Z-factor.")
    oil_formation_volume_factor: list[float] = Field(..., description="Oil formation volume factor.")
    solution_gas_oil_ratio: list[float] = Field(..., description="Solution gas-to-oil ratio.")
    gas_formation_volume_factor: list[float] = Field(..., description="Gas formation volume factor.")
    oil_density: list[float] = Field(..., description="Oil density.")
    gas_specific_gravity: list[float] = Field(..., description="Gas specific gravity.")
    equilibrium_gas_comp: list[list[float]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float]] = Field(..., description="Equilibrium oil composition.")

    def __init__(
        self,
        liquid_volume: npt.NDArray[np.float64] | list[float],
        moles_gas_produced: npt.NDArray[np.float64] | list[float],
        z_factor: npt.NDArray[np.float64] | list[float],
        two_phase_z_factor: npt.NDArray[np.float64] | list[float],
        oil_formation_volume_factor: npt.NDArray[np.float64] | list[float],
        solution_gas_oil_ratio: npt.NDArray[np.float64] | list[float],
        gas_formation_volume_factor: npt.NDArray[np.float64] | list[float],
        oil_density: npt.NDArray[np.float64] | list[float],
        gas_specific_gravity: npt.NDArray[np.float64] | list[float],
        equilibrium_gas_comp: npt.NDArray[np.float64] | list[list[float]],
        equilibrium_oil_comp: npt.NDArray[np.float64] | list[list[float]],
        **kwargs,
    ):
        super().__init__(
            liquid_volume=self._to_list(liquid_volume),
            moles_gas_produced=self._to_list(moles_gas_produced),
            z_factor=self._to_list(z_factor),
            two_phase_z_factor=self._to_list(two_phase_z_factor),
            oil_formation_volume_factor=self._to_list(oil_formation_volume_factor),
            solution_gas_oil_ratio=self._to_list(solution_gas_oil_ratio),
            gas_formation_volume_factor=self._to_list(gas_formation_volume_factor),
            oil_density=self._to_list(oil_density),
            gas_specific_gravity=self._to_list(gas_specific_gravity),
            equilibrium_gas_comp=self._to_list(equilibrium_gas_comp),
            equilibrium_oil_comp=self._to_list(equilibrium_oil_comp),
            **kwargs,
        )

    def to_dict(self) -> dict[str, npt.NDArray[np.float64]]:
        return {
            PVTHeaders.LIQUID_VOLUME.magic_name: np.array(self.liquid_volume),
            PVTHeaders.MOLES_GAS_PRODUCED.magic_name: np.array(self.moles_gas_produced),
            PVTHeaders.Z_FACTOR.magic_name: np.array(self.z_factor),
            PVTHeaders.TWO_PHASE_Z_FACTOR.magic_name: np.array(self.two_phase_z_factor),
            PVTHeaders.OIL_FORMATION_VOLUME_FACTOR.magic_name: np.array(self.oil_formation_volume_factor),
            PVTHeaders.SOLUTION_GAS_OIL_RATIO.magic_name: np.array(self.solution_gas_oil_ratio),
            PVTHeaders.GAS_FORMATION_VOLUME_FACTOR.magic_name: np.array(self.gas_formation_volume_factor),
            PVTHeaders.OIL_DENSITY.magic_name: np.array(self.oil_density),
            PVTHeaders.GAS_SPECIFIC_GRAVITY.magic_name: np.array(self.gas_specific_gravity),
            PVTHeaders.EQUILIBRIUM_GAS_COMP.magic_name: np.array(self.equilibrium_gas_comp),
            PVTHeaders.EQUILIBRIUM_OIL_COMP.magic_name: np.array(self.equilibrium_oil_comp),
        }
