import asyncio
import json

from examples.data.eos_development_data import default_eos_input
from fluidmagic_api_sdk.client.async_client import AsyncClient
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Running EOS Development Endpoint ----
# This example demonstrates generating a default EOS model inline.


# Sync example
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:
    eos_data = client.eos.generate_default_eos(default_eos_input)
    print("Generated default EOS (sync):")
    print(json.dumps(eos_data.model_dump(), indent=2))


# Async example
async def run_async_example() -> None:
    async with AsyncClient.using_client_credentials(client_id, client_secret, environment="dev") as client:
        eos_data = await client.eos.generate_default_eos(default_eos_input)
        print("Generated default EOS (async):")
        print(json.dumps(eos_data.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(run_async_example())
