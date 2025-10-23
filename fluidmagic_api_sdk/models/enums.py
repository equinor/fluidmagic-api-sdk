"""File containing enums."""

from enum import StrEnum, auto
from typing import Self


class NoCasingEnum(StrEnum):
    """Base class enum that ignores casing (changes input to uppercase, NB enum definition must be uppercase)."""

    @classmethod
    def _missing_(cls, value: str) -> Self:
        """Return the Enum member if the value matches the uppercase version of an Enum member value."""
        for member in cls:
            if member.upper() == value.upper():
                return member


class EOSType(NoCasingEnum):
    """Enum for EOS types."""

    PR = auto()
    PR78 = auto()
    SRK = auto()
    DUMMY = auto()


class PhaseType(StrEnum):
    """Fluid phase types."""

    OIL = auto()
    GAS = auto()
    MIX = auto()

    __values__ = [OIL, GAS, MIX]


class TankType(StrEnum):
    """Tank types used in processes."""

    K_VALUE = "kval"
    RECOVERY_FACTOR = "rec"
    FLASH = "flash"
    VOLUME = "volume"
    OIL_TANK = "oiltank"
    GAS_TANK = "gastank"
    NGL_TANK = "ngltank"


class ComponentProcessFactorType(StrEnum):
    """Recovery table types."""

    RECOVERY_FACTOR = "rectable"
    K_VALUE = "kvaltable"
