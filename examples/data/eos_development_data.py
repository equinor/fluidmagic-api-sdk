from examples.data.simulations_data import (
    eos_data,
    flash_measured,
    flash_pressures,
    flash_temperatures,
    oil_feed,
    psat_measured,
    psat_temperature,
)
from fluidmagic_api_sdk.models.eos_models import DefaultEOSCreateModel, EOSTuneModel

default_eos_input = DefaultEOSCreateModel(
    eos_name="default_srk",
    eos_type="SRK",
    plus_fraction_molecular_weight=220.0,
    plus_fraction_density=850.0,
)

tune_eos_input = EOSTuneModel(
    eos_data=eos_data,
    method_preset="mix_1",
    simulations=[
        {
            "name": "psat",
            "parameters": {
                "molar_composition": oil_feed,
                "temperature": psat_temperature,
                "measured": psat_measured.model_dump(),
                "weights": {"saturation_pressure": 1.0},
            },
        },
        {
            "name": "flash",
            "parameters": {
                "molar_composition": oil_feed,
                "pressures": flash_pressures,
                "temperatures": flash_temperatures,
                "measured": flash_measured.model_dump(),
                "weights": {"gas_oil_ratio": 1.0, "oil_density": 1.0, "gas_density": 1.0},
            },
        },
    ],
)
