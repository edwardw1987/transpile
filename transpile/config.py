import os

curdir = os.path.dirname(__file__)

templates_dir = os.path.join(curdir, "templates")

class _Settings(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

settings = _Settings()