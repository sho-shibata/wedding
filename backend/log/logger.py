import json
from logging import getLogger, config

with open('log/config.json', 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)

# ここからはいつもどおり
def logger():
    logger = getLogger('debugLogger')
    return logger
