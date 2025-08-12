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
    lang: str = "en_US"
    logins: dict = None
    dsn: str = None
    # List of models or table to be used
    domains: list
    # Sql aliases
    table_aliases: dict = None
    # Dataframes keys
    df_keys: list = None
    # DataFrames
    df: dict = {}

    def __init__(self, data):
        self.name = data["name"]
        self.dsn = data["dsn"]["main"]
        self.data = data
        self.table_aliases = data.get("odoo").get("table_aliases")
        self.domains = data["domain"].keys()
        self.set_df_keys()
        if "lang" in data:
            self.lang = data["lang"]

    def set_df_keys(self):
        df_by_domain_keys = []
        for domain in self.data["domain"].values():
            df_by_domain_keys.append(domain)
        dfs = []
        for elm in df_by_domain_keys:
            dfs.extend(elm)
        self.df_keys = dfs

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

    def welcome(self):
        return """
        # Hello World

        Here is your **Shiny Kpi** application.

        Tabs on the right give acces to many data information.

        Sidebar on the left allows you to globally filter your kpis.
        """

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
