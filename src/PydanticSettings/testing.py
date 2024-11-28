import asyncio
import os
from unittest.mock import AsyncMock, patch
from typing import Dict, Any, AsyncGenerator
from pydantic import ValidationError
from core import PydanticSettings, EnvironmentSettings


class AsyncUnitTestingUtilities:
    """
    A utility class to provide async features for unit testing with PydanticSettings.
    """

    @staticmethod
    async def mock_env_vars(env: Dict[str, Any]) -> AsyncGenerator[None, None]:
        """
        Async context manager to mock environment variables.

        Args:
            env (dict): Dictionary of environment variables to mock.

        Yields:
            None: Mocks the environment variables within the context.
        """
        with patch.dict("os.environ", env):
            yield

    @staticmethod
    async def validate_settings(settings_class: Any, env_vars: Dict[str, Any]) -> bool:
        """
        Validate a Pydantic settings class against mocked environment variables asynchronously.

        Args:
            settings_class (Any): The Pydantic settings class to validate.
            env_vars (dict): Mocked environment variables.

        Returns:
            bool: True if validation succeeds, raises ValidationError otherwise.
        """
        async with AsyncUnitTestingUtilities.mock_env_vars(env_vars):
            try:
                settings = settings_class()
                print("Validation Passed:", settings.dict())
                return True
            except ValidationError as e:
                print("Validation Failed:", e.errors())
                raise e

    @staticmethod
    async def simulate_profile_switch(pydantic_settings_instance: PydanticSettings, profile: str) -> AsyncGenerator[None, None]:
        """
        Async context manager to simulate switching environment profiles and test their effects.

        Args:
            pydantic_settings_instance (PydanticSettings): Instance of PydanticSettings.
            profile (str): Profile to switch to (e.g., "Production", "Testing").

        Yields:
            None: Simulates the profile switch for testing.
        """
        original_profile = pydantic_settings_instance.environment
        try:
            pydantic_settings_instance.set_environment(profile)
            yield
        finally:
            # Restore the original profile after testing
            pydantic_settings_instance.set_environment(original_profile)

    @staticmethod
    async def mock_secrets_manager(secrets: Dict[str, Any]) -> AsyncGenerator[None, None]:
        """
        Mock secrets manager asynchronously for testing secret retrieval.

        Args:
            secrets (dict): Mocked secrets to simulate secrets manager behavior.

        Yields:
            None: Simulates secrets retrieval within the context.
        """
        async_mock = AsyncMock(return_value=secrets)
        with patch.object(PydanticSettings, "fetch_secrets", async_mock):
            yield

    @staticmethod
    async def simulate_invalid_env_file(env_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate an invalid `.env` file asynchronously for testing validation errors.

        Args:
            env_vars (dict): A dictionary of invalid environment variables.

        Returns:
            dict: Invalid `.env` file content.
        """
        # Add malformed or invalid entries
        env_vars["MALFORMED_KEY"] = "==value"
        env_vars["DEBUG"] = "not_a_boolean"
        return env_vars

    @staticmethod
    async def test_full_suite():
        """
        Comprehensive example of testing all features in the async unit testing utilities.
        """
        pydantic_settings_instance = PydanticSettings()

        # Mock environment variables
        async with AsyncUnitTestingUtilities.mock_env_vars({"APP_NAME": "TestApp", "DEBUG": "true"}):
            assert os.getenv("APP_NAME") == "TestApp"

        # Validate settings class
        mock_env = {"APP_NAME": "ValidApp", "DEBUG": "false", "PORT": "8080"}
        assert await AsyncUnitTestingUtilities.validate_settings(EnvironmentSettings, mock_env)

        # Simulate profile switching
        async with AsyncUnitTestingUtilities.simulate_profile_switch(pydantic_settings_instance, "Testing"):
            assert pydantic_settings_instance.environment == "Testing"
        # Original environment is restored
        assert pydantic_settings_instance.environment == "Development"

        # Mock secrets manager
        mock_secrets = {"SECRET_KEY": "MockSecret"}
        async with AsyncUnitTestingUtilities.mock_secrets_manager(mock_secrets):
            secrets = await pydantic_settings_instance.fetch_secrets()
            assert secrets["SECRET_KEY"] == "MockSecret"

        # Simulate invalid environment
        invalid_env = await AsyncUnitTestingUtilities.simulate_invalid_env_file({"PORT": "not_a_number"})
        try:
            await AsyncUnitTestingUtilities.validate_settings(EnvironmentSettings, invalid_env)
        except ValidationError:
            print("Validation failed as expected for invalid environment variables.")


# Singleton instance for easier import
unit_testing = AsyncUnitTestingUtilities()
