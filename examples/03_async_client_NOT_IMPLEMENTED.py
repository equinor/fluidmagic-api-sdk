import asyncio

from fluidmagic_api_sdk.client.async_client import AsyncClient

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application

# ---- Using the Async Client - DOES NOT WORK CURRENTLY. ----
# Use the async client to make requests with async/await syntax.


async def main() -> None:
    async with AsyncClient.using_client_credentials(client_id, client_secret) as client:
        facilities = await client.list_facilities()
        print(facilities)


if __name__ == "__main__":
    asyncio.run(main())
