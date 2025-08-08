import logging
import tomllib
from importlib.resources import files

logger = logging.getLogger(__name__)


def load():
    package = get_override_package()
    return get_custom_settings(package)


def get_override_package():
    with open("data/config.toml", "rb") as config:
        parsed = tomllib.load(config)
        return recursive_dict_get(parsed, ["override_package", "package"])


def get_custom_settings(override_package):
    def get_config_data(file, package=override_package):
        try:
            file_path = files(package.replace("-", "_")) / f"data/{file}.toml"
        except ModuleNotFoundError as e:
            e.add_note(
                f"  >> Please check than package '{package}' is installed"
                + " to continue sucessfully."
            )
            raise e
        except Exception as e:
            raise e
        data = False
        try:
            with file_path.open("rb") as f:
                data = tomllib.load(f)
        except FileNotFoundError as e:
            e.add_note(
                f"  >> Please check than file '{file_path}' exists or create it"
                + " to continue sucessfully."
            )
            raise e
        except Exception as e:
            raise e
        return data

    main_settings = get_config_data("config")
    dsn = get_config_data("dsn")
    main_settings.update(dsn)
    check_custom_settings(main_settings)
    name = main_settings["name"]
    if name == "odoo":
        odoo_toml = get_config_data("odoo", "shiny-kpi")
        main_settings.update({"odoo": odoo_toml})
    return main_settings


def check_custom_settings(data):
    messages = []
    source = data.get("data_source")
    if not source:
        messages = ["Missing 'data_source' in config.toml file."]
    name = source.get("name")
    if not name:
        messages.append("Missing 'name' in 'data_source' section in config.toml file")
        if name == "odoo":
            """"""
            # TODO manage case where this is not Odoo
    dsn = data.get("dsn")
    if not dsn or not dsn.get("main"):
        messages.append("Missing 'dsn.main' section in dsn.toml file")
    if messages:
        logger.error(f"Custom settings check failed: {', '.join(messages)}")


def recursive_dict_get(my_dict, keys):
    tree = my_dict.copy()
    for key in keys:
        value = tree.get(key)
        if value:
            tree = tree[key]
        else:
            return False
    return tree
