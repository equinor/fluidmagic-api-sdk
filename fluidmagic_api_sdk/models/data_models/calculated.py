from pydantic import BaseModel, Field


class FlashCalculated(BaseModel):
    """Class for flash calculation results."""

    gas_mole_fraction: list[float] = Field(..., description="Gas mole fraction.")
    equilibrium_gas_comp: list[list[float]] = Field(..., description="Equilibrium gas composition.")
    equilibrium_oil_comp: list[list[float]] = Field(..., description="Equilibrium oil composition.")
    oil_density: list[float] = Field(..., description="Oil density.")
    gas_density: list[float] = Field(..., description="Gas density.")
    gas_oil_ratio: list[float] = Field(..., description="Gas-to-Oil ratio.")

    def __init__(
        self,
        gas_mole_fraction: list[float],
        equilibrium_gas_comp: list[list[float]],
        equilibrium_oil_comp: list[list[float]],
        oil_density: list[float],
        gas_density: list[float],
        gas_oil_ratio: list[float],
        **kwargs,
    ):
        super().__init__(
            gas_mole_fraction=gas_mole_fraction,
            equilibrium_gas_comp=equilibrium_gas_comp,
            equilibrium_oil_comp=equilibrium_oil_comp,
            oil_density=oil_density,
            gas_density=gas_density,
            gas_oil_ratio=gas_oil_ratio,
            **kwargs,
        )
