# settings.py
import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'polls.yaml'


def get_config(path):
    with open(path) as f:
        result = yaml.load(f)
    return result


config = get_config(config_path)
print("config: {}".format(config))
