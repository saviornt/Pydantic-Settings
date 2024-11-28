import os
import json
import yaml
import logging
from typing import Any, Dict
from pydantic_settings import BaseSettings
from dotenv import dotenv_values
from cryptography.fernet import Fernet

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Pydantic_Settings")

class EnvironmentSettings(BaseSettings):
    """
    Base class for strongly-typed environment settings.
    """
    app_name: str = "DummyAppName"
    debug: bool = False
    timeout: float = 30.5
    port: int = 8000

    class Config:
        env_file = ".env"  # Default .env file
        env_file_encoding = "utf-8"


class PydanticSettings:
    """
    Core class for managing settings, configurations, and secrets.
    """

    def __init__(self):
        self.yaml_file: str = "config.yaml"
        self.json_file: str = "config.json"
        self.encrypted_env_file: str = ".env.encrypted"
        self.secret_key_file: str = "secret.key"
        self.environment: str = os.getenv("ENVIRONMENT", "Development")
        self.config: Dict[str, Any] = {}

    def set_environment(self, environment: str):
        """
        Set the application environment profile.
        """
        self.environment = environment

    async def load_config(self) -> Dict[str, Any]:
        """
        Load configurations from YAML and JSON files.
        """
        if os.path.exists(self.yaml_file):
            with open(self.yaml_file, "r") as file:
                self.config.update(yaml.safe_load(file))

        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                self.config.update(json.load(file))

        return self.config

    async def fetch_secrets(self) -> Dict[str, Any]:
        """
        Fetch secrets using configured secrets manager or fallback to encrypted .env.
        """
        secrets_client_name = os.getenv("SECRETS_MANAGER", "secretsmanager")
        secrets = {}

        if secrets_client_name == "secretsmanager":
            try:
                import boto3  # type: ignore
                client = boto3.client("secretsmanager")
                secret_id = os.getenv("AWS_SECRET_ID", "MyAppSecrets")
                secrets = json.loads(client.get_secret_value(SecretId=secret_id)["SecretString"])
                logger.info("Loaded secrets from AWS Secrets Manager.")
            except ImportError:
                logger.info("boto3 not installed. AWS Secrets Manager functionality will not be available.")
        elif secrets_client_name == "keyvault":
            try:
                from azure.keyvault.secrets import SecretClient  # type: ignore
                from azure.identity import DefaultAzureCredential  # type: ignore
                vault_url = os.getenv("AZURE_VAULT_URL")
                client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
                secrets = {secret.name: secret.value for secret in client.list_properties_of_secrets()}
                logger.info("Loaded secrets from Azure Key Vault.")
            except ImportError:
                logger.info("Azure Key Vault libraries not installed. Azure functionality will not be available.")
        elif secrets_client_name == "google_secret_manager":
            try:
                from google.cloud import secretmanager  # type: ignore
                client = secretmanager.SecretManagerServiceClient()
                project_id = os.getenv("GOOGLE_PROJECT_ID")
                secrets = {
                    secret.name: secret.payload.data.decode("UTF-8")
                    for secret in client.list_secrets(parent=f"projects/{project_id}")
                }
                logger.info("Loaded secrets from Google Secret Manager.")
            except ImportError:
                logger.info("Google Cloud Secret Manager libraries not installed. Google functionality will not be available.")

        if not secrets:
            logger.warning("No secrets manager found. Using encrypted .env fallback.")
            secrets = await self.load_encrypted_env()

        return secrets

    async def load_encrypted_env(self) -> Dict[str, str]:
        """
        Load and decrypt encrypted environment variables.
        """
        with open(self.secret_key_file, "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        with open(self.encrypted_env_file, "rb") as file:
            decrypted_data = fernet.decrypt(file.read())
        return dict(line.split("=") for line in decrypted_data.decode().splitlines())

    async def load_env(self) -> EnvironmentSettings:
        """
        Load and merge configurations from `.env`, YAML, JSON, and secrets.

        Returns:
            EnvironmentSettings: Parsed and validated environment settings.
        """
        env_vars = dotenv_values(".env")
        await self.load_config()
        secrets = await self.fetch_secrets()

        merged_settings = {**env_vars, **self.config, **secrets}
        return EnvironmentSettings(**merged_settings)

    def encrypt_env_file(self, env_file: str = ".env"):
        """
        Encrypt an existing `.env` file.

        Args:
            env_file (str): Path to the `.env` file to encrypt.
        """
        if not os.path.exists(env_file):
            logger.error(f"File '{env_file}' does not exist.")
            return

        # Generate a key if it doesn't exist
        if not os.path.exists(self.secret_key_file):
            key = Fernet.generate_key()
            with open(self.secret_key_file, "wb") as key_file:
                key_file.write(key)
            logger.info(f"Encryption key generated and saved to '{self.secret_key_file}'.")

        # Read the key
        with open(self.secret_key_file, "rb") as key_file:
            key = key_file.read()

        # Read and encrypt the .env file
        with open(env_file, "r") as file:
            env_data = file.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(env_data.encode())

        # Save encrypted data to the encrypted_env_file
        with open(self.encrypted_env_file, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        logger.info(f"File '{env_file}' encrypted and saved as '{self.encrypted_env_file}'.")
