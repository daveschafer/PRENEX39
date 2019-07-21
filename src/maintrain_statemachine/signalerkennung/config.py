import configparser


def parse_config(configfile):
    """Parse and validate the given config file."""
    config = configparser.ConfigParser()
    config.read(str(configfile))
    return config
