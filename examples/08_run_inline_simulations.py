import json

from examples.inline_data import flash_eos_data
from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.simulate_models import FlashMeasuredModel, FlashWeightsModel

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- Running Inline Simulations ----
# This example demonstrates running simulations inline without having to upload resources and create configurations.
# This is useful for quick simulations or testing that don't need to be saved or shared.

# Define Data
molar_composition = [0.5, 0.3, 0.2]  # Mole fractions of components
temperatures = [30.0, 50.0]  # in Kelvin
pressures = [100, 120]  # in bara

flash_measured = FlashMeasuredModel(
    gas_oil_ratio=[84.6, 707.6],
    gas_density=[84.6, 44.1],
    oil_density=[707.6, 766.5],
)

flash_weights = FlashWeightsModel(
    gas_oil_ratio=0.5,
    gas_density=0.8,
    oil_density=1,
)

# Run Inline Flash Simulation
print("=== Running Inline Flash Simulation ===")
with Client.using_client_credentials(client_id, client_secret) as client:

    # Run Flash Simulation
    print("Running Flash Simulation...")
    flash_result = client.simulations.run_flash(
        eos=flash_eos_data,
        molar_composition=molar_composition,
        temperatures=temperatures,
        pressures=pressures,
        measured=flash_measured,
        weights=flash_weights,
    )
    print("Flash Simulation Result:")
    print(json.dumps(flash_result.model_dump(), indent=2))
