"""Classes and constants for handling headers."""

from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cache
from typing import Any

from pandas import Timestamp


@dataclass(frozen=True)
class Units:
    """Common units found in Headers."""

    DAY = "d"
    DAYS = "days"
    MONTH = "month"
    YEAR = "year"
    DATE = "date"
    STRING = "string"
    INTEGER = "integer"
    REAL = "real"
    METER = "m"
    CUBIC_METER = "m3"
    STANDARD_CUBIC_METER = "sm3"
    ACTUAL_CUBIC_METER = "am3"
    STANDARD_CUBIC_METER_PER_STANDARD_CUBIC_METER = f"{STANDARD_CUBIC_METER}/{STANDARD_CUBIC_METER}"
    CUBIC_METER_PER_DAY = f"{CUBIC_METER}/{DAY}"
    CUBIC_METER_PER_STANDARD_CUBIC_METER = f"{CUBIC_METER}/{STANDARD_CUBIC_METER}"
    STANDARD_CUBIC_METER_PER_DAY = f"{STANDARD_CUBIC_METER}/{DAY}"
    ACTUAL_CUBIC_METER_PER_DAY = f"{ACTUAL_CUBIC_METER}/{DAY}"
    BAR = "bar"
    KILOGRAM = "kg"
    KILOGRAM_PER_DAY = f"{KILOGRAM}/{DAY}"
    MOLE = "mol"
    KILOGRAM_MOLE = "kgmol"
    KILO_MOLES_PER_DAY = f"{KILOGRAM_MOLE}/{DAY}"
    KILOGRAM_PER_KILOGRAM_MOLE = f"{KILOGRAM}/{KILOGRAM_MOLE}"
    KILOGRAM_PER_CUBIC_METER = f"{KILOGRAM}/{CUBIC_METER}"
    CELSIUS = "c"
    KELVIN = "k"
    MEGAJOULE = "mj"
    CUBIC_METER_PER_KILOGRAM_MOLE = f"{CUBIC_METER}/{KILOGRAM_MOLE}"
    MEGAJOULE_PER_CUBIC_METER = f"{MEGAJOULE}/{CUBIC_METER}"
    MOLE_FRACTION = f"{MOLE}-%"
    CENTIPOISE = "cp"
    NEWTON_PER_METER = "N/m"
    NEWTON = "N"
    BAR_INVERSE = f"1/{BAR}"

    @classmethod
    def get_units_list(cls) -> list[str]:
        """Return all values as a list of strings."""
        return [value for key, value in vars(cls).items() if not key.startswith("__") and isinstance(value, str)]


@dataclass(order=True)
class Header:
    """Datastructures for single header.

    Custom equality `==` check allows a `_Header` to be compared to both tuples and strings with similar content.
    The equality check is case-agnostic:
        `_Header(name, unit) == `"name unit"`
        `_Header(name, unit) == `"(name unit)"`
        `_Header(name, unit) == `" ( NAME,   unit ) "`
        `_Header(name, unit) == `("name", "UNIT")`


    Attributes:
        name: The name of header, e.g. c12, z-c1-c2.
        unit: The unit of header, e.g. kg, mol, bar.
        full: Tuple representation of name and unit.
        ecl_name: The eclipse version of the header name.
        alt_name: Alternative version of the header name.
        magic_name: Name used in a magic file corresponding to this header.
        is_identifier: Whether it identifies a specific field or well.
    """

    name: str
    unit: str
    full: tuple[str, str]
    ecl_name: str | None
    alt_name: str | None
    magic_name: str | None
    is_identifier: bool = field(default=False)

    # NOTE: Possibility to validate unit to allow/disallow creation here.
    def __init__(
        self,
        name: str | tuple[str, str],
        unit: str | None = None,
        ecl_name: str | None = None,
        alt_name: str | None = None,
        magic_name: str | None = None,
        is_identifier: bool = False,
    ) -> None:
        """Create a new header.

        Args:
            name: The name associated with this header. Either a string or a tuple of name and unit strings.
            unit: The unit, if any, associated with this header. Defaults to None.
            ecl_name: The Eclipse-name, if any, associated with this header. Defaults to None.
            alt_name: The alternative name, if any, associated with this header. Defaults to None.
            magic_name: The FluidMagic name, if any, associated with this header. Defaults to None.
            is_identifier: Whether it identifies a specific field or well. Defaults to False.

        Raises:
            ValueError: If the type or shape of arguments are incorrect.
        """
        if unit is None:
            if isinstance(name, tuple):
                if len(name) != 2:
                    raise ValueError("If first argument is a tuple of name and unit, it must have length 2.")
                self.full = name[0].lower(), name[1].lower()
                self.name, self.unit = self.full
            else:
                raise ValueError("Could not create Header, missing unit argument.")
        else:
            if not isinstance(name, str):
                raise ValueError("If unit is supplied as an argument the name must be a string.")
            self.name, self.unit = name.lower(), unit.lower()
            self.full = self.name, self.unit

        self.ecl_name = ecl_name
        self.alt_name = alt_name
        self.magic_name = magic_name
        self.is_identifier = is_identifier

    @staticmethod
    def get_unit_primitive(unit: str) -> type:
        """Get the unit primitive type for a given unit.

        Args:
            unit: Unit string.

        Returns:
            Primitive type for unit e.g. int, float, string.
        """
        if unit in [Units.DATE]:
            return Timestamp
        if unit in [Units.INTEGER]:
            return int
        if unit in [
            Units.DAY,
            Units.DAYS,
            Units.MONTH,
            Units.YEAR,
            Units.REAL,
            Units.METER,
            Units.CUBIC_METER,
            Units.STANDARD_CUBIC_METER,
            Units.ACTUAL_CUBIC_METER,
            Units.STANDARD_CUBIC_METER_PER_STANDARD_CUBIC_METER,
            Units.CUBIC_METER_PER_DAY,
            Units.CUBIC_METER_PER_STANDARD_CUBIC_METER,
            Units.STANDARD_CUBIC_METER_PER_DAY,
            Units.ACTUAL_CUBIC_METER_PER_DAY,
            Units.BAR,
            Units.KILOGRAM,
            Units.KILOGRAM_PER_DAY,
            Units.MOLE,
            Units.KILOGRAM_MOLE,
            Units.KILO_MOLES_PER_DAY,
            Units.KILOGRAM_PER_KILOGRAM_MOLE,
            Units.KILOGRAM_PER_CUBIC_METER,
            Units.CELSIUS,
            Units.KELVIN,
            Units.MEGAJOULE,
            Units.CUBIC_METER_PER_KILOGRAM_MOLE,
            Units.MEGAJOULE_PER_CUBIC_METER,
            Units.MOLE_FRACTION,
            Units.CENTIPOISE,
            Units.NEWTON_PER_METER,
            Units.NEWTON,
            Units.BAR_INVERSE,
        ]:
            return float
        if unit in [Units.STRING]:
            return str
        raise ValueError(f"Could not find primitive for unit {unit}.")

    def __str__(self) -> str:
        """String representation of Header."""
        return f"{self.name} ({self.unit})"

    def __len__(self) -> int:
        """Get length of Header, should always be 2."""
        return len(self.full)

    def __iter__(self) -> Iterator:
        """Custom iterator yielding name and unit."""
        yield from [self.name, self.unit]

    def __eq__(self, other: Any) -> bool:
        """Custom equality check for Header, case agnostic.

        Args:
            other: Name-unit pair to check against.

        Returns:
            True if matched, False otherwise.
        """
        if isinstance(other, Header):
            return (self.name, self.unit) == (other.name, other.unit)
        if isinstance(other, tuple):
            return (self.name, self.unit) == (other[0].lower(), other[1].lower())
        if isinstance(other, str):
            if other.strip().startswith("(") and other.strip().endswith(")"):
                other = other.replace("(", "", 1)
                other = other.rstrip()[:-1]
            if other.count(",") >= 1:
                other = other.replace(",", " ", 1)

            other = other.split()
            if len(other) == 2:
                return (self.name, self.unit) == (other[0].lower(), other[1].lower())

            if len(other) == 1:
                if other[0] in [self.alt_name, self.name, self.ecl_name, self.magic_name]:
                    return True
            return False

        return NotImplemented

    def get_all_names(self) -> list[str]:
        """Flattens all the optional names to a single list.

        Returns:
            All possible names for header.
        """
        return [name for name in [self.name, self.ecl_name, self.alt_name, self.magic_name] if name]


class MetaHeaders(type):
    """Metaclass implementing commonly used methods for Headers, e.g. __iter__."""

    def __iter__(self) -> Iterator:
        for attr in dir(self):
            value = getattr(self, attr)
            if isinstance(value, Header):
                yield value

    def get_header_by_name(self, search_name: str) -> Header | None:
        """Get header only by name.

        Args:
            search_name: The name to look for.

        Returns:
            The correct header if it exists.
        """
        search_name_lower = search_name.lower()
        attr_names = ["name", "ecl_name", "alt_name", "magic_name"]
        for attr in dir(self):
            header = getattr(self, attr)
            if isinstance(header, Header):
                if any(search_name_lower == getattr(header, attr_name, None) for attr_name in attr_names):
                    return header
        return None

    def get_pretty_print(self, search_name: str) -> str:
        """Format header for printing.

        Args:
            search_name: The name to look for.

        Returns:
            The correct header pretty formatted.
        """
        for attr_name in dir(self):
            header = getattr(self, attr_name)
            if isinstance(header, Header):
                if any(
                    search_name == getattr(header, name_attr, "")
                    for name_attr in ["name", "ecl_name", "alt_name", "magic_name"]
                ):
                    # Format the attr_name for pretty print
                    return " ".join(word.capitalize() for word in attr_name.split("_"))
        return search_name


@dataclass(frozen=True)
class Headers(metaclass=MetaHeaders):
    """Container for headers."""

    PVTNUM = Header("pvtnum", Units.INTEGER)
    OIL_VOLUME = Header("oil_vol", Units.STANDARD_CUBIC_METER_PER_DAY, alt_name="vol-oil")
    GAS_VOLUME = Header("gas_vol", Units.STANDARD_CUBIC_METER_PER_DAY, alt_name="vol-gas")
    NGL_VOLUME = Header("ngl_vol", Units.STANDARD_CUBIC_METER_PER_DAY, ecl_name="nglvol")
    TOTAL_VOLUME = Header("total_vol", Units.STANDARD_CUBIC_METER_PER_DAY, ecl_name="totvol")
    WATER_VOLUME = Header("water_vol", Units.STANDARD_CUBIC_METER_PER_DAY)
    OIL_DENSITY = Header("oil_dens", Units.KILOGRAM_PER_CUBIC_METER, alt_name="oildens", magic_name="deno")
    GAS_DENSITY = Header("gas_dens", Units.KILOGRAM_PER_CUBIC_METER, alt_name="gasdens", magic_name="deng")
    NGL_DENSITY = Header("ngl_dens", Units.KILOGRAM_PER_CUBIC_METER, alt_name="ngldens")
    INJECTION_TRACER_FRACTION = Header("injtrace_fraction", Units.REAL, ecl_name="igt_frac")
    RESERVOIR_PRESSURE = Header("reservoir_pres", Units.BAR, ecl_name="p-res", alt_name="res_pres")
    RESERVOIR_TEMPERATURE = Header("reservoir_temp", Units.CELSIUS, ecl_name="t-res", alt_name="res_temp")
    EXPERIMENT_TYPE = Header("experiment-type", Units.STRING, alt_name="exp")
    MOLES = Header("molarstream_", Units.KILO_MOLES_PER_DAY, ecl_name="z-")
    INJECTION_GAS = Header("injectiongas", Units.KILO_MOLES_PER_DAY, ecl_name="i-", magic_name="yinj")
    LIFT_GAS = Header("liftgas_", Units.KILO_MOLES_PER_DAY, "lg-")
    LIFT_GAS_VOLUME = Header("liftgas_vol", Units.STANDARD_CUBIC_METER_PER_DAY, alt_name="vol-liftgas")
    NET_GAS_VOLUME = Header("netgas_vol", Units.STANDARD_CUBIC_METER_PER_DAY)
    SEPARATOR_PRESSURE = Header("sep_pres", Units.BAR, alt_name="p-sep")
    SEPARATOR_TEMPERATURE = Header("sep_temp", Units.CELSIUS)
    GAS_GRAVITY = Header("gas_gravity", Units.REAL)
    OIL_MOLES = Header("oil_moles", Units.KILO_MOLES_PER_DAY, alt_name="xoil")
    GAS_MOLES = Header("gas_moles", Units.KILO_MOLES_PER_DAY, alt_name="ygas")
    NGL_MOLES = Header("ngl_moles", Units.KILO_MOLES_PER_DAY)
    TOTAL_MOLES = Header("total_moles", Units.KILO_MOLES_PER_DAY)
    OIL_MOLAR_COMPOSITION = Header("oil_molarcomp", Units.MOLE_FRACTION)
    GAS_MOLAR_COMPOSITION = Header("gas_molarcomp", Units.MOLE_FRACTION, alt_name="gasmolarcomp")
    NGL_MOLAR_COMPOSITION = Header("ngl_molarcomp", Units.MOLE_FRACTION)
    TOTAL_MOLAR_COMPOSITION = Header("total_molarcomp", Units.MOLE_FRACTION)
    OIL_MASS_COMPOSITION = Header("oil_masscomp", Units.MOLE_FRACTION)
    GAS_MASS_COMPOSITION = Header("gas_masscomp", Units.MOLE_FRACTION)
    NGL_MASS_COMPOSITION = Header("ngl_masscomp", Units.MOLE_FRACTION)
    TOTAL_MASS_COMPOSITION = Header("total_masscomp", Units.MOLE_FRACTION)
    OIL_MASS_STREAM = Header("oil_massstream", Units.KILOGRAM_PER_DAY)
    GAS_MASS_STREAM = Header("gas_massstream", Units.KILOGRAM_PER_DAY)
    NGL_MASS_STREAM = Header("ngl_massstream", Units.KILOGRAM_PER_DAY)
    OIL_MASS = Header("oil_mass", Units.KILOGRAM_PER_DAY)
    GAS_MASS = Header("gas_mass", Units.KILOGRAM_PER_DAY)
    NGL_MASS = Header("ngl_mass", Units.KILOGRAM_PER_DAY)
    TOTAL_MASS = Header("total_mass", Units.KILOGRAM_PER_DAY)
    OIL_MOLAR_STREAM = Header("oil_molarstream", Units.KILO_MOLES_PER_DAY)
    GAS_MOLAR_STREAM = Header("gas_molarstream", Units.KILO_MOLES_PER_DAY)
    NGL_MOLAR_STREAM = Header("ngl_molarstream", Units.KILO_MOLES_PER_DAY)
    TOTAL_MOLAR_STREAM = Header("total_molarstream", Units.KILO_MOLES_PER_DAY)
    OIL_MOLECULAR_WEIGHT = Header("oil_molweight", Units.KILOGRAM_PER_KILOGRAM_MOLE)
    GAS_MOLECULAR_WEIGHT = Header("gas_molweight", Units.KILOGRAM_PER_KILOGRAM_MOLE)
    NGL_MOLECULAR_WEIGHT = Header("ngl_molweight", Units.KILOGRAM_PER_KILOGRAM_MOLE)
    TOTAL_MOLECULAR_WEIGHT = Header("total_molweight", Units.KILOGRAM_PER_KILOGRAM_MOLE)
    GAS_HEAT = Header("gas_heat", Units.MEGAJOULE_PER_CUBIC_METER)
    LAB = Header("lab_", MOLES.unit)
    VAPOR_PRESSURE = Header("oil_vpcr4", Units.BAR)
    # These headers are borderline placeholders and will only be seen by the user if they do not specify an output file.
    TOT_MOLAR_STREAM = Header(f"tot_{MOLES.name}", MOLES.unit)
    NET_MOLAR_STREAM = Header(f"net_{MOLES.name}", MOLES.unit)

    TIME = Header("time", Units.DAYS)
    DATE = Header("date", Units.DATE)
    WELL = Header("well", Units.STRING, is_identifier=True)
    ID = Header("id", Units.STRING, is_identifier=True)
    FLUID_ID = Header("fluid_id", Units.STRING, is_identifier=True)
    MWP = Header("mwp", Units.KILOGRAM_PER_KILOGRAM_MOLE)
    ALPHA = Header("alpha", Units.REAL)
    PROCESS = Header("process", Units.STRING)

    # Rates
    # NOTE: Eclipse names
    WELL_OIL_PRODUCTION_RATE = Header("wopr", Units.STANDARD_CUBIC_METER_PER_DAY)
    WELL_GAS_PRODUCTION_RATE = Header("wgpr", Units.STANDARD_CUBIC_METER_PER_DAY)
    WELL_WATER_PRODUCTION_RATE = Header("wwpr", Units.STANDARD_CUBIC_METER_PER_DAY)
    WELL_GAS_INJECTION_RATE = Header("wgir", Units.STANDARD_CUBIC_METER_PER_DAY)
    FIELD_OIL_PRODUCTION_RATE = Header("fopr", Units.STANDARD_CUBIC_METER_PER_DAY)
    WELL_TRACER_PRODUCTION_RATE = Header("wtpr", Units.STANDARD_CUBIC_METER_PER_DAY)
    CONNECTION_OIL_PRODUCTION_RATE = Header("copr", Units.STANDARD_CUBIC_METER_PER_DAY)
    CONNECTION_GAS_PRODUCTION_RATE = Header("cgpr", Units.STANDARD_CUBIC_METER_PER_DAY)
    CONNECTION_TRACER_PRODUCTION_RATE = Header("ctpr", Units.STANDARD_CUBIC_METER_PER_DAY)
    # NOTE: Internal use only, not in Eclipse.
    # WGIR - ecl equivalent
    AVERAGE_GAS_INJECTION_RATE = Header("avg_ginj", Units.STANDARD_CUBIC_METER_PER_DAY)

    # Total injection/production
    WELL_TRACER_PRODUCTION_TOTAL = Header("wtpt", Units.STANDARD_CUBIC_METER)
    CONNECTION_TRACER_PRODUCTION_TOTAL = Header("ctpt", Units.STANDARD_CUBIC_METER)

    # NOTE: All eclipse names
    WELL_OIL_PRODUCTION_TOTAL = Header("wopt", Units.STANDARD_CUBIC_METER)
    WELL_GAS_PRODUCTION_TOTAL = Header("wgpt", Units.STANDARD_CUBIC_METER)
    WELL_WATER_PRODUCTION_TOTAL = Header("wwpt", Units.STANDARD_CUBIC_METER)
    WELL_GAS_INJECTION_TOTAL = Header("wgit", Units.STANDARD_CUBIC_METER)
    FIELD_OIL_PRODUCTION_TOTAL = Header("fopt", Units.STANDARD_CUBIC_METER)
    FIELD_GAS_PRODUCTION_TOTAL = Header("fgpt", Units.STANDARD_CUBIC_METER)
    FIELD_WATER_PRODUCTION_TOTAL = Header("fwpt", Units.STANDARD_CUBIC_METER)
    CONNECTION_OIL_PRODUCTION_TOTAL = Header("copt", Units.STANDARD_CUBIC_METER)
    CONNECTION_GAS_PRODUCTION_TOTAL = Header("cgpt", Units.STANDARD_CUBIC_METER)

    # Pressures
    # NOTE: Eclipse headers
    WELL_BOTTOM_HOLE_PRESSURE = Header("wbhp", Units.BAR)
    WELL_TUBING_HEAD_PRESSURE = Header("wthp", Units.BAR)
    WELL_BLOCK_PRESSURE = Header("wbpr", Units.BAR)
    ONE_POINT_PRESSURE_AVERAGE = Header("wbp", Units.BAR)
    NINE_POINT_PRESSURE_AVERAGE = Header("wbp9", Units.BAR)
    FIELD_AVERAGE_PRESSURE = Header("fpr", Units.BAR)
    CONNECTION_PRESSURE = Header("cpr", Units.BAR)

    # NOTE: Internal use only, not in Eclipse.
    UPTIME_OIL = Header("uptime_oil", Units.REAL)
    UPTIME_GAS = Header("uptime_gas", Units.REAL)

    # NOTE: Internal use only, not in Eclipse.
    # Also called surface x from res x
    OIL_VOLUME_ORIGINATING_RESERVOIR_OIL = Header(
        "oil_vol_ro", Units.STANDARD_CUBIC_METER_PER_DAY, ecl_name="vol-oil-ro"
    )
    OIL_VOLUME_ORIGINATING_RESERVOIR_GAS = Header(
        "oil_vol_rg", Units.STANDARD_CUBIC_METER_PER_DAY, ecl_name="vol-oil-rg"
    )
    NGL_VOLUME_ORIGINATING_RESERVOIR_OIL = Header("ngl_vol_ro", Units.STANDARD_CUBIC_METER_PER_DAY)
    NGL_VOLUME_ORIGINATING_RESERVOIR_GAS = Header("ngl_vol_rg", Units.STANDARD_CUBIC_METER_PER_DAY)
    GAS_VOLUME_ORIGINATING_RESERVOIR_OIL = Header("gas_vol_ro", Units.STANDARD_CUBIC_METER_PER_DAY)
    GAS_VOLUME_ORIGINATING_RESERVOIR_GAS = Header("gas_vol_rg", Units.STANDARD_CUBIC_METER_PER_DAY)

    # Temp headers, never shown to users.
    PRESSURE_ADJUSTMENT = Header("pressure_adjustment", "tmp")
    THROUGHPUT = Header("throughput", "tmp")

    @staticmethod
    @cache
    def get_headers_list(get_name: bool = True, get_unit: bool = False, include_alt_names: bool = False) -> list[str]:
        """Get all headers from class Headers as a list of strings.

        Args:
            get_name: Whether the returned list should include name part of header.
            get_unit: Whether the returned list should include unit part of header.
            include_alt_names: Whether to include all alternative names for each header.

        Returns:
            List of strings with all header names from Headers class.
        """
        result = []
        for header in vars(Headers).values():
            if isinstance(header, Header):
                names = header.get_all_names() if include_alt_names else [header.name]

                for name in names:
                    result.append(
                        f"{name if get_name else ''}{' ' if get_name and get_unit else ''}"
                        + f"{header.unit if get_unit else ''}"
                    )
        return result

    @staticmethod
    def _filter_by_prefix(names: list[str], prefix: str) -> list[str]:
        return [name for name in names if name.startswith(prefix)]

    @classmethod
    def filter_names_by_header(cls, names: list[str], header: Header) -> list[str]:
        """This method filters the input list of names by checking if they start with the name of the given header.

        Args:
            names: A list of strings representing the names to be filtered.
            header: An instance of the Header class, used to filter the input list of names.

        Returns:
            A list of filtered names that start with the given header name.
        """
        return cls._filter_by_prefix(names, header.name)


@dataclass(frozen=True)
class EOSHeaders(metaclass=MetaHeaders):
    """Collection of EOS specific headers."""

    CHAR_NAME = Header("char_name", Units.STRING, alt_name="name")
    EOS_TYPE = Header("eos_type", Units.STRING, ecl_name="eos", alt_name="type")
    COMPONENT_NAMES = Header("cname", Units.STRING, ecl_name="cnames", alt_name="component_names")
    MOLECULAR_WEIGHTS = Header("mw", Units.REAL, alt_name="molecular_weights")
    UPPER_MOLECULAR_WEIGHTS = Header("mwu", Units.KILOGRAM_MOLE, alt_name="upper_molecular_weights")
    CRITICAL_TEMPERATURES = Header("tc", Units.KELVIN, ecl_name="tcrit", alt_name="critical_temperatures")
    CRITICAL_PRESSURES = Header("pc", Units.BAR, ecl_name="pcrit", alt_name="critical_pressures")
    CRITICAL_VOLUMES = Header("vc", Units.CUBIC_METER_PER_KILOGRAM_MOLE, ecl_name="vcrit")
    ACENTRIC_FACTORS = Header("af", Units.REAL, ecl_name="acf", alt_name="acentric_factors")
    VOLUME_SHIFTS = Header("vs", Units.REAL, ecl_name="sshift", alt_name="volume_shifts")
    SURFACE_VOLUME_SHIFT_PARAMETERS = Header("svs", Units.REAL, ecl_name="sshifts", alt_name="surface_volume_shifts")
    OMEGA_A = Header("omegaa", Units.REAL, alt_name="omega_a")
    OMEGA_B = Header("omegab", Units.REAL, alt_name="omega_b")
    PENELOUX_VOLUME_CORRECTION = Header("cpen_ref", Units.REAL, alt_name="volume_corrections")
    PENELOUX_TEMPERATURE_GRADIENT = Header("cpen_t", Units.REAL, alt_name="temperature_gradient")
    GROSS_HEATING_VALUES = Header("hw", Units.MEGAJOULE_PER_CUBIC_METER, alt_name="component_heating_values")
    LIQUID_DENSITIES = Header("lden", Units.REAL, alt_name="liquid_densities")
    PARACHORS = Header("parachor", Units.REAL, alt_name="parachors")
    CRITICAL_VOLUME_CORRELATIONS = Header("vcvis", Units.CUBIC_METER_PER_KILOGRAM_MOLE, alt_name="critical_volumes")
    BINARY_INTERACTION_PARAMETERS = Header("bip", Units.REAL, ecl_name="bic", alt_name="binary_interaction_parameters")
    LBC_COEFFICIENTS = Header("lbc_coefficients", Units.REAL, ecl_name="lbccoef", alt_name="lbc")
    CSP_COEFFICIENTS = Header("csp_coefficients", Units.REAL, ecl_name="pedtune", alt_name="csp")
    RESERVOIR_VOLUME_SHIFT_TEMP = Header(
        "temperature_for_reservoir_volume_shift", Units.KELVIN, ecl_name="tref", alt_name="rtemp"
    )
    BOILING_TEMPERATURES = Header("boiling_temperatures", Units.KELVIN, ecl_name="tboil")
    SPECIFIC_GRAVITIES = Header("specific_gravity", Units.REAL, alt_name="relative_density")
    CARBON_NUMBERS = Header("carbon_number", Units.REAL, alt_name="carbon_numbers")
    BOILING_POINT_LOWER = Header("boiling_point_low", Units.KELVIN)
    BOILING_POINT_UPPER = Header("boiling_point_up", Units.KELVIN)
    LIQUID_YIELD = Header("liquid_yield", unit="m3_km3")
    CRITICAL_Z_FACTORS = Header("critical_z_factors", unit=Units.REAL, ecl_name="zcrit", alt_name="zc")


@dataclass(frozen=True)
class PVTHeaders(metaclass=MetaHeaders):
    """Collection of PVT specific headers."""

    # PVTNUM = Headers.PVTNUM
    PVTNUM = Header("pvt_number", Units.INTEGER, magic_name="pvtnum")
    PRESSURE = Header("pressure", Units.BAR, magic_name="pres")
    TEMPERATURE = Header("temperature", Units.CELSIUS, magic_name="temp")
    SATURATION_PRESSURE = Header("saturation_pressure", Units.BAR, magic_name="psat")
    DENSITY = Header("density", Units.KILOGRAM_PER_CUBIC_METER, magic_name="den")
    OIL_DENSITY = Headers.OIL_DENSITY
    GAS_DENSITY = Headers.GAS_DENSITY
    RELATIVE_TOTAL_VOLUME = Header("relative_total_volume", Units.CUBIC_METER, magic_name="vrt")
    RELATIVE_OIL_VOLUME = Header("relative_oil_volume", Units.REAL, magic_name="vro")
    LIQUID_VOLUME = Header("liquid_volume", Units.REAL, magic_name="liq-vol")
    TOTAL_GAS_OIL_RATIO = Header(
        "total_gas_oil_ratio", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="tot-gor"
    )
    GAS_OIL_RATIO = Header("gas_oil_ratio", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="gor")
    SOLUTION_GAS_OIL_RATIO_DLE = Header(
        "solution_gas_oil_ratio_dle", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="rsd"
    )
    OIL_FORMATION_VOLUME_FACTOR = Header(
        "oil_formation_volume_factor", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="bo"
    )
    GAS_SPECIFIC_GRAVITY = Header("gas_specific_gravity", Units.REAL, magic_name="sg")
    COMPRESSIBILITY = Header("compressibility", Units.BAR_INVERSE, magic_name="compr")
    Y_FACTOR = Header("y_factor", Units.REAL, magic_name="y-fac")
    Z_FACTOR = Header("z-factor", Units.REAL, magic_name="z-fac")
    MOLES_GAS_PRODUCED = Header("moles_gas_produced", Units.REAL, magic_name="np")
    TWO_PHASE_Z_FACTOR = Header("two_phase_z_factor", Units.REAL, magic_name="z-fac2")
    OIL_VISCOSITY = Header("oil_viscosity", Units.CENTIPOISE, magic_name="viso")
    GAS_VISCOSITY = Header("gas_viscosity", Units.CENTIPOISE, magic_name="visg")
    OIL_FORMATION_VOLUME_FACTOR_DLE = Header(
        "oil_formation_volume_factor_dle", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="bod"
    )
    GAS_FORMATION_VOLUME_FACTOR = Header(
        "gas_formation_volume_factor", Units.CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="bg"
    )
    EQUILIBRIUM_OIL_COMP = Header("equilibrium_oil_composition", Units.MOLE_FRACTION, magic_name="eq-oil")
    EQUILIBRIUM_GAS_COMP = Header("equilibrium_gas_composition", Units.MOLE_FRACTION, magic_name="eq-gas")
    GAS_MOLE_FRACTION = Header("gas_mole_fraction", Units.REAL, magic_name="ng")
    EXPERIMENT = Header("experiment", Units.STRING, magic_name="na")
    GAS_TEMPERATURE = Header("gas_temperature", Units.CELSIUS, magic_name="na")
    GAS_EXPERIMENT = Header("gas_experiment", Units.STRING, magic_name="na")
    INJECTION_GAS = Headers.INJECTION_GAS
    PHASE = Header("phase", "na", magic_name="na")
    SOLUTION_GAS_OIL_RATIO = Header(
        "solution_gas_oil_ratio", Units.STANDARD_CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="rs"
    )
    SOLUTION_OIL_GAS_RATIO = Header(
        "solution_oil_gas_ratio", Units.STANDARD_CUBIC_METER_PER_STANDARD_CUBIC_METER, magic_name="rv"
    )
    FLUID_TYPE = Header("fluid_type", Units.STRING, magic_name="fluid-type")
    SATURATION_TYPE = Header("saturation_type", Units.STRING, magic_name="sat_type")


MOLES_TO_VOLUME_HEADERS_WITH_RES = [
    Headers.OIL_VOLUME_ORIGINATING_RESERVOIR_OIL.full,
    Headers.OIL_VOLUME_ORIGINATING_RESERVOIR_GAS.full,
    Headers.NGL_VOLUME_ORIGINATING_RESERVOIR_OIL.full,
    Headers.NGL_VOLUME_ORIGINATING_RESERVOIR_GAS.full,
    Headers.GAS_VOLUME_ORIGINATING_RESERVOIR_OIL.full,
    Headers.GAS_VOLUME_ORIGINATING_RESERVOIR_GAS.full,
]

MOLES_TO_VOLUME_HEADERS = [
    Headers.TOTAL_VOLUME.name,
    Headers.TOTAL_MASS.name,
    Headers.TOTAL_MOLES.name,
    Headers.TOTAL_MOLAR_COMPOSITION.name,
    Headers.TOTAL_MASS_COMPOSITION.name,
    Headers.TOTAL_MOLAR_STREAM.name,
    Headers.TOTAL_MOLECULAR_WEIGHT.name,
    Headers.OIL_VOLUME.name,
    Headers.OIL_MASS.name,
    Headers.OIL_DENSITY.name,
    Headers.OIL_MOLECULAR_WEIGHT.name,
    Headers.OIL_MOLES.name,
    Headers.OIL_MOLAR_COMPOSITION.name,
    Headers.OIL_MASS_COMPOSITION.name,
    Headers.OIL_MOLAR_STREAM.name,
    Headers.OIL_MASS_STREAM.name,
    Headers.GAS_VOLUME.name,
    Headers.GAS_MASS.name,
    Headers.GAS_DENSITY.name,
    Headers.GAS_MOLECULAR_WEIGHT.name,
    Headers.GAS_MOLES.name,
    Headers.GAS_HEAT.name,
    Headers.GAS_GRAVITY.name,
    Headers.GAS_MOLAR_COMPOSITION.name,
    Headers.GAS_MASS_COMPOSITION.name,
    Headers.GAS_MOLAR_STREAM.name,
    Headers.GAS_MASS_STREAM.name,
    Headers.NGL_MASS_STREAM.name,
    Headers.NGL_VOLUME.name,
    Headers.NGL_MASS.name,
    Headers.NGL_DENSITY.name,
    Headers.NGL_MOLECULAR_WEIGHT.name,
    Headers.NGL_MOLES.name,
    Headers.NGL_MOLAR_COMPOSITION.name,
    Headers.VAPOR_PRESSURE.name,
]
