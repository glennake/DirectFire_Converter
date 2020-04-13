#!/usr/bin/env python

# Import modules

import json

# Import common, logging and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Initialise common functions

"""
Import any common functions needed here
"""


def generate(logger, parsed_data):

    logger.log(2, __name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generate data

    logger.log(2, __name__ + ": generate data")

    formatted_data = json.dumps(parsed_data, indent=2)
    dst_config.append(formatted_data)

    # Return generated data

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
