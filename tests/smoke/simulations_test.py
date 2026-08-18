from examples.data.simulations_data import (
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


def test_inline_flash_smoke(sync_client):
    flash_result = sync_client.simulations.run_flash(
        eos=eos_data,
        molar_composition=oil_feed,
        temperatures=flash_temperatures,
        pressures=flash_pressures,
        measured=flash_measured,
    )
    assert flash_result.flash_calculated.gas_oil_ratio


def test_inline_cme_smoke(sync_client):
    cme_result = sync_client.simulations.run_cme(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=cme_pressures,
        temperature=cme_temperature,
        measured=cme_measured,
    )
    assert cme_result.relative_total_volume


def test_inline_cvd_smoke(sync_client):
    cvd_result = sync_client.simulations.run_cvd(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=cvd_pressures,
        temperature=cvd_temperature,
        measured=cvd_measured,
    )
    assert cvd_result.z_factor


def test_inline_dle_smoke(sync_client):
    dle_result = sync_client.simulations.run_dle(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=dle_pressures,
        temperature=dle_temperature,
        measured=dle_measured,
    )
    assert dle_result.oil_formation_volume_factor_dle


def test_inline_sep_smoke(sync_client):
    sep_result = sync_client.simulations.run_sep(
        eos=eos_data,
        molar_composition=oil_feed,
        pressures=sep_pressures,
        temperatures=sep_temperatures,
        measured=sep_measured,
    )
    assert sep_result.total_gas_oil_ratio


def test_inline_process_smoke(sync_client):
    process_result = sync_client.simulations.run_process(
        eos=eos_data,
        molar_stream=oil_feed,
        process=process_data,
    )
    assert process_result.tank_names
    assert len(process_result.oil_volume) == len(process_result.tank_names)


def test_inline_psat_smoke(sync_client):
    psat_result = sync_client.simulations.run_psat(
        eos=eos_data,
        molar_composition=oil_feed,
        measured=psat_measured,
        temperature=psat_temperature,
    )
    assert psat_result.saturation_pressure_calculated.saturation_pressure


def test_inline_flash_smoke_async(run_with_async_client):
    flash_result = run_with_async_client(
        lambda client: client.simulations.run_flash(
            eos=eos_data,
            molar_composition=oil_feed,
            temperatures=flash_temperatures,
            pressures=flash_pressures,
            measured=flash_measured,
        )
    )
    assert flash_result.flash_calculated.gas_oil_ratio


def test_inline_cme_smoke_async(run_with_async_client):
    cme_result = run_with_async_client(
        lambda client: client.simulations.run_cme(
            eos=eos_data,
            molar_composition=oil_feed,
            pressures=cme_pressures,
            temperature=cme_temperature,
            measured=cme_measured,
        )
    )
    assert cme_result.relative_total_volume


def test_inline_cvd_smoke_async(run_with_async_client):
    cvd_result = run_with_async_client(
        lambda client: client.simulations.run_cvd(
            eos=eos_data,
            molar_composition=oil_feed,
            pressures=cvd_pressures,
            temperature=cvd_temperature,
            measured=cvd_measured,
        )
    )
    assert cvd_result.z_factor


def test_inline_dle_smoke_async(run_with_async_client):
    dle_result = run_with_async_client(
        lambda client: client.simulations.run_dle(
            eos=eos_data,
            molar_composition=oil_feed,
            pressures=dle_pressures,
            temperature=dle_temperature,
            measured=dle_measured,
        )
    )
    assert dle_result.oil_formation_volume_factor_dle


def test_inline_sep_smoke_async(run_with_async_client):
    sep_result = run_with_async_client(
        lambda client: client.simulations.run_sep(
            eos=eos_data,
            molar_composition=oil_feed,
            pressures=sep_pressures,
            temperatures=sep_temperatures,
            measured=sep_measured,
        )
    )
    assert sep_result.total_gas_oil_ratio


def test_inline_process_smoke_async(run_with_async_client):
    process_result = run_with_async_client(
        lambda client: client.simulations.run_process(
            eos=eos_data,
            molar_stream=oil_feed,
            process=process_data,
        )
    )
    assert process_result.tank_names
    assert len(process_result.oil_volume) == len(process_result.tank_names)


def test_inline_psat_smoke_async(run_with_async_client):
    psat_result = run_with_async_client(
        lambda client: client.simulations.run_psat(
            eos=eos_data,
            molar_composition=oil_feed,
            measured=psat_measured,
            temperature=psat_temperature,
        )
    )
    assert psat_result.saturation_pressure_calculated.saturation_pressure
