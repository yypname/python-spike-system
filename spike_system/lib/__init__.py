import logging
from logging import handlers

rf_handler = handlers.TimedRotatingFileHandler(
    'redis.log', when='midnight', interval=1, backupCount=7)
rf_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(filename)s line:%(lineno)d [%(levelname)s] %(message)s")
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(rf_handler)

