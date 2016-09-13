import logging
import logging.config
import os

from scruffy import ConfigFile, File, PackageDirectory
from .main import main

config = ConfigFile('~/.thespomat.conf', defaults=File('config/default.cfg', parent=PackageDirectory()), apply_env=True)
config.load()
