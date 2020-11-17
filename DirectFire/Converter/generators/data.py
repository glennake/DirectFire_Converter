#!/usr/bin/env python

# Import modules

import logging
import sys
from traceback_with_variables import prints_tb, LoggerAsFile

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


# Catch exceptions and log


@prints_tb(
    file_=LoggerAsFile(logger),
    num_context_lines=3,
    max_value_str_len=9999999,
    max_exc_str_len=9999999,
)
def catch_exception(exc_type, exc_value, exc_trace):

    sys.__excepthook__(exc_type, exc_value, exc_trace)


sys.excepthook = catch_exception


# Generator


@prints_tb(
    file_=LoggerAsFile(logger),
    num_context_lines=3,
    max_value_str_len=9999999,
    max_exc_str_len=9999999,
)
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
