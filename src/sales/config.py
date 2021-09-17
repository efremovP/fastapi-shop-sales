from pathlib import Path
from dynaconf import Dynaconf

PROJECT_ROOT = Path(__file__).parents[2]

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

settings = Dynaconf(
    envvar_prefix="FASTAPI_SALES",
    settings_files=['settings.toml', '.secrets.toml'],
)

def get_settings():
    return settings
