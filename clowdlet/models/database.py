"""Database model module."""
from __future__ import annotations

from clowdlet.models.deployment import Deployment
from clowdlet.utils import replace_vars

PG_IMAGE = "quay.io/cloudservices/postgresql-rds"


class Database(Deployment):
    """Class representing single Database deployment - persistently running container."""

    def __init__(self, database_yaml: dict[str, str | int], parameters: dict[str, str], clowdapp_name: str):
        self.name = "database"
        self.db_name = replace_vars(str(database_yaml["name"]), parameters)
        self.db_version = replace_vars(str(database_yaml["version"]), parameters)
        self.image = f"{PG_IMAGE}:{self.db_version}"
        self.command = ""
        self.env = {
            "POSTGRESQL_DATABASE": self.db_name,
            "POSTGRESQL_USER": parameters.get("POSTGRESQL_USER", ""),
            "POSTGRESQL_PASSWORD": parameters.get("POSTGRESQL_PASSWORD", ""),
        }
        self.clowdapp_name = clowdapp_name
