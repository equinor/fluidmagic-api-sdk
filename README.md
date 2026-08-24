# fluidmagic-api-sdk
Python SDK for accessing and working with the FluidMagic API:

DEV: https://api-fluidmagic-api-dev.radix.equinor.com/docs#/

PROD: https://api-fluidmagic-api-prod.radix.equinor.com/docs#/


## Quick Start

### Basic Client Usage

Here's a simple example to get started with the FluidMagic API:

```python
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Create a client using credentials
with Client.using_client_credentials(client_id, client_secret) as client:
    # List all facilities
    facilities = client.list_facilities()
    print(facilities)
```

### Interactive Login

For interactive authentication with delegated user permissions:

```python
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "YOUR_CLIENT_ID"

# Login interactively
with Client.using_interactive_login(client_id) as client:
    facilities = client.list_facilities()
    print(facilities)
```

### Working with the DEV Environment
To connect to the DEV environment, specify the `environment` parameter when creating the client:

```python
from fluidmagic_api_sdk.client.sync_client import Client

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Create a client for the DEV environment
with Client.using_client_credentials(client_id, client_secret, environment="dev") as client:
    facilities = client.list_facilities()
    print(facilities)
```

## Examples

The `examples/` directory contains comprehensive examples demonstrating SDK functionality:

- **01_run_client_within_context_manager.py** - Basic client usage with credentials
- **02_login_with_interactive_client.py** - Interactive login flow
- **03_async_client.py** - Asynchronous client operations
- **04_run_conversions.py** - Inline conversion examples
- **05_run_simulations.py** - Inline simulation examples
- **06_run_eos_development_functions.py** - EOS development functions (e.g., create default EOS, tune EOS)

Shared input payloads used by the examples are defined in `examples/data/`.
