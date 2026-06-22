from fluidmagic_api_sdk.client.sync_client import Client

client_id = "CLIENT_ID"  # Replace with the client_id of your application
client_secret = "CLIENT_SECRET"  # Replace with the client_secret of your application


# ---- Login interactively ----
# Login interactively following the delegated user permission flow.

with Client.using_interactive_login(client_id, environment="dev") as client:
    facilities = client.list_facilities()
    print(facilities)
