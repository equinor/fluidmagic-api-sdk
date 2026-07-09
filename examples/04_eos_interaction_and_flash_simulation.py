import json

from examples.shared_data import flash_eos_model
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- EOS Interaction and Flash Simulation ----
# This example demonstrates EOS interaction and flash simulation capabilities.

# List available EOSs
print("=== Listing available EOSs ===")
with Client.using_client_credentials(client_id=client_id, client_secret=client_secret) as client:
    facility = client.get_facility("dum")  # Get the dummy facility
    eoses = facility.eos.list()  # List the EOSs in the dummy facility
    print(f"Found {len(eoses)} EOSs in the dummy facility:")
    print(json.dumps([eos.model_dump() for eos in eoses], indent=2))

# Create EOS and run a Flash Simulation
print("\n=== Creating EOS and running Flash Simulation ===")

with Client.using_client_credentials(client_id=client_id, client_secret=client_secret) as client:
    facility = client.get_facility("dum")  # Get the dummy facility

    # Create EOS
    new_eos = facility.eos.create(flash_eos_model)
    print(f"Created EOS with ID: {new_eos.id}")

    # Get new EOS by ID
    retrieved_eos = facility.eos.get(new_eos.id)

    # Run Flash Simulation
    flash_result = retrieved_eos.simulate_flash(
        molar_composition=[0.5, 0.3, 0.2],
        temperature_conditions=[30.0, 50.0],
        pressure_conditions=[100, 120],
    )
    print("Flash Simulation Result:")
    print(json.dumps(flash_result.model_dump(), indent=2))

    # Delete EOS by ID
    facility.eos.delete(new_eos.id)
    print(f"Deleted EOS with ID: {new_eos.id}")
