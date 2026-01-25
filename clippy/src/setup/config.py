config = {}

def set(key, value):
    config[key] = value

def get(key, default=None):
    return config.get(key, default)