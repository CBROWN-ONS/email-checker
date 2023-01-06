import configparser
import os


def read_config():
    config = configparser.ConfigParser()
    config.read(f"{os.getcwd().strip('src')}config.ini")
    config.sections()
    return config


cur_config = read_config()

email = cur_config['SETTINGS']['email']
password = cur_config['SETTINGS']['password']
delete_email = cur_config['FILTERS']['delete_name']
delete_keyword = cur_config['FILTERS']['delete_keyword']
flag_email = cur_config['FILTERS']['flag_name']
flag_keyword = cur_config['FILTERS']['flag_keyword']
