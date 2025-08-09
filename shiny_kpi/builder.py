from .main import instance


def get_nav_panels(ui):
    panels = []
    get_dataframes()
    for domain in instance.domains:
        df = [instance.df.get(x) for x in instance.data['domain'][domain]]
        panels.append(ui.nav_panel(domain, df))
    return panels


def get_dataframes():
    """
    Get the dataframe for each domain.
    """
    data = instance.data
    for elm in instance.df_keys:
        sql = instance.get_sql_from_table(
            instance.get_table(data["df"][elm]["model"])
        )
        if sql:
            instance.df[elm] = instance.conn.read(sql)
