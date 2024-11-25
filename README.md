# PydanticSettings

**PydanticSettings** is a powerful Python library designed to streamline the management of environment variables, configurations, and secrets in Python projects. It integrates Pydantic's robust validation capabilities, supports encrypted `.env` files, and offers optional integration with AWS, Azure, and Google secrets managers.

## Features

- **Environment Management**:
  - Load and validate `.env` files with Pydantic's strong typing.
  - Support for nested variables (e.g., `DATABASE__USER`).
  - Dynamically merge settings from `.env`, YAML, JSON, and secrets managers.

- **Secrets Management**:
  - Integration with AWS Secrets Manager, Azure Key Vault, and Google Cloud Secret Manager.
  - Encrypted `.env` fallback for local secrets management.

- **Environment Profiles**:
  - Easily switch between `Development`, `Production`, and `Testing` profiles.

- **Utilities**:
  - Export settings to JSON or YAML.
  - Command-line interface (CLI) for validation and encryption.
  - Encrypt an existing `.env` file securely for production use.

- **Async Testing Utilities**:
  - Mock environment variables, secrets, and profiles.
  - Validate settings asynchronously.

## Installation

### Core Library

**Install the library from GitHub:**

```bash
pip install git+https://github.com/saviornt/Pydantic-Settings.git
```

### Optional Integrations

**AWS Secrets Manager:**

```bash
pip install git+https://github.com/<username>/<repository>.git#egg=PydanticSettings[aws]
```

**Azure Key Vault:**

``` bash
pip install git+https://github.com/<username>/<repository>.git#egg=PydanticSettings[azure]
```

**Google Cloud Secret Manager:**

``` bash
pip install git+https://github.com/<username>/<repository>.git#egg=PydanticSettings[google]
```

**Install with all integrations:**

```bash
pip install git+https://github.com/<username>/<repository>.git#egg=PydanticSettings[aws,azure,google]
```

## Quick Start

### Loading Settings

```python
from PydanticSettings import pydantic_settings

async def main():
    settings = await pydantic_settings.load_env()
    print(settings.app_name)

import asyncio
asyncio.run(main())
```

### Encrypting a .env File

```python
from PydanticSettings import pydantic_settings

# Encrypt an existing .env file
pydantic_settings.encrypt_env_file(".env")
```

### Validating Settings (Async)

```python
import asyncio
from PydanticSettings import unit_testing, EnvironmentSettings

async def test_example():
    # Mock environment variables
    async with unit_testing.mock_env_vars({"APP_NAME": "TestApp"}):
        assert os.getenv("APP_NAME") == "TestApp"

    # Validate settings
    mock_env = {"APP_NAME": "ValidApp", "DEBUG": "false", "PORT": "8080"}
    assert await unit_testing.validate_settings(EnvironmentSettings, mock_env)

asyncio.run(test_example())
```

## CLI Usage

### Validate a .env File

```bash
pydantic_settings validate-env .env
```

### Encrypt a .env File

```bash
pydantic_settings encrypt-env .env
```

### Decrypt an .env.encrypted File

```bash
pydantic_settings decrypt-env .env.encrypted
```

## Advanced Features

### Switching Profiles

```python
from PydanticSettings import pydantic_settings

pydantic_settings.set_environment("Production")
```

### Using Secrets Managers

- AWS Secrets Manager: `Set SECRETS_MANAGER=secretsmanager` in your `.env` file.
- Azure Key Vault: Set `SECRETS_MANAGER=keyvault` and provide `AZURE_VAULT_URL`.
- Google Cloud Secret Manager: Set `SECRETS_MANAGER=google_secret_manager` and provide `GOOGLE_PROJECT_ID`.

### Export Settings to YAML or JSON

```python
Copy code
from PydanticSettings import export_settings

settings_dict = {"app_name": "MyApp", "debug": True}
print(export_settings(settings_dict, format="yaml"))
```

## Contribution

We welcome contributions! Please fork the repository and submit a pull request with detailed changes.

## License

This library is licensed under the MIT License. See the LICENSE file for details.
