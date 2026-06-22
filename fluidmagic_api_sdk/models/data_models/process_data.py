"""File for process related pydantic data classes."""

from typing import Self

from pydantic import BaseModel, model_validator

from ..enums import ComponentProcessFactorType, TankType
from .eos_data import EOSData


class ProcessFactorData(BaseModel):
    """Pydantic model for data transfer, validation and serialization across boundaries.

    Attributes:
        name: Component process factor name.
        table_type: Component process factor table type (rec or kval - table).
        table: Table data as list of list.
        plus_index: Index in component list where the heavy plus fraction starts.
        reference_eos: Reference EOS model data.
    """

    name: str
    table_type: ComponentProcessFactorType
    table: list[list[float]]
    plus_index: int
    reference_eos: EOSData | None = None

    def get_implicit_component_count(self) -> int:
        """Get the implicit component count.

        Returns:
            Implicit component count.
        """
        return len(self.table[0]) - 1

    # TODO(#2079): This is dupe code from process
    @model_validator(mode="after")
    def model_validation(self) -> Self:
        """Validates the values of the table.

        Raises:
            ProcessException: If the rows have differing number of values.
            ProcessException: If the plus fraction is not increasing.
            ProcessException: If the plus fraction is not between 0 and 1.
        """
        plus_fraction = 0.0
        column_count = len(self.table[0])

        for i, table in enumerate(self.table):
            if len(table) != column_count:
                raise ValueError("KVAL or REC table must have equal number of components.")
            if table[0] < plus_fraction:
                raise ValueError("Plus fraction in KVAL or REC table must be increasing.")
            elif table[0] > 1.0:
                raise ValueError("Plus fraction in KVAL or REC table must be between 0 and 1.")
            else:
                plus_fraction = table[0]
        return self


class TankData(BaseModel):
    """Pydantic model for data transfer, validation and serialization across boundaries.

    Attributes:
        name: Tank name.
        tank_type: Tank type ( oil gas, flash, etc.).
        pressure: Tank pressure.
        temperature: Tank temperature.
        volume_splits: Volume splits for tank_type volume.
        oil_destination: Tank oil destination.
        gas_destination: Tank gas destination.
        process_factor: ProcessFactorData object.
    """

    name: str
    tank_type: TankType
    pressure: float
    temperature: float
    volume_splits: list[float] | None = None
    oil_destination: str | None = None
    gas_destination: str | None = None
    process_factor: ProcessFactorData | None = None

    def get_implicit_component_count(self) -> int | None:
        """Get the implicit component count.

        Returns:
            Implicit component count.
        """
        if self.process_factor is None:
            return None
        return self.process_factor.get_implicit_component_count()


class ProcessData(BaseModel):
    """Pydantic model for data transfer, validation and serialization across boundaries.

    Attributes:
        name: Process name.
        tanks: List of TankData objects.
    """

    name: str
    tanks: list[TankData]

    def get_implicit_component_count(self) -> int | None:
        """Get the implicit component count.

        Returns:
            Implicit component count. -1 if there is count constraint.
        """
        counts = [tank.get_implicit_component_count() for tank in self.tanks]
        counts = [count for count in counts if count is not None]
        if not counts:
            return -1

        return counts[0]
