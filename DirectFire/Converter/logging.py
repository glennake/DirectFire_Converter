#!/usr/bin/env python

# Import modules

try:
    from datetime import datetime
except:
    raise ImportError("Could not import module: datetime")

try:
    import logging
except:
    raise ImportError("Could not import module: logging")

# Import settings

import DirectFire.Converter.settings as settings


class logger:
    def __init__(self, src_format, dst_format):

        now = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

        logging.basicConfig(
            filename="logs/"
            + now
            + "_"
            + str(src_format)
            + "_"
            + str(dst_format)
            + ".log",
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )

    def log(self, log_level, message):

        if log_level >= settings.LOG_LEVEL:  # If log level ge log setting continue

            if log_level == 1:  ## debug

                logging.debug(message)

            elif log_level == 2:  ## info

                logging.info(message)

            elif log_level == 3:  ## warning

                logging.warning(message)

            elif log_level == 4:  ## error

                logging.error(message)

            elif log_level == 5:  ## critical

                logging.critical(message)

            elif log_level == 6:  ## exception

                logging.exception(message)
