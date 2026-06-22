# fluidmagic-api-sdk
Python SDK for accessing and working with the FluidMagic API:

DEV: https://api-fluidmagic-api-dev.radix.equinor.com/docs#/

PROD: https://api-fluidmagic-api.radix.equinor.com/docs#/

## Installation

Install the package using pip:

```bash
pip install fluidmagic-api-sdk
```

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
with Client.using_interactive_login(client_id, environment="dev") as client:
    facilities = client.list_facilities()
    print(facilities)
```

## Examples

The `examples/` directory contains comprehensive examples demonstrating SDK functionality:

- **01_run_client_within_context_manager.py** - Basic client usage with credentials
- **02_login_with_interactive_client.py** - Interactive login flow
- **03_async_client.py** - Asynchronous client operations
- **04_eos_interaction_and_flash_simulation.py** - EOS management and flash simulations
- **05_run_moles_to_vol_conversion.py** - Moles to volume conversion workflow
- **06_run_rate_to_moles_conversion.py** - Rate to moles conversion workflow
