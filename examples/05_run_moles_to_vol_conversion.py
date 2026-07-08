from shared_data import eos_model, moles_to_vol_input, moles_to_vol_output, process_model

from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.resources.config import MolesToVolCreateModel

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- Running a Moles to Volume Conversion ----
# This example demonstrates how to upload models, create a config, and run a conversion.
# (EOS, Process models, and input/output data are imported from shared_data.py)

# Upload models, create config, and run conversion
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:
    facility = client.get_facility("dum")  # Get the dummy facility

    # Create EOS
    eos = facility.eos.create(eos_model)
    print(f"Created EOS with ID: {eos.id}")

    # Create Process
    process = facility.processes.create(process_model)
    print(f"Created Process with ID: {process.id}")

    # Create Config
    config_model = MolesToVolCreateModel(
        name="My Config",
        description="My Config Description",
        eos_id=eos.id,
        process_id=process.id,
    )

    config = facility.configs.create_moles_to_vol(config_model)
    print(f"Created Config with ID: {config.id}")

    # Run Moles to Volume Conversion
    result = config.run_moles_to_vol(input=moles_to_vol_input, output=moles_to_vol_output)
    print("Moles to Volume Conversion Result:")
    print(result)

    # Cleanup
    facility.configs.delete(config.id)
    facility.eos.delete(eos.id)
    facility.processes.delete(process.id)
    print("Cleanup completed")
