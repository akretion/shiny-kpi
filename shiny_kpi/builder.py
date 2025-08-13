from shiny import render

from .main import instance
from .tool import drop_null_columns_in_df


def get_nav_panels(ui):
    panels = []
    get_dataframes()
    for domain in instance.domains:
        dfs = [
            instance.df.get(x)
            # x: instance.df.get(x)
            for x in instance.data["domain"][domain]
            if x in instance.df
        ]
        if dfs:
            panels.append(ui.nav_panel(domain, dfs))
    return panels


@render.data_frame
def get_dataframe(dfs):
    return dfs


def get_dataframes():
    """
    Get the dataframe for each domain.
    """
    data = instance.data
    for elm in instance.src_keys:
        sql = instance.get_sql_from_src(data["src"][elm])
        if sql:
            df = instance.conn.read(sql)
            df = drop_null_columns_in_df(df)
            instance.df[elm] = df
