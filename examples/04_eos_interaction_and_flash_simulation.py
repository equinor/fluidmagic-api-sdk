from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.resources.eos import EOSCreateModel

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- EOS Interaction and Flash Simulation ----
# This example demonstrates EOS interaction and flash simulation capabilities.

# List available EOSs
print("=== Listing available EOSs ===")
with Client.using_client_credentials(client_id=client_id, client_secret=client_secret) as client:
    facility = client.get_facility("dum")  # Get the dummy facility
    eoses = facility.eos.list()  # List the EOSs in the dummy facility
    print(eoses)

# Create EOS and run a Flash Simulation
print("\n=== Creating EOS and running Flash Simulation ===")
input_data = EOSCreateModel(
    name="New EOS",
    description="A new EOS model",
    eos_data=EOSData(
        eos_type="srk",
        component_names=["c1", "c2", "c3-c4"],
        molecular_weights=[16.04, 30.07, 58.12],
        upper_molecular_weights=[16.04, 30.07, 58.12],
        critical_temperatures=[190.6, 305.3, 425.2],
        critical_pressures=[45.99, 48.72, 37.96],
        acentric_factors=[0.008, 0.098, 0.193],
        binary_interaction_parameters=[[0.0, 0.1, 0.2], [0.1, 0.0, 0.3], [0.2, 0.3, 0.0]],
        volume_shifts=[0.0, 0.0, 0.0],
    ),
)

with Client.using_client_credentials(client_id=client_id, client_secret=client_secret) as client:
    facility = client.get_facility("dum")  # Get the dummy facility

    # Create EOS
    new_eos = facility.eos.create(input_data)
    print(f"Created EOS with ID: {new_eos.id}")

    # Get new EOS by ID
    retrieved_eos = facility.eos.get(new_eos.id)
    print(f"Retrieved EOS: {retrieved_eos.name}")

    # Run Flash Simulation
    flash_result = retrieved_eos.simulate_flash(
        molar_composition=[0.5, 0.3, 0.2],
        temperature_conditions=[50.0, 30.0],
        pressure_conditions=[100, 120],
    )
    print("Flash Simulation Result:")
    print(flash_result)

    # Delete EOS by ID
    facility.eos.delete(new_eos.id)
    print(f"Deleted EOS with ID: {new_eos.id}")
