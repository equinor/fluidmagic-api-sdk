from fluidmagic_api_sdk.models.config_models import ConfigModel
from fluidmagic_api_sdk.models.data_models.calculated import FlashCalculated
from fluidmagic_api_sdk.models.fluid_models import FluidModel
from fluidmagic_api_sdk.models.process_models import ProcessModel


def parse_process(payload: dict) -> ProcessModel:
    return ProcessModel.model_validate(payload)


def parse_process_list(payload: list[dict]) -> list[ProcessModel]:
    return [ProcessModel.model_validate(item) for item in payload]


def parse_fluid(payload: dict) -> FluidModel:
    return FluidModel.model_validate(payload)


def parse_fluid_list(payload: list[dict]) -> list[FluidModel]:
    return [FluidModel.model_validate(item) for item in payload]


def parse_config(payload: dict) -> ConfigModel:
    return ConfigModel.model_validate(payload)


def parse_config_list(payload: list[dict]) -> list[ConfigModel]:
    return [ConfigModel.model_validate(item) for item in payload]


def parse_flash_result(payload: dict) -> FlashCalculated:
    return FlashCalculated.model_validate(payload)
