from examples.data.conversion_data import (
    characterization_input,
    eos_data,
    fluid,
    moles_to_vol_input,
    output_filter,
    process_data,
    rate_to_moles_input,
)
from fluidmagic_api_sdk.models.config_models import FluidFilterType


def test_inline_rate_to_moles_smoke(sync_client):
    rate_to_moles_result = sync_client.conversions.run_rate_to_moles(
        eos=eos_data,
        fluid=fluid,
        process=process_data,
        input=rate_to_moles_input,
        output=FluidFilterType.ALL,
    )
    assert rate_to_moles_result.headers
    assert rate_to_moles_result.data


def test_inline_moles_to_volume_smoke(sync_client):
    moles_to_volume_result = sync_client.conversions.run_moles_to_volume(
        eos=eos_data,
        process=process_data,
        input=moles_to_vol_input,
        output=output_filter,
    )
    assert moles_to_volume_result.headers
    assert moles_to_volume_result.data


def test_inline_characterize_fluid_to_eos_smoke(sync_client):
    characterization_result = sync_client.conversions.run_characterize_fluid_to_eos(
        eos=eos_data,
        input_data=characterization_input,
    )
    assert characterization_result.characterized_fluid.headers
    assert characterization_result.characterized_fluid.data


def test_inline_rate_to_moles_smoke_async(run_with_async_client):
    rate_to_moles_result = run_with_async_client(
        lambda client: client.conversions.run_rate_to_moles(
            eos=eos_data,
            fluid=fluid,
            process=process_data,
            input=rate_to_moles_input,
            output=FluidFilterType.ALL,
        )
    )
    assert rate_to_moles_result.headers
    assert rate_to_moles_result.data


def test_inline_moles_to_volume_smoke_async(run_with_async_client):
    moles_to_volume_result = run_with_async_client(
        lambda client: client.conversions.run_moles_to_volume(
            eos=eos_data,
            process=process_data,
            input=moles_to_vol_input,
            output=output_filter,
        )
    )
    assert moles_to_volume_result.headers
    assert moles_to_volume_result.data


def test_inline_characterize_fluid_to_eos_smoke_async(run_with_async_client):
    characterization_result = run_with_async_client(
        lambda client: client.conversions.run_characterize_fluid_to_eos(
            eos=eos_data,
            input_data=characterization_input,
        )
    )
    assert characterization_result.characterized_fluid.headers
    assert characterization_result.characterized_fluid.data
