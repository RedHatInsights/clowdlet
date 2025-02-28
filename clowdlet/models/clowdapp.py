"""ClowdApp model module."""
from pathlib import Path
from typing import Any

from clowdlet.models.deployment import Deployment
from clowdlet.utils import replace_vars


class ClowdApp:
    """Class representing single ClowdApp containing multiple deployments and other objects."""

    def __init__(self, clowdapp_yaml: dict[str, Any], parameters: dict[str, str]):
        self.name: str = replace_vars(clowdapp_yaml.get("metadata", {}).get("name", "clowdapp"), parameters)
        self.deployments: list[Deployment] = []

        self._parse_deployments(clowdapp_yaml.get("spec", {}).get("deployments", []), parameters)

    def _parse_deployments(self, deployments: list[dict[str, Any]], parameters: dict[str, str]) -> None:
        for deployment in deployments:
            self.deployments.append(Deployment(deployment, parameters, self.name))

    def render_quadlet_network(self) -> str:
        """Return string representing quadlet unit compatible with systemd."""
        lines = [
            "[Unit]",
            "After=network-online.target",
            "",
            "[Network]",
            f"NetworkName={self.name}",
            "",
            "[Install]",
            "WantedBy=multi-user.target default.target",
        ]
        return "\n".join(lines) + "\n"

    def write_quadlets(self, output_directory: str) -> None:
        """Create directory and Quadlet files for the ClowdApp in output_directory."""
        clowdapp_directory = Path(output_directory) / self.name
        print(f"Creating directory: {clowdapp_directory}")
        Path(clowdapp_directory).mkdir(exist_ok=True, parents=True)

        network_file = Path(clowdapp_directory) / f"{self.name}.network"
        print(f"Creating file: {network_file}")
        with Path(network_file).open("w") as network_file_f:
            network_file_f.write(self.render_quadlet_network())

        for deployment in self.deployments:
            deployment.write_quadlets(clowdapp_directory)
