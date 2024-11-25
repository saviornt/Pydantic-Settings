import json
import yaml

def export_settings(settings: dict, format: str = "json") -> str:
    """
    Export settings in JSON or YAML format.

    Args:
        settings (dict): Dictionary of settings.
        format (str): Format to export ("json" or "yaml").

    Returns:
        str: Exported settings as a string.
    """
    if format == "json":
        return json.dumps(settings, indent=2)
    elif format == "yaml":
        return yaml.dump(settings, default_flow_style=False)
    else:
        raise ValueError("Unsupported format. Use 'json' or 'yaml'.")
