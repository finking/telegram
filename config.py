import os
import configparser
from __path__ import EXE_PATH
from utils import LOGGER
import traceback

dict_setting = {}


def load_config(output_path):
    config_file = os.path.join(output_path, 'config.ini')
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        config.read_dict({
            'DB': {
                'host': 'localhost',
                'user': 'root',
                'passwd': '1234',
                'db': 'first_bot'
            },
            'Telegram': {
                'API_TOKEN': 'API_Bot'
            }
        })
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)
                LOGGER.info(f'Конфигурация записана в {config_file}')
        except Exception as e:
            LOGGER.error(f'Возникла ошибка при Записи данных: {e} в файл {config_file}')
            LOGGER.debug(traceback.format_exc())
        
    return config, config_file


def load_settings():
    try:
        config, config_file = load_config(EXE_PATH)
        dict_setting['host'] = config.get('DB', 'host')
        dict_setting['user'] = config.get('DB', 'user')
        dict_setting['passwd'] = config.get('DB', 'passwd')
        dict_setting['db'] = config.get('DB', 'db')
        if config.get('Telegram', 'API_TOKEN') == 'API_Bot':
            LOGGER.info(f'Замените данные в файле {config_file} на реальные!')
            return False
        else:
            dict_setting['api_token'] = config.get('Telegram', 'API_TOKEN')
    except Exception as e:
        LOGGER.error(f'Возникла ошибка при Загрузки данных: {e}')
        LOGGER.debug(traceback.format_exc())
    
    return dict_setting