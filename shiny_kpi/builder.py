from .main import instance


def get_nav_panels(ui):
    panels = []
    query_data(instance.domain)
    for domain in instance.domain:
        panels.append(ui.nav_panel(domain, domain))
    return panels


def query_data(ui):
    get_dataframes(instance.data["domain"])


def get_dataframes(domains):
    """
    Get the dataframe for each domain.
    """
    data = instance.data
    df_keys = []
    for domain in domains.values():
        df_keys.append(domain)
    dfs = []
    for elm in df_keys:
        # get_dataframe([x["model"] for x in df])
        dfs.extend(elm)
    src = []
    for elm in dfs:
        instance.get_sql_from_table(instance.get_table(instance.data["df"][elm]["model"]))
    return df


def get_dataframe(model):
    return 
