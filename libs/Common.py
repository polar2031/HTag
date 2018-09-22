import configparser


class Config:
    CONFIG_FILE = 'config.ini'

    @staticmethod
    def create_config(config_file=CONFIG_FILE, lang='zh_TW'):
        config = configparser.ConfigParser()
        config['DEFAULT']['language'] = lang
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        return config

    @staticmethod
    def get_config(config_file=CONFIG_FILE):
        config = configparser.ConfigParser()
        if config.read(config_file):
            return config
        return None
