"""File for FrameData class."""

from __future__ import annotations

import re
from typing import Any, ClassVar

import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator

from ...utilities.headers import Headers
from ...utilities.utils import (
    check_required_headers,
    component_sort_key,
    extract_component_groups,
    validate_headers_and_units,
)


class FrameData(BaseModel):
    """Pydantic model for data transfer, validation and serialization across boundaries.

    Attributes:
        headers: DataFrame headers.
        units: DataFrame units.
        index: DataFrame index (date string, int or None.
        data: DataFrame data.
    """

    headers: list[str] = Field(..., description="Column headers for data, e.g. (date, id, C1).")
    units: list[str] = Field(..., description="Column header unist, for data, e.g. (string, int, m3, kgmol).")
    index: list[str | int] | None = Field(..., description="Row index for data, e.g. ('01.01.2021', 1).")
    data: list[list[Any]] = Field(..., description="Data matrix.")

    @field_validator("headers")
    @classmethod
    def validate_header_format(cls, headers):
        """Validate header format for security (length and character set)."""
        if not headers:
            return headers

        pattern = re.compile(r"^[a-zA-Z0-9_-]+$")
        max_length = 100

        invalid_headers = []
        for idx, header in enumerate(headers):
            if len(header) > max_length:
                invalid_headers.append(f"Header at position {idx} exceeds maximum length of {max_length}: '{header}'")

            if not pattern.match(header):
                invalid_headers.append(
                    f"Header at position {idx} contains invalid characters: '{header}' "
                    + "(only alphanumeric, underscore, hyphen allowed)"
                )

        if invalid_headers:
            raise ValueError(", ".join(invalid_headers))

        return headers

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> FrameData:
        """Construct FrameData from pandas dataframe.

        Args:
            df: Pandas dataframe to generate FrameData from.

        Returns:
            FrameData object.
        """
        if isinstance(df.index[0], pd.Timestamp):
            index = [str(i) for i in df.index.tolist()]
        else:
            index = [int(i) for i in df.index.tolist()]

        exclude_types = ["datetime", "timedelta"]
        if df.select_dtypes(exclude_types).columns.tolist():
            df = df.select_dtypes(exclude=exclude_types)

        headers, units = list(zip(*df.columns.tolist()))
        data = df.to_numpy().tolist()

        return cls(
            headers=[str(header) for header in headers],
            units=[str(unit) for unit in units],
            index=index,
            data=data,
        )

    def to_dataframe(self) -> pd.DataFrame:
        """Convert self to pandas dataframe.

        Returns:
            Dataframe based on index columns and data from self.
        """
        if self.index is None:
            index = self.index
        elif isinstance(self.index[0], str):
            index = [pd.Timestamp(i) for i in self.index]
        else:
            index = [int(i) for i in self.index]
        return pd.DataFrame(self.data, index, pd.MultiIndex.from_tuples(zip(self.headers, self.units)))

    def get_fluid_names(self) -> list[str]:
        """Get a list of unique fluid names from the data."""
        headers = self.headers
        data = self.data
        identifiers = [header.name for header in Headers if header.is_identifier]
        found_identifiers = [id_name for id_name in identifiers if id_name in headers]

        if found_identifiers:
            # Use the first found identifier
            identifier = found_identifiers[0]
            identifier_index = headers.index(identifier)

            if "date" in headers and headers.index("date") < identifier_index:
                identifier_index -= 1

            fluid_names = {
                row[identifier_index]
                for row in data
                if row and len(row) > identifier_index and row[identifier_index] is not None
            }
        else:
            fluid_names = []

        return sorted(list(fluid_names))

    def get_component_names(self, preferred_prefix: str = "molarstream") -> list[str]:
        """
        Retrieve a sorted list of component names based on the specified prefix.

        Args:
            preferred_prefix: The prefix of the component group to retrieve. Defaults to "molarstream".

        Returns:
            A sorted list of component names corresponding to the specified prefix.

        Raises:
            ValueError: If the specified prefix is invalid.
        """
        component_groups = extract_component_groups(self.headers, sort_key=component_sort_key)

        if preferred_prefix in component_groups:
            return component_groups[preferred_prefix]
        else:
            raise ValueError(
                f"Invalid prefix '{preferred_prefix}' specified. Available prefixes: {list(component_groups.keys())}"
            )

    def get_component_count(self) -> int:
        """Get the number of components in the fluid model."""
        return len(self.get_component_names())


class FluidLibFrameData(FrameData):
    """Fluid library data model with specific header requirements.

    ## Required Headers
    - `fluid_id`: Unique identifier for the fluid
      - Unit: `string`
    - `experiment-type`: Type of experiment data
      - Unit: `string`
    - `reservoir_temperature`: Temperature of the reservoir
      - Unit: `c`
    - `molarstream*`: Molar stream properties (any header starting with 'molarstream')
      - Unit: `kgmol/d`

    ## Optional Headers
    - `injection_gas*`: Injection gas properties (any header starting with 'injection_gas')
      - Unit: `kgmol/d`
    - `lift_gas*`: Lift gas properties (**REQUIRED** for rate to mol conversions)
      - Unit: `kgmol/d`
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "headers": [
                        "fluid_id",
                        "experiment-type",
                        "reservoir_temperature",
                        "molarstream_c1",
                        "molarstream_c2",
                    ],
                    "units": ["string", "string", "c", "kgmol/d", "kgmol/d"],
                    "index": [],
                    "data": [["fluid1", "cme", 90, 0.3, 42], ["fluid1", "cme", 90, 0.4, 43]],
                }
            ]
        }
    }
    REQUIRED_HEADERS: ClassVar[list] = [
        Headers.FLUID_ID,
        Headers.RESERVOIR_TEMPERATURE,
        Headers.EXPERIMENT_TYPE,
        Headers.MOLES,
    ]
    OPTIONAL_HEADERS: ClassVar[list] = [Headers.INJECTION_GAS, Headers.LIFT_GAS]

    @model_validator(mode="after")
    def validate_fluid_lib_headers(self):
        """Validate required headers."""
        check_required_headers(self.headers, self.REQUIRED_HEADERS)
        validate_headers_and_units(self.headers, self.units)

        return self

    def has_lift_gas(self) -> bool:
        """Check if lift gas headers are present."""
        return any(header.startswith(Headers.LIFT_GAS.name) for header in self.headers)


class RateToMolFrameData(FrameData):
    """Rate to mol input data model with specific header requirements.

    ## Required Headers
    - `fluid_id`: Unique identifier for the fluid
      - Unit: `string`
    - `sep_temp`: Separator temperature (Required when process model not used)
      - Unit: `c`
    - `sep_pres`: Separator pressure (Required when process model not used)
      - Unit: `bar`
    - `oil_vol`: Oil volume
      - Unit: `sm3/d`
    - `gas_vol`: Gas volume
      - Unit: `sm3/d`

    ## Optional Headers
    - `res_pres`: Reservoir pressure
      - Unit: `bar`
    - `oil_density`: Oil density
      - Unit: `kg/m3`
    - `gas_density`: Gas density
      - Unit: `kg/m3`
    - `liftgas_vol`: Lift gas volume
      - Unit: `sm3/d`
    - `netgas_vol`: Net gas volume
      - Unit: `sm3/d`
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "headers": ["fluid_id", "oil_vol", "gas_vol", "liftgas_vol", "netgas_vol"],
                    "units": ["string", "sm3/d", "sm3/d", "sm3/d", "sm3/d"],
                    "index": ["2021-01-11 00:00:00", "2021-02-11 00:00:00"],
                    "data": [["fluid1", 15, 1.01, 100, 50, 20, 30], ["fluid1", 90, 1.01, 100, 50, 20, 30]],
                }
            ]
        }
    }

    REQUIRED_HEADERS: ClassVar[list] = [Headers.FLUID_ID, Headers.OIL_VOLUME, Headers.GAS_VOLUME]

    OPTIONAL_HEADERS: ClassVar[list] = [
        Headers.RESERVOIR_TEMPERATURE,
        Headers.OIL_DENSITY,
        Headers.GAS_DENSITY,
        Headers.SEPARATOR_TEMPERATURE,
        Headers.SEPARATOR_PRESSURE,
        Headers.LIFT_GAS_VOLUME,
        Headers.NET_GAS_VOLUME,
    ]

    @model_validator(mode="after")
    def validate_separator_headers(self):
        """Validate required headers."""
        check_required_headers(self.headers, self.REQUIRED_HEADERS)
        validate_headers_and_units(self.headers, self.units)
        return self

    def validate_conditional_separator_headers(self):
        """Validate that separator temperature and pressure are provided when needed."""
        check_required_headers(self.headers, [Headers.SEPARATOR_TEMPERATURE, Headers.SEPARATOR_PRESSURE])

        return self


class MolToVolFrameData(FrameData):
    """Model for mole-to-volume input data.

    ## Headers
    - `molarstream*`: Molar stream properties (any header starting with 'molarstream_')
      - Unit: `kgmol/d`
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "headers": ["molarstream_c1", "molarstream_c2", "molarstream_c3"],
                    "units": ["kgmol/d", "kgmol/d", "kgmol/d"],
                    "index": [],
                    "data": [[0.6, 0.3, 0.1]],
                }
            ]
        }
    }
    REQUIRED_HEADERS: ClassVar[list] = [Headers.MOLES]

    @model_validator(mode="after")
    def validate_moles_headers(self):
        """Validate that headers start with 'molarstream_'."""
        check_required_headers(self.headers, self.REQUIRED_HEADERS)
        validate_headers_and_units(self.headers, self.units)
        return self
