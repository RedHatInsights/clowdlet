"""Deployment model module."""
from pathlib import Path
from typing import Any

from clowdlet.utils import replace_vars

CLOWDER_CONFIG_ENV = "ACG_CONFIG"


class Deployment:
    """Class representing single Deployment - persistently running container."""

    def __init__(self, deployment_yaml: dict[str, Any], parameters: dict[str, str], default_network: str):
        self.name: str = replace_vars(deployment_yaml["name"], parameters)
        self.image: str = replace_vars(deployment_yaml["podSpec"]["image"], parameters)
        self.command: str = replace_vars(" ".join(deployment_yaml["podSpec"]["command"]), parameters)
        self.env: dict[str, str] = {}
        for variable in deployment_yaml["podSpec"]["env"]:
            self.env[variable["name"]] = replace_vars(variable.get("value", ""), parameters)
        # Path to emulated Clowder config JSON
        self.env[CLOWDER_CONFIG_ENV] = parameters.get(CLOWDER_CONFIG_ENV, "")
        self.network = default_network

    def render_quadlet_container(self) -> str:
        """Return string representing quadlet unit compatible with systemd."""
        lines = [
            "[Container]",
            f"ContainerName={self.name}",
            f"Image={self.image}",
            f"Exec={self.command}",
            f"Network={self.network}.network",
        ]

        for env_key, env_val in self.env.items():
            lines.append(f"Environment={env_key}={env_val}")

        lines.extend(
            [
                "",
                "[Service]",
                "Restart=always",
                "",
                "[Install]",
                "WantedBy=multi-user.target default.target",
            ],
        )
        return "\n".join(lines) + "\n"

    def write_quadlets(self, output_directory: Path) -> None:
        """Generate quadlet files in output_directory."""
        container_file = output_directory / f"{self.name}.container"
        print(f"Creating file: {container_file}")
        with Path(container_file).open("w") as container_file_f:
            container_file_f.write(self.render_quadlet_container())
