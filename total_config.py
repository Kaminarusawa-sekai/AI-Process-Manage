import yaml
from pathlib import Path

def load_config(config_path):
    with open(Path(__file__).parent / config_path, 'r',encoding='utf-8') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')
print(config)