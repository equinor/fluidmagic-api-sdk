"""File for EOSData."""

from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, Field

from ...utilities.utils import cast_to_np_array
from ..enums import EOSType


class EOSData(BaseModel):
    """Pydantic model for data transfer, validation and serialization across boundaries.

    Attributes:
        eos_type: EOS type.
        component_names: Component names.
        critical_temperatures: Critical temperatures.
        critical_pressures: Critical pressures.
        acentric_factors: Acentric factors.
        binary_interaction_parameters: Binary interaction parameters.
        volume_shifts: Volume shifts.
        molecular_weights: Molecular weights.
        upper_molecular_weights: Upper molecular weights.
        surface_volume_shifts: Surface volume shift parameters.
        parachors: Used for calculation of gas-oil interfacial tension (IFT)
        omega_a: Omega A list.
        omega_b: Omega B list.
        component_heating_values: Gross heating values, used to calculate component heating values in EOS.
        temperature_for_reservoir_volume_shift: Temperature for reservoir volume shift.
        liquid_densities: Liquid densities.
        critical_volumes: Critical volumes.
        lbc_coefficients: Lorentz Bray Clark coefficients.
        csp_coefficients: Corresponding states principle coefficients.
        volume_corrections: Peneloux volume correction (Only used when writing eos to file).
        temperature_gradient: Peneloux temperature gradient (Only used when writing eos to file).
        boiling_temperatures: Boiling temperature for components (Only used when writing eos to file).
        name: EOS name.
        is_csp_model: If EOS model is using CSP viscosity.
    """

    eos_type: EOSType = Field(..., description="EOS type.")
    component_names: list[str] = Field(..., description="Component names. N2, CO2, C1...")
    critical_temperatures: list[float] = Field(..., description="Critical temperatures [kelvin].")
    critical_pressures: list[float] = Field(..., description="Critical pressures [bar].")
    acentric_factors: list[float] = Field(..., description="Acentric factors.")
    binary_interaction_parameters: list[list[float]] = Field(..., description="Binary interaction parameters.")
    volume_shifts: list[float] = Field(..., description="Volume shifts.")
    molecular_weights: list[float] = Field(..., description="Molecular weights.")
    upper_molecular_weights: list[float] | None = Field(..., description="Upper molecular weights.")
    surface_volume_shifts: list[float] | None = Field(..., description="Surface volume shift parameters.")
    parachors: list[float] | None = Field(..., description="Used for calculation of gas-oil interfacial tension (IFT)")
    omega_a: list[float] | None = Field(..., description="Omega A list.")
    omega_b: list[float] | None = Field(..., description="Omega B list.")
    component_heating_values: list[float] | None = Field(
        ..., description="Gross heating values, used to calculate component heating values in EOS."
    )
    temperature_for_reservoir_volume_shift: float | None = Field(
        ..., description="Temperature for reservoir volume shift."
    )
    liquid_densities: list[float] | None = Field(..., description="Liquid densities.")
    critical_volumes: list[float] | None = Field(..., description="Critical volumes.")
    lbc_coefficients: list[float] | None = Field(..., description="Lorentz Bray Clark coefficients.")
    csp_coefficients: list[float] | None = Field(..., description="Corresponding states principle coefficients.")
    volume_corrections: list[float] | None = Field(
        ..., description="Peneloux volume correction (Only used when writing eos to file)."
    )
    temperature_gradient: list[float] | None = Field(
        ..., description="Peneloux temperature gradient (Only used when writing eos to file)."
    )
    boiling_temperatures: list[float] | None = Field(
        ..., description="Boiling temperature for components (Only used when writing eos to file)."
    )
    name: str | None = Field(..., description="EOS name.")
    is_csp_model: bool | None = Field(..., description="If EOS model is using CSP viscosity.")

    def __init__(
        self,
        eos_type: EOSType | str,
        component_names: list[str] | npt.NDArray[np.str_],
        critical_temperatures: list[float] | npt.NDArray[np.float64],
        critical_pressures: list[float] | npt.NDArray[np.float64],
        acentric_factors: list[float] | npt.NDArray[np.float64],
        binary_interaction_parameters: list[list[float]] | npt.NDArray[np.float64],
        volume_shifts: list[float] | npt.NDArray[np.float64],
        molecular_weights: list[float] | npt.NDArray[np.float64],
        upper_molecular_weights: list[float] | npt.NDArray[np.float64] | None = None,
        surface_volume_shifts: list[float] | npt.NDArray[np.float64] | None = None,
        parachors: list[float] | npt.NDArray[np.float64] | None = None,
        omega_a: list[float] | npt.NDArray[np.float64] | None = None,
        omega_b: list[float] | npt.NDArray[np.float64] | None = None,
        component_heating_values: list[float] | npt.NDArray[np.float64] | None = None,
        temperature_for_reservoir_volume_shift: float | np.float64 | None = None,
        liquid_densities: list[float] | npt.NDArray[np.float64] | None = None,
        critical_volumes: list[float] | npt.NDArray[np.float64] | None = None,
        lbc_coefficients: list[float] | npt.NDArray[np.float64] | None = None,
        csp_coefficients: list[float] | npt.NDArray[np.float64] | None = None,
        volume_corrections: list[float] | npt.NDArray[np.float64] | None = None,
        temperature_gradient: list[float] | npt.NDArray[np.float64] | None = None,
        boiling_temperatures: list[float] | npt.NDArray[np.float64] | None = None,
        name: str | None = None,
        is_csp_model: bool = False,
        **kwargs,
    ):
        """Create EOS data and cast all data to the format EOS expects (mostly Numpy arrays).

        Args:
            eos_type: EOS type.
            component_names: Component names.
            critical_temperatures: Critical temperatures.
            critical_pressures: Critical pressures.
            acentric_factors: Acentric factors.
            binary_interaction_parameters: Binary interaction parameters.
            volume_shifts: Volume shifts.
            molecular_weights: Molecular weights.
            upper_molecular_weights: Upper molecular weights. Defaults to None.
            surface_volume_shifts: Surface volume shift parameters. Defaults to None.
            parachors: Used for calculation of gas-oil interfacial tension (IFT). Defaults to None.
            omega_a: Omega A list. Defaults to None.
            omega_b: Omega B list. Defaults to None.
            component_heating_values: Component heating values. Defaults to None.
            temperature_for_reservoir_volume_shift: Temperature for reservoir volume shift. Defaults to None.
            liquid_densities: Liquid densities. Defaults to None.
            critical_volumes: Critical volumes. Defaults to None.
            lbc_coefficients: Lorentz Bray Clark coefficients. Defaults to None.
            csp_coefficients: Corresponding states principle coefficients. Defaults to None.
            volume_corrections: Peneloux volume correction. Defaults to None.
            temperature_gradient: Peneloux temperature gradient. Defaults to None.
            boiling_temperatures: Boiling temperature for components (Only used when writing EOS to file).
                Defaults to None.
            name: EOS name. Defaults to None.
            is_csp_model: If EOS model is using CSP viscosity.
        """
        super().__init__(
            eos_type=EOSType(eos_type),
            component_names=list(component_names),
            critical_temperatures=list(critical_temperatures),
            critical_pressures=list(critical_pressures),
            acentric_factors=list(acentric_factors),
            binary_interaction_parameters=list(binary_interaction_parameters),
            volume_shifts=list(volume_shifts),
            molecular_weights=list(molecular_weights),
            upper_molecular_weights=self._down_cast(upper_molecular_weights),
            surface_volume_shifts=self._down_cast(surface_volume_shifts),
            parachors=self._down_cast(parachors),
            omega_a=self._down_cast(omega_a),
            omega_b=self._down_cast(omega_b),
            component_heating_values=self._down_cast(component_heating_values),
            temperature_for_reservoir_volume_shift=self._cast_to_float(temperature_for_reservoir_volume_shift),
            liquid_densities=self._down_cast(liquid_densities),
            critical_volumes=self._down_cast(critical_volumes),
            lbc_coefficients=self._down_cast(lbc_coefficients),
            csp_coefficients=self._down_cast(csp_coefficients),
            volume_corrections=self._down_cast(volume_corrections),
            temperature_gradient=self._down_cast(temperature_gradient),
            boiling_temperatures=self._down_cast(boiling_temperatures),
            name=name,
            is_csp_model=is_csp_model,
            **kwargs,
        )

    def __eq__(self, other: Any) -> bool:
        """Overwrite default comparator to allow comparison between EOSData objects. Check object equality.

        Args:
            other: The EOSData object to compare with.

        Returns:
            If EOSData objects are equal.

        Raises:
            ValueError: If objects have different attributes (keys).
        """
        if not isinstance(other, EOSData):
            return NotImplemented
        keys, other_keys = vars(self), vars(other)
        if diff := set(keys).symmetric_difference(other_keys):
            raise ValueError(f"Object attributes are not the same, can not compare objects. Different keys: {diff}.")

        return self.all_close(other)

    def to_numpy(self):
        """Upcast all attributes to numpy arrays and enum for EOS object.

        Returns:
            All EOSData attributes cast to EOS appropriate formats.
        """
        return (
            self.eos_type,
            np.array(self.component_names).astype(str),
            np.array(self.critical_temperatures),
            np.array(self.critical_pressures),
            np.array(self.acentric_factors),
            np.array(self.binary_interaction_parameters),
            np.array(self.volume_shifts),
            np.array(self.molecular_weights),
            cast_to_np_array(self.upper_molecular_weights),
            cast_to_np_array(self.surface_volume_shifts),
            cast_to_np_array(self.parachors),
            cast_to_np_array(self.omega_a),
            cast_to_np_array(self.omega_b),
            cast_to_np_array(self.component_heating_values),
            self._cast_to_float(self.temperature_for_reservoir_volume_shift),
            cast_to_np_array(self.liquid_densities),
            cast_to_np_array(self.critical_volumes),
            cast_to_np_array(self.lbc_coefficients),
            cast_to_np_array(self.csp_coefficients),
            cast_to_np_array(self.boiling_temperatures),
            self.name,
            self.is_csp_model,
        )

    def all_close(self, other: EOSData, **kwargs) -> bool:
        """Check if two EOSData objects are equal*.

        *With rtol and atol values specified in kwargs or the default used by numpy.

        Args:
            other: EOSData object to be compared.
            **kwargs: Keyword arguments for numpy comparison.

        Returns:
            If the two EOSData objects are equal/close.

        Raises:
            ValueError: If objects have different attributes (keys).
        """
        keys, other_keys = vars(self), vars(other)
        if diff := set(keys).symmetric_difference(other_keys):
            raise ValueError(f"Object attributes are not the same, can not compare objects. Different keys: {diff}.")

        for key in keys:
            self_ = vars(self)[key]
            other_ = vars(other)[key]

            if not isinstance(self_, type(other_)):
                raise TypeError(f"'{key}' is not same type!")

            if isinstance(self_, list):
                self_ = np.array(self_)
                other_ = np.array(other_)

            if isinstance(self_, np.ndarray):
                if np.issubdtype(self_.dtype, np.number):
                    if np.allclose(self_, other_, **kwargs) is False:
                        return False
                else:
                    if not np.all(self_ == other_):
                        return False
            elif isinstance(self_, float):
                if np.isclose(self_, other_, **kwargs) is False:
                    return False
            else:
                if self_ != other_:
                    return False
        return True

    def diff(self, other: EOSData) -> str:
        """Generate difference between two EOSData objects in a human-readable format.

        Args:
            other: EOSData object to be compared.

        Returns:
            Human-readable difference between two EOSData objects.
        """
        result = ["EOS DIFFERENCE:"]
        keys, other_keys = vars(self), vars(other)
        if diff := set(keys).symmetric_difference(other_keys):
            result.append(f"Attribute difference: {diff}.")
            keys = set(keys).intersection(other_keys)

        for key in keys:
            self_ = getattr(self, key)
            other_ = getattr(other, key)
            if np.any(self_ != other_):
                if not isinstance(self_, type(other_)):
                    result.append(f"Attribute '{key}' is a different type.")
                    continue
                if key == "binary_interaction_parameters":
                    continue
                result.append(f"Attribute '{key}' difference:")
                if isinstance(self_, float):
                    self_ = np.array([self_])
                    other_ = np.array([other_])
                if isinstance(self_, list):
                    self_ = np.array(self_)
                    other_ = np.array(other_)
                if isinstance(self_, (np.ndarray, np.generic)):
                    result.append(f"Self:  {', '.join([f'{f:>8.3f}' for f in self_])}")
                    result.append(f"Other: {', '.join([f'{f:>8.3f}' for f in other_])}")
                    result.append(f"Diff:  {', '.join([f'{f:>8.3f}' for f in other_ - self_])}")
                else:
                    result.append(f"Difference display for type '{type(self_)}' has not been implemented.")

        return "\n".join(result)

    @staticmethod
    def _cast_to_np_array(data: list[float | list[float] | str] | None) -> npt.NDArray[np.float64 | np.str_] | None:
        """Cast data to a Numpy array if it is not None."""
        return np.array(data) if data is not None else None

    @staticmethod
    def _down_cast(data: list[float | list[float] | str] | None) -> npt.NDArray[np.float64 | np.str_] | None:
        if isinstance(data, np.ndarray):
            return data.tolist()
        return data

    @staticmethod
    def _cast_to_float(data: float | np.float64 | None) -> float | None:
        """Cast data to float if it is not None."""
        return float(data) if data is not None else None
