import asyncio
import os
from dataclasses import dataclass
from pathlib import Path

import pytest
from dotenv import load_dotenv

from fluidmagic_api_sdk.client.async_client import AsyncClient
from fluidmagic_api_sdk.client.sync_client import Client

TEST_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(TEST_ENV_PATH, override=False)


@dataclass(frozen=True)
class SmokeSettings:
    client_id: str
    client_secret: str
    environment: str


def _is_unset(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip() in {"", "YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET", "dev|prod"}


@pytest.fixture(scope="session")
def smoke_settings() -> SmokeSettings:
    client_id = os.getenv("FM_TEST_CLIENT_ID")
    client_secret = os.getenv("FM_TEST_CLIENT_SECRET")
    environment = os.getenv("FM_TEST_ENVIRONMENT", "dev")

    if _is_unset(client_id) or _is_unset(client_secret):
        raise RuntimeError(
            "Missing smoke test credentials. Populate tests/.env with FM_TEST_CLIENT_ID and "
            "FM_TEST_CLIENT_SECRET (and optionally FM_TEST_ENVIRONMENT)."
        )

    return SmokeSettings(client_id=client_id, client_secret=client_secret, environment=environment)


@pytest.fixture
def sync_client(smoke_settings: SmokeSettings):
    with Client.using_client_credentials(
        smoke_settings.client_id,
        smoke_settings.client_secret,
        environment=smoke_settings.environment,
    ) as client:
        yield client


@pytest.fixture
def async_client(smoke_settings: SmokeSettings):
    client_cm = AsyncClient.using_client_credentials(
        smoke_settings.client_id,
        smoke_settings.client_secret,
        environment=smoke_settings.environment,
    )
    client = asyncio.run(client_cm.__aenter__())
    try:
        yield client
    finally:
        asyncio.run(client_cm.__aexit__(None, None, None))


@pytest.fixture
def run_async():
    def _run(awaitable):
        return asyncio.run(awaitable)

    return _run
