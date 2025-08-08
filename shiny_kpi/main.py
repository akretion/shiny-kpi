"""
TODO
- sources:
"""

from shiny_kpi.src_app.odoo import Odoo

from . import config


def main():
    data = config.load()
    inst = get_object(data["name"])(data)
    inst.connect()
    inst.get_logins()
    # inst.get_tables()
    return inst


def get_object(kind):
    """Return an instance of the requested application type.
    Also could be
        case "sage100":
            return Sage100
        case "business_central":
            return BusinessCentral
        case "any":
            return Any
    """
    match kind:
        case "odoo":
            return Odoo
        case _:
            raise ValueError(f"Unsupported type: {kind}")


instance = main()
