import tomllib
import tomlkit
import os

def check_config():
    config = """
# DO NOT TOUCH
config_version = "0.0.1"

# [MAIN]
# sets the home command timeout in seconds
home_timeout = 10

# [ECONOMY]

# if you have the Economy Pilot plugin, you can enable it here
economy_enabled = false

# sets the minimum warp price, before the distance calculation, 0 to disable
min_home_teleport_price = 100
# sets the distance calculation price multiplier, set to 0.0 to disable
home_teleport_price_multiplier = 1.0
    """

    directory = 'config'
    filename = 'home-pilot.toml'
    file_path = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)

    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.write(config)


def load_config():
    directory = 'config'
    filename = 'home-pilot.toml'
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'rb') as file:
        toml_data = tomllib.load(file)
        home_timeout = toml_data.get("home_timeout")

        economy_enabled = toml_data.get("economy_enabled")
        minimum_home_warp_price = toml_data.get("min_home_teleport_price")
        home_teleport_price_multiplier = toml_data.get("home_teleport_price_multiplier")

    return home_timeout, economy_enabled, minimum_home_warp_price, home_teleport_price_multiplier

### ECONOMY PILOT INTEGRATION

def load_config_eco():
    directory = 'config'
    filename = 'economy-pilot-lite.toml'
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'rb') as file:
        toml_data = tomllib.load(file)
        currency_symbol = toml_data.get("currency_symbol")
    return currency_symbol