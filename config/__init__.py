import configparser

DEFAULT_CONFIG_FILE = "./config.ini"


class ConfigUtil():
    def __init__(self):
        self.config = configparser.SafeConfigParser()
        self.config.read(DEFAULT_CONFIG_FILE)


_util = ConfigUtil()


def get(section, key):
    return _util.config.get(section, key)

def getint(section, key):
    return _util.config.getint(section, key)
