import json

from examples.data.data import (
    cme_measured,
    cme_pressures,
    cme_temperature,
    cvd_measured,
    cvd_pressures,
    cvd_temperature,
    dle_measured,
    dle_pressures,
    dle_temperature,
    eos_data,
    flash_measured,
    flash_pressures,
    flash_temperatures,
    oil_feed,
    process_data,
    psat_measured,
    psat_temperature,
    sep_measured,
    sep_pressures,
    sep_temperatures,
)
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- Running Inline Simulations ----
# This example demonstrates running simulations inline without having to upload resources and create configurations.
# This is useful for quick simulations or testing that don't need to be saved or shared.

# Run Inline Flash Simulation
print("=== Running Inline Flash Simulation ===")
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:

    # Run Flash Simulation
    print("Running Flash Simulation...")
    flash_result = client.simulations.run_flash(
        eos=eos_data,
        molar_composition=oil_feed,
        temperatures=flash_temperatures,
        pressures=flash_pressures,
        measured=flash_measured,
    )
    print("Flash Simulation Result:")
    print(json.dumps(flash_result.model_dump(), indent=2))

    # Run CME Simulation
    print("\n=== Running Inline CME Simulation ===")
    print("Running CME Simulation...")
    cme_result = client.simulations.run_cme(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=cme_pressures,
        temperature=cme_temperature,
        measured=cme_measured,
    )
    print("CME Simulation Result:")
    print(json.dumps(cme_result.model_dump(), indent=2))

    # Run CVD Simulation
    print("\n=== Running Inline CVD Simulation ===")
    print("Running CVD Simulation...")
    cvd_result = client.simulations.run_cvd(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=cvd_pressures,
        temperature=cvd_temperature,
        measured=cvd_measured,
    )
    print("CVD Simulation Result:")
    print(json.dumps(cvd_result.model_dump(), indent=2))

    # Run DLE Simulation
    print("\n=== Running Inline DLE Simulation ===")
    print("Running DLE Simulation...")
    dle_result = client.simulations.run_dle(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=dle_pressures,
        temperature=dle_temperature,
        measured=dle_measured,
    )
    print("DLE Simulation Result:")
    print(json.dumps(dle_result.model_dump(), indent=2))

    # Run SEP Simulation
    print("\n=== Running Inline SEP Simulation ===")
    print("Running SEP Simulation...")
    sep_result = client.simulations.run_sep(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=sep_pressures,
        temperatures=sep_temperatures,
        measured=sep_measured,
    )
    print("SEP Simulation Result:")
    print(json.dumps(sep_result.model_dump(), indent=2))

    # Run Process Simulation
    print("\n=== Running Inline Process Simulation ===")
    print("Running Process Simulation...")
    process_result = client.simulations.run_process(
        eos=eos_data,
        molar_stream=oil_feed,
        process=process_data,
    )
    print("Process Simulation Result:")
    print(json.dumps(process_result.model_dump(), indent=2))

    # Run PSAT Simulation
    print("\n=== Running Inline PSAT Simulation ===")
    print("Running PSAT Simulation...")
    psat_result = client.simulations.run_psat(
        eos=eos_data,
        molar_composition=oil_feed,
        measured=psat_measured,
        temperature=psat_temperature,
    )
    print("PSAT Simulation Result:")
    print(json.dumps(psat_result.model_dump(), indent=2))
