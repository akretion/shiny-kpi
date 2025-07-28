"""
TODO
- sources:
"""

from . import config
from .app.odoo import Odoo


def main():
    data = config.load()
    inst = get_object(data["data_source"]["name"])(data)
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
