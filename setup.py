from setuptools import setup, find_packages

setup(
    name="PydanticSettings",
    version="1.0.0",
    author="Your Name",
    description="Dynamic environment and configuration management with Pydantic.",
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.10.2",
        "python-dotenv>=1.0.0",
        "cryptography>=3.4.8",
        "PyYAML>=6.0",
    ],
    extras_require={
        "aws": ["boto3>=1.17.0"],
        "azure": ["azure-keyvault-secrets>=4.3.0", "azure-identity>=1.5.0"],
        "google": ["google-cloud-secret-manager>=2.7.0"],
    },
    entry_points={
        "console_scripts": [
            "pydantic_settings=PydanticSettings.cli:PydanticSettingsCLI.cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
