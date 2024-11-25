import os
from .core import pydantic_settings

class PydanticSettingsHelp:
    """
    Provides detailed help information about the PydanticSettings library.
    """

    @staticmethod
    def get_help() -> str:
        """
        Returns a comprehensive help file as a string.

        Returns:
            str: Help text describing the library's features, usage, and examples.
        """
        help_text = """
PydanticSettings Library Help
=============================
The `PydanticSettings` library provides a robust system for managing environment
variables, configurations, and secrets in Python projects.

Features:
---------
1. **Environment Management**:
   - Load and validate `.env` files.
   - Support nested variables (e.g., `DATABASE__USER`).
   - Dynamically merge settings from `.env`, YAML, JSON, and secrets managers.

2. **Secrets Management**:
   - Integrates with AWS Secrets Manager, Azure Key Vault, and Google Secret Manager.
   - Encrypted `.env` fallback for local secrets management.

3. **Environment Profiles**:
   - Supports profiles such as `Development`, `Production`, and `Testing`.

4. **Utilities**:
   - Export settings to JSON or YAML.
   - Command-line interface for validating and encrypting `.env` files.
   - Encrypt an existing `.env` file securely for production use.

Encrypting a `.env` File:
-------------------------
The `encrypt_env_file()` method allows you to securely encrypt an existing `.env` file.

Usage:
    ```python
    from PydanticSettings import pydantic_settings

    # Encrypt an existing .env file
    pydantic_settings.encrypt_env_file(".env")
    ```

This generates a key (if not already present) and saves the encrypted file as `.env.encrypted`.

Creating an Environment File:
-----------------------------
The `.env` file is a text file containing key-value pairs:
Example:
    APP_NAME=MyApp
    DEBUG=true
    DATABASE__USER=admin
    DATABASE__PASSWORD=securepassword

For nested variables, use double underscores (`__`) to represent nested keys.

Using the CLI:
--------------
The library includes a command-line interface (CLI). Install the library and use:
    $ pydantic_settings validate-env .env
    $ pydantic_settings encrypt-env .env
    $ pydantic_settings decrypt-env .env.encrypted

Library Usage:
--------------
1. **Loading Settings**:
    ```python
    from PydanticSettings import pydantic_settings

    async def main():
        settings = await pydantic_settings.load_env()
        print(settings.app_name)

    import asyncio
    asyncio.run(main())
    ```

2. **Exporting Settings**:
    ```python
    from PydanticSettings import export_settings

    settings_dict = {"app_name": "MyApp", "debug": True}
    print(export_settings(settings_dict, format="yaml"))
    ```

3. **Async Unit Testing**:
    ```python
    import asyncio
    from PydanticSettings import unit_testing

    async def test_example():
        # Mock environment variables
        async with unit_testing.mock_env_vars({"APP_NAME": "TestApp"}):
            assert os.getenv("APP_NAME") == "TestApp"

        # Validate settings
        mock_env = {"APP_NAME": "ValidApp", "DEBUG": "false", "PORT": "8080"}
        assert await unit_testing.validate_settings(EnvironmentSettings, mock_env)

    asyncio.run(test_example())
    ```

For additional documentation, visit the official repository or contact support.

"""
        return help_text

    @staticmethod
    def get_dynamic_help() -> str:
        """
        Returns a dynamically generated help file, including active profiles and secrets managers.

        Returns:
            str: Help text including real-time details of the user's configuration.
        """
        current_profile = pydantic_settings.environment
        secrets_manager = (
            os.getenv("SECRETS_MANAGER", "Not configured")
            .replace("_", " ")
            .title()
        )

        dynamic_help = f"""
Dynamic Details:
----------------
Current Environment Profile: {current_profile}
Configured Secrets Manager: {secrets_manager}
"""
        return PydanticSettingsHelp.get_help() + dynamic_help


# Singleton instance for easier import
help = PydanticSettingsHelp()
