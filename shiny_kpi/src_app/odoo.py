import polars as pl
from pg_autojoin import SqlJoin

from .app import SourceApp


class Odoo(SourceApp):
    def get_logins(self):
        ignored = self.data.get("odoo").get("misc").get("ignored_logins")
        query = f"SELECT id, login FROM res_users WHERE login NOT IN {tuple(ignored)}"
        self.logins = self.conn.read(query)

    def get_organizations(self):
        query = """
        SELECT c.id, p.name FROM res_company c
            LEFT JOIN res_partner p ON p.id = c.partner_id
        ORDER BY c.id DESC
        """
        return self.conn.read(query, out="list")

    def get_table(self, model):
        return model.replace(".", "_")

    def get_sql_from_table(self, table):
        dsn = self.split_dsn()
        autojoin = SqlJoin(
            db=dsn["db"], user=dsn["user"], password=dsn["password"], host=dsn["host"]
        )
        if self.table_aliases:
            # If table aliases are defined, we use them
            autojoin.set_aliases(self.table_aliases)
        autojoin.set_columns_to_retrieve(["name", "ref", "code"])
        return autojoin.get_joined_query(table=table)

    def get_tables(self):
        """Return list of tables according to:
        - config data source set manually
        - user grants
        """
        sql = f"""
        SELECT model, name FROM ir_model WHERE model IN {tuple(self.instance.models)}"""
        df = self.instance.conn.read(sql)
        # TODO manage exceptions
        df = df.with_columns(
            table=pl.col("model").str.replace(".", "_", literal=True, n=10)
        )
        print(df)
        return df.select("table").to_series().to_list()
