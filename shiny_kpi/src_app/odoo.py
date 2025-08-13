from pg_autojoin import SqlJoin
from pg_sql_helper import PgSqlHelper
from sqlglot import parse_one, transpile

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

    def get_sql_from_src(self, src):
        table = self.get_table(src.get("model"))
        dsn = self.split_dsn()
        dsn.pop("scheme")
        autojoin = SqlJoin(**dsn)
        if self.table_aliases:
            # If table aliases are defined, we use them
            autojoin.set_aliases(self.table_aliases)
        autojoin.set_columns_to_retrieve(["name", "ref", "code"])
        cols = autojoin.get_columns_in_table(table)
        sql, asterisk_cols = autojoin.get_joined_query(table=table)
        helper = PgSqlHelper(**dsn, lang=self.lang)
        helper.set_columns_to_drop(["create_uid", "create_date"])
        helper.set_columns_to_drop_according_to_regex([r"_id$"])
        if asterisk_cols:
            pfix = asterisk_cols[:-2]
            cols = ", ".join([f"{pfix}.{x}" for x in helper.process(table)])
            sql = sql.replace(asterisk_cols, cols)
        if sql:
            where = src.get("where")
            if where:
                sql = parse_one(sql).where(where).sql()
            sql = transpile(sql, read="postgres")[0]
        return sql

    def _add_common_conditions(self, cols):
        if "company_id" in cols:
            ""
