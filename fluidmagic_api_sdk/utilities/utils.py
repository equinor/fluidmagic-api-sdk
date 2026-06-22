import re
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np
import numpy.typing as npt

from .headers import Header, Headers, Units

LIBRARY_COMPONENT_NAMES = [
    "n2",
    "co2",
    "h2s",
    "c1",
    "c2",
    "c3",
    "ic4",
    "c4",
    "ic5",
    "neo-c5",
    "c5",
    "c6",
    "nC7",
    "nC8",
    "nC9",
    "nC10",
]
# Matches for library components at the end of a string as long as they are not preceded by a number or letter.
LIBRARY_COMPONENT_PATTERN = rf"(?<![a-zA-Z0-9])({'|'.join(map(re.escape, LIBRARY_COMPONENT_NAMES))})$"

# Matches for heavy components at the end of a string as long as they are not preceded by a number or letter
# or another heavy component followed by a dash. This is to prevent picking up lumped components.
SINGLE_HEAVY_COMPONENT_PATTERN = r"(?<![a-zA-Z0-9])(?<!(c([0-9])-))(?<!(c\d{2}-))c(?:[7-9]|\d{2})$"

# Matches for lumped heavy components at then end of a string as long as they are not preceded by a number or letter.
LUMPED_HEAVY_COMPONENT_PATTERN = r"(?<![a-zA-Z0-9])(c([7-9]|\d{2})-c([8-9]|\d{2}))$"
# Matches for normal components, including optional ranges, at the end of a string prefixed with "n".
NORMAL_COMPONENT_PATTERN = r"(?<![a-zA-Z0-9])nc\d+(?:-c\d+)?$"
# Matches for any component name at the end of a string.
ALL_COMPONENTS_PATTERN = (
    rf"{LUMPED_HEAVY_COMPONENT_PATTERN}|"
    rf"{SINGLE_HEAVY_COMPONENT_PATTERN}|"
    rf"{LIBRARY_COMPONENT_PATTERN}|"
    rf"{NORMAL_COMPONENT_PATTERN}"
)


def get_current_utc_time():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def cast_to_np_array(data: list[float | list[float] | str] | None) -> npt.NDArray[np.float64 | np.str_] | None:
    """Cast data to a Numpy array if it is not None."""
    return np.array(data) if data is not None else None


def component_sort_key(s: str) -> float:
    """Provide sorting key for sorting component strings."""
    if s == "n2":
        return -2
    if s == "co2":
        return -1
    if s == "h2s":
        return 0
    # Else sort by trailing digits.
    match = re.search(r"(\d+)$", s)
    key = float(match.group(1)) if match else float("inf")
    # Add offset for isotopes and neo components.
    if s.startswith("i"):
        key -= 0.3
    elif s.startswith("neo"):
        key -= 0.1
    elif s.startswith("n"):
        key -= 0.2
    return key


def match_component_name(name: str) -> str | None:
    """Check if a name matches the pattern for a component name.

    This should be true if the name ends with a component name (e.g. n2, c1, ic5, c12),
    or if it ends with a lumped component name (e.g. c6-c8, c9-c12)

    Args:
        name: The name to check.

    Returns:
        The matched component name, or None if no match was found.
    """

    component_pattern = re.compile(ALL_COMPONENTS_PATTERN)
    search = component_pattern.search(name)
    if not search:
        return None
    else:
        return search.group(0)


def extract_component_groups(headers: list[str], sort_key: callable = lambda x: x) -> defaultdict[str, list[str]]:
    """Extract and group component names from headers by prefix, with sorting.

    Args:
        headers: A list of header strings.
        sort_key: A callable used to sort the component names. Defaults to the identity function.

    Returns:
        A defaultdict where keys are prefixes, and values are sorted lists of component names.
    """
    component_groups = defaultdict(list)

    for header in headers:
        prefix = header.split("_")[0]
        component = match_component_name(header)
        if component and component not in component_groups[prefix]:
            component_groups[prefix].append(component)

    # Sort the components within each group using the specified sort key
    for prefix in component_groups:
        component_groups[prefix].sort(key=sort_key)

    return component_groups


def check_required_headers(headers: list[Header] | list[str], required_names: list[str] | list[Header]) -> None:
    """Check that specified header names exist in the provided headers list.

    Args:
        headers: List of header names to validate.
        required_names: List of required header names.

    Raises:
        ValueError: If some required headers are not found.
    """
    normalized_headers = [(header.name if isinstance(header, Header) else header).lower() for header in headers]

    normalized_required_names = [(name.name if isinstance(name, Header) else name).lower() for name in required_names]

    missing_list = []
    for required_name in normalized_required_names:
        found_name = False

        for header in normalized_headers:
            if header.startswith(required_name) or required_name.startswith(header):
                found_name = True
                break

        if not found_name:
            missing_list.append(required_name)

    if missing_list:
        raise ValueError(f"Error: required header(s) [{', '.join(missing_list)}] were not found.")


def validate_headers_and_units(headers: list[str], units: list[str]) -> None:
    """Validate headers and units, collecting errors and warnings.

    Args:
        headers: List of headers.
        units: List of units.

    Raises:
        ValueError: If units are unrecognized or if Header.unit does not match the incoming unit.
    Logs:
        Warnings for unrecognized headers.
    """
    valid_header_names = Headers.get_headers_list(get_name=True, include_alt_names=True)
    valid_units = Units.get_units_list()
    validation_errors = {}
    validation_warnings = {}

    for header, unit in zip(headers, units):
        warning_str = ""

        matching_prefixes = [name for name in valid_header_names if header.startswith(name)]

        if not matching_prefixes:
            warning_str += f"Unrecognized header: {header}. "
        elif matching_prefixes:
            valid_header = None
            for prefix in matching_prefixes:
                valid_header = Headers.get_header_by_name(prefix)

            if valid_header and valid_header.unit == unit:
                continue
            # Quick fix. Might need to update Headers class to support multiple units, if this is common.
            if valid_header and valid_header.unit == Units.STANDARD_CUBIC_METER_PER_DAY:
                if unit in [Units.CUBIC_METER_PER_DAY, Units.ACTUAL_CUBIC_METER_PER_DAY]:
                    continue

            if valid_header and valid_header.unit != unit:
                warning_str += f"Header '{header}' has unit '{unit}', expected '{valid_header.unit}'. "
                validation_errors[(header, unit)] = warning_str
                continue

        if unit not in valid_units:
            warning_str += f"Unrecognized unit: {unit}. "
            validation_errors[(header, unit)] = warning_str
            continue

        validation_warnings[(header, unit)] = warning_str

    if validation_warnings:
        # logger.warning(f"Validation warnings: {str(validation_warnings)}")
        pass

    if validation_errors:
        invalid_pairs_str = "; ".join(f"{msg} ({header}, {unit})" for (header, unit), msg in validation_errors.items())
        raise ValueError(f"Invalid unit(s) detected: {invalid_pairs_str}")

    return None
