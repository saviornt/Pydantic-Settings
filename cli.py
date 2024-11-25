import click
from .core import pydantic_settings
from dotenv import dotenv_values

class PydanticSettingsCLI:
    """Command-Line Interface for Pydantic_Settings."""

    @staticmethod
    @click.group()
    def cli():
        """Main CLI group."""
        pass

    @staticmethod
    @cli.command()
    @click.argument("file", type=click.Path(exists=True))
    def validate_env(file):
        """Validate the .env file."""
        env_vars = dotenv_values(file)
        schema = pydantic_settings.generate_schema(env_vars)
        try:
            pydantic_settings.validate_env_vars(env_vars, schema)
            click.echo("Environment file is valid!")
        except ValueError as e:
            click.echo(f"Validation failed: {e}")

    @staticmethod
    @cli.command()
    @click.argument("file", type=click.Path(exists=True))
    def encrypt_env(file):
        """Encrypt the .env file."""
        pydantic_settings.encrypt_env_file(file)
        click.echo(f"{file} has been encrypted.")

    @staticmethod
    @cli.command()
    @click.argument("file", type=click.Path(exists=True))
    def decrypt_env(file):
        """Decrypt the .env file."""
        decrypted_data = pydantic_settings.decrypt_env_file(file)
        click.echo("Decrypted environment variables:")
        for key, value in decrypted_data.items():
            click.echo(f"{key}={value}")

    @staticmethod
    @cli.command()
    def list_env():
        """List all environment variables."""
        settings = pydantic_settings.load_env()
        for key, value in settings.items():
            click.echo(f"{key}={value}")

if __name__ == "__main__":
    PydanticSettingsCLI.cli()
