from typing import Any

from fluidmagic_api_sdk.models.eos_models import EOSCreateModel
from fluidmagic_api_sdk.models.fluid_models import FluidCreateModel
from fluidmagic_api_sdk.models.process_models import ProcessCreateModel


def build_list_facilities() -> dict[str, Any]:
    """Build the request payload for listing facilities."""
    return {
        "method": "GET",
        "path": "/facilities",
    }


def build_get_facility(id: str) -> dict[str, Any]:
    """Build the request payload for getting a specific facility."""
    return {
        "method": "GET",
        "path": f"/facilities/{id}",
    }


def build_list_eoses(facility_id: str, name: str | None = None, component_count: int | None = None) -> dict[str, Any]:
    """Build the request payload for listing EOS models for a facility."""
    params = {}
    if name is not None:
        params["name"] = name
    if component_count is not None:
        params["component_count"] = component_count

    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/eos",
        "params": params if params else None,
    }


def build_get_eos(facility_id: str, eos_id: str) -> dict[str, Any]:
    """Build the request payload for getting a specific EOS model."""
    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/eos/{eos_id}",
    }


def build_create_eos(facility_id: str, eos: EOSCreateModel) -> dict[str, Any]:
    """Build the request payload for creating a new EOS model."""
    return {"method": "POST", "path": f"/facilities/{facility_id}/eos", "body": eos.model_dump()}


def build_delete_eos(facility_id: str, eos_id: str) -> dict[str, Any]:
    """Build the request payload for deleting a specific EOS model."""
    return {
        "method": "DELETE",
        "path": f"/facilities/{facility_id}/eos/{eos_id}",
    }


def build_list_processes(facility_id: str, name: str | None, component_count: int | None) -> dict[str, Any]:
    """Build the request payload for listing Process models for a facility."""
    params = {}
    if name is not None:
        params["name"] = name
    if component_count is not None:
        params["component_count"] = component_count

    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/processes",
        "params": params if params else None,
    }


def build_get_process(facility_id: str, process_id: str) -> dict[str, Any]:
    """Build the request payload for getting a specific Process model."""
    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/processes/{process_id}",
    }


def build_create_process(facility_id: str, process: ProcessCreateModel) -> dict[str, Any]:
    """Build the request payload for creating a new Process model."""
    return {"method": "POST", "path": f"/facilities/{facility_id}/processes", "body": process.model_dump()}


def build_delete_process(facility_id: str, process_id: str) -> dict[str, Any]:
    """Build the request payload for deleting a specific Process model."""
    return {
        "method": "DELETE",
        "path": f"/facilities/{facility_id}/processes/{process_id}",
    }


def build_list_fluids(facility_id: str, name: str | None = None, component_count: int | None = None) -> dict[str, Any]:
    """Build the request payload for listing Fluid models for a facility."""
    params = {}
    if name is not None:
        params["name"] = name
    if component_count is not None:
        params["component_count"] = component_count

    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/fluids",
        "params": params if params else None,
    }


def build_get_fluid(facility_id: str, fluid_id: str) -> dict[str, Any]:
    """Build the request payload for getting a specific Fluid model."""
    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/fluids/{fluid_id}",
    }


def build_create_fluid(facility_id: str, fluid: FluidCreateModel) -> dict[str, Any]:
    """Build the request payload for creating a new Fluid model."""
    return {"method": "POST", "path": f"/facilities/{facility_id}/fluids", "body": fluid.model_dump()}


def build_delete_fluid(facility_id: str, fluid_id: str) -> dict[str, Any]:
    """Build the request payload for deleting a specific Fluid model."""
    return {
        "method": "DELETE",
        "path": f"/facilities/{facility_id}/fluids/{fluid_id}",
    }


def build_list_configs(facility_id: str, name: str | None = None, config_type: str | None = None) -> dict[str, Any]:
    """Build the request payload for listing Config models for a facility."""
    params = {}
    if name is not None:
        params["name"] = name
    if config_type is not None:
        params["config_type"] = config_type

    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/configs",
        "params": params if params else None,
    }


def build_get_config(facility_id: str, config_id: str) -> dict[str, Any]:
    """Build the request payload for getting a specific Config model."""
    return {
        "method": "GET",
        "path": f"/facilities/{facility_id}/configs/{config_id}",
    }


def build_create_config(facility_id: str, body: dict[str, Any]) -> dict[str, Any]:
    """Build the request payload for creating a new Config model."""
    return {"method": "POST", "path": f"/facilities/{facility_id}/configs", "body": body}


def build_delete_config(facility_id: str, config_id: str) -> dict[str, Any]:
    """Build the request payload for deleting a specific Config model."""
    return {
        "method": "DELETE",
        "path": f"/facilities/{facility_id}/configs/{config_id}",
    }


def build_simulate_flash(
    facility_id: str,
    eos_id: str,
    body: dict[str, Any],
) -> dict[str, Any]:
    """Build the request payload for simulating a flash calculation."""
    return {
        "method": "POST",
        "path": f"/facilities/{facility_id}/eos/{eos_id}/simulate-flash",
        "body": body,
    }
