from dataclasses import replace

from . import dev

config = replace(dev.config)
config.TESTING = True
config.PAGE_SIZE = 5
