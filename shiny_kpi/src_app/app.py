"""App class represent any kind of application.
It is an abstract class that defines the basic methods
"""

from abc import ABC, abstractmethod
from urllib.parse import urlparse

from ..db_connect import DbConnect


class SourceApp(ABC):
    name: str = None
    data: dict = None
    conn: DbConnect = None
    logins: dict = None
    dsn: str = None
    # List of models or table to be used
    domain: list
    # Sql aliases
    table_aliases: dict = None

    def __init__(self, data):
        self.name = data["name"]
        self.dsn = data["dsn"]["main"]
        self.data = data
        self.table_aliases = data.get("odoo").get("table_aliases")
        self.domain = data["domain"].keys()

    def connect(self):
        if not self.conn:
            conn = DbConnect(self.dsn)
            if conn:
                self.conn = conn
        return self.conn

    @abstractmethod
    def get_organizations(self):
        pass

    @abstractmethod
    def get_sql_from_table(self, table):
        pass

    def get_table(self, model):
        return model

    @abstractmethod
    def get_tables(self):
        pass

    def split_dsn(self):
        """Split the DSN into its components."""
        parsed = urlparse(self.dsn)
        return {
            "scheme": parsed.scheme,
            "user": parsed.username,
            "password": parsed.password,
            "host": parsed.hostname,
            "port": parsed.port,
            "db": parsed.path.lstrip("/"),
        }
