import json

from shared_data import eos_model, fluid_model, process_model

from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.config_models import RateToMolesCreateModel, RateToMolesRunInput
from fluidmagic_api_sdk.models.data_models.frame_data import RateToMolFrameData

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Running a Rate to Moles Conversion ----
# This example demonstrates how to upload models, create a config, and run a rate to moles conversion.
# (EOS, Process, and Fluid models are imported from shared_data.py)

# Define Input Data
data = RateToMolFrameData(
    headers=[
        "fluid_id",
        "oil_vol",
        "gas_vol",
        "liftgas_vol",
        "netgas_vol",
    ],
    units=[
        "string",
        "sm3/d",
        "sm3/d",
        "sm3/d",
        "sm3/d",
    ],
    index=["2021-01-11 00:00:00"],
    data=[
        [
            "well1",
            100.904,
            100.0,
            50.0,
            100.2,
        ],
    ],
)

input_data = RateToMolesRunInput(input=data, output="total")

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
    result = config.run_rate_to_moles(input_data)
    print("Rate to Moles Conversion Result:")
    print(json.dumps(result.model_dump(), indent=2))

    # Cleanup
    facility.configs.delete(config.id)
    facility.eos.delete(eos.id)
    facility.processes.delete(process.id)
    facility.fluids.delete(fluid.id)
    print("Cleanup completed")
