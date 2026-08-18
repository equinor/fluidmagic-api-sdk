import json

from examples.data.conversion_data import (
    characterization_input,
    eos_data,
    fluid,
    moles_to_vol_input,
    output_filter,
    process_data,
    rate_to_moles_input,
)
from fluidmagic_api_sdk.client.sync_client import Client
from fluidmagic_api_sdk.models.config_models import FluidFilterType

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Running Inline Conversions ----
# This example demonstrates how to run conversions inline without requiring pre-uploaded resources.
# This is useful for quick conversions or testing that don't need to be saved or shared.
# (All data definitions are imported from data/conversion_data.py)

# Run inline conversions
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:
    # Run Rate to Moles Conversion
    rate_to_moles_result = client.conversions.run_rate_to_moles(
        eos=eos_data,
        fluid=fluid,
        process=process_data,
        input=rate_to_moles_input,
        output=FluidFilterType.ALL,
    )
    print("Rate to Moles Conversion Result:")
    print(json.dumps(rate_to_moles_result.model_dump(), indent=2))

    # Run Moles to Volume Conversion
    moles_to_vol_result = client.conversions.run_moles_to_volume(
        eos=eos_data,
        process=process_data,
        input=moles_to_vol_input,
        output=output_filter,
    )
    print("\nMoles to Volume Conversion Result:")
    print(json.dumps(moles_to_vol_result.model_dump(), indent=2))

    # Run Characterization Conversion
    characterization_result = client.conversions.run_characterize_fluid_to_eos(
        eos=eos_data,
        input_data=characterization_input,
    )
    print("\nCharacterization Conversion Result:")
    print(json.dumps(characterization_result.model_dump(), indent=2))
