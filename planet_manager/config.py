import os
import sys

from xdg import BaseDirectory

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def config():
    config_path = BaseDirectory.load_first_config("pman")

    try:
        config_file = os.path.join(config_path, "config.toml")
        f = open(config_file, "rb")
        config = tomllib.load(f)

        return config
    except FileNotFoundError:
        print("No configuration file found.", file=sys.stderr)
        exit(1)
    except tomllib.TOMLDecodeError:
        logger.error(f"Configuration file is invalid.", file=sys.stderr)
        exit(1)
