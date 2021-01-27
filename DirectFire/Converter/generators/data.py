#!/usr/bin/env python

# Import modules

import logging
import sys

import json

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

"""
Import any common functions needed here
"""

# Initiate logging

logger = logging.getLogger(__name__)

# Generator

def generate(parsed_data):

    logger.info(__name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generator specific variables

    """
    Generator specific variables
    """

    # Generate data

    logger.info(__name__ + ": generate data")

    formatted_data = json.dumps(parsed_data, indent=2)
    dst_config.append(formatted_data)

    # Return generated data

    logger.info(__name__ + ": generator module finished")

    return dst_config
