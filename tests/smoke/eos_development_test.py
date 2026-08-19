from examples.data.eos_development_data import default_eos_input, tune_eos_input
from fluidmagic_api_sdk.models.data_models.eos_data import EOSData
from fluidmagic_api_sdk.models.eos_models import EOSTuneResultModel


def test_generate_default_eos_smoke(sync_client):
    result = sync_client.eos.generate_default_eos(default_eos_input)
    assert isinstance(result, EOSData)
    assert result.component_names
    assert len(result.component_names) == len(result.molecular_weights)


def test_generate_default_eos_smoke_async(run_with_async_client):
    result = run_with_async_client(lambda client: client.eos.generate_default_eos(default_eos_input))
    assert isinstance(result, EOSData)
    assert result.component_names
    assert len(result.component_names) == len(result.molecular_weights)


def test_tune_eos_smoke(sync_client):
    result = sync_client.eos.tune_eos(tune_eos_input)
    assert isinstance(result, EOSTuneResultModel)
    assert result.parameters_used
    assert result.tuned_eos_data.component_names


def test_tune_eos_smoke_async(run_with_async_client):
    result = run_with_async_client(lambda client: client.eos.tune_eos(tune_eos_input))
    assert isinstance(result, EOSTuneResultModel)
    assert result.parameters_used
    assert result.tuned_eos_data.component_names
