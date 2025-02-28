"""ClowdAppTemplate model module."""
from typing import Any

from clowdlet.models.clowdapp import ClowdApp


class ClowdAppTemplate:
    """Class representing template containing multiple ClowdApp templates and list of applicable parameters."""

    def __init__(self, template_yaml: dict[str, Any], custom_env: dict[str, str]):
        self.parameters: dict[str, str] = {}
        self.clowdapps: list[ClowdApp] = []

        if template_yaml.get("kind", "") != "Template":
            msg = "Expecting Template kind in the yaml file."
            raise ValueError(msg)

        self._parse_parameters(template_yaml.get("parameters", []), custom_env)
        self._parse_objects(template_yaml.get("objects", []))

    def _parse_parameters(self, parameters: list[dict[str, str]], custom_env: dict[str, str]) -> None:
        for param in parameters:
            param_name = param["name"]
            param_value = custom_env[param_name] if param_name in custom_env else param.get("value", "")
            if not isinstance(param_value, str):
                msg = f"Type of parameter {param_name} is not str."
                raise TypeError(msg)
            self.parameters[param_name] = param_value
        # Merge rest of custom env into parameters dict (on top of template parameters)
        for custom_param, custom_val in custom_env.items():
            if custom_param not in self.parameters:
                self.parameters[custom_param] = custom_val

    def _parse_objects(self, objects: list[dict[str, Any]]) -> None:
        for obj in objects:
            if obj.get("kind", "") == "ClowdApp":
                self.clowdapps.append(ClowdApp(obj, self.parameters))
