from .main import instance


def get_nav_panels(ui):
    panels = []
    for domain in instance.domain:
        panels.append(ui.nav_panel(domain, domain))
    return panels
    # return [ui.nav_panel(x, x) for x in instance.domain]
