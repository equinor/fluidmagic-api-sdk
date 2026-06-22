from fluidmagic_api_sdk.client.sync_client import Client

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Run the client within a context manager ----
# For making simple request to the FluidMagic API, you can use the client within a context manager. This ensures that the client is properly closed after use.

with Client.using_client_credentials(client_id, client_secret) as client:
    facilities = client.list_facilities()
    print(facilities)
