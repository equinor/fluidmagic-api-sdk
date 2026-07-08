import json

from examples.shared_data import eos_model, fluid_model, process_model, rate_to_moles_input
from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.config_models import FluidFilterType, RateToMolesCreateModel

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Running a Rate to Moles Conversion ----
# This example demonstrates how to upload models, create a config, and run a rate to moles conversion.
# (EOS, Process, Fluid models, and input data are imported from shared_data.py)

# Upload models, create config, and run conversion
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:
    facility = client.get_facility("dum")  # Get the dummy facility

    # Create EOS
    eos = facility.eos.create(eos_model)
    print(f"Created EOS with ID: {eos.id}")

    # Create Process
    process = facility.processes.create(process_model)
    print(f"Created Process with ID: {process.id}")

    # Create Fluid
    fluid = facility.fluids.create(fluid_model)
    print(f"Created Fluid with ID: {fluid.id}")

    # Create Config
    config_model = RateToMolesCreateModel(
        name="My Config",
        description="My Config Description",
        eos_id=eos.id,
        process_id=process.id,
        fluid_id=fluid.id,
    )

    config = facility.configs.create_rate_to_moles(config_model)
    print(f"Created Config with ID: {config.id}")

    # Run Rate to Moles Conversion
    result = config.run_rate_to_moles(input=rate_to_moles_input, output=FluidFilterType.ALL)
    print("Rate to Moles Conversion Result:")
    print(json.dumps(result.model_dump(), indent=2))

    # Cleanup
    facility.configs.delete(config.id)
    facility.eos.delete(eos.id)
    facility.processes.delete(process.id)
    facility.fluids.delete(fluid.id)
    print("Cleanup completed")
