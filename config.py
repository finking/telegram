import os
import configparser
from __path__ import EXE_PATH

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
                'API_TOKEN': '%API_Bot%'
            }
        })
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
    return config


def load_settings():
    try:
        config = load_config(EXE_PATH)
        dict_setting['host'] = config.get('DB', 'host')
        dict_setting['user'] = config.get('DB', 'user')
        dict_setting['passwd'] = config.get('DB', 'passwd')
        dict_setting['db'] = config.get('DB', 'db')
        dict_setting['api_token'] = config.get('Telegram', 'API_TOKEN')
    except Exception as e:
        print(f'Error in config: {e}')  
    
    return dict_setting