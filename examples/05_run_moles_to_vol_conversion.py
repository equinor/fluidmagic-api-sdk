from shared_data import eos_model, process_model

from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.config_models import MolesToVolRunInput
from fluidmagic_api_sdk.resources.config import MolesToVolCreateModel

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- Running a Moles to Volume Conversion ----
# This example demonstrates how to upload models, create a config, and run a conversion.
# (EOS and Process models are imported from shared_data.py)

# Define Input Data
data = MolesToVolRunInput(
    input={
        "headers": [
            "molarstream_n2",
            "molarstream_co2",
            "molarstream_c1",
            "molarstream_c2",
            "molarstream_c3",
            "molarstream_ic4",
            "molarstream_c4",
            "molarstream_ic5",
            "molarstream_c5",
            "molarstream_c6",
            "molarstream_c7",
            "molarstream_c8",
            "molarstream_c9",
            "molarstream_c10-c12",
            "molarstream_c13-c14",
            "molarstream_c15-c17",
            "molarstream_c18-c21",
            "molarstream_c22-c28",
            "molarstream_c29-c36",
            "molarstream_c37-c45",
            "molarstream_c46-c58",
            "molarstream_c59-c80",
        ],
        "index": ["2021-01-11 00:00:00"],
        "units": ["kgmol/d" for _ in range(22)],
        "data": [
            [
                0.005,
                0.02,
                0.25,
                0.15,
                0.10,
                0.05,
                0.05,
                0.03,
                0.03,
                0.02,
                0.02,
                0.02,
                0.02,
                0.04,
                0.05,
                0.06,
                0.07,
                0.05,
                0.03,
                0.01,
                0.005,
                0.005,
            ]
        ],
    },
    output={
        "sep1": ["net_molarstream_*"],
        "oiltank": ["oil_vol", "oil_mass", "oil_moles"],
        "gastank": ["gas_vol", "gas_mass", "gas_moles"],
    },
)

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
    result = config.run_moles_to_vol(data)
    print("Moles to Volume Conversion Result:")
    print(result)

    # Cleanup
    facility.configs.delete(config.id)
    facility.eos.delete(eos.id)
    facility.processes.delete(process.id)
    print("Cleanup completed")
