#!/usr/bin/env python

# Import modules

import logging
import sys
from traceback_with_variables import prints_tb, LoggerAsFile

"""
Import any modules needed here
"""

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


def generate(parsed_data):

    logger.info(__name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generator specific variables

    """
    Generator specific variables
    """

    # Generate system

    logger.info(__name__ + ": generate system")

    """
    Generate system objects such as hostname, DNS
    """

    # Generate interfaces

    logger.info(__name__ + ": generate interfaces")

    """
    Generate interfaces
    """

    # Generate zones

    logger.info(__name__ + ": generate zones")

    """
    Generate zones
    """

    # Generate static routes

    logger.info(__name__ + ": generate static routes")

    """
    Generate static routes
    """

    # Generate network objects

    logger.info(__name__ + ": generate network objects")

    """
    Generate network objects
    """

    # Generate network groups

    logger.info(__name__ + ": generate network groups")

    """
    Generate network groups
    """

    # Generate service objects

    logger.info(__name__ + ": generate service objects")

    """
    Generate service objects
    """

    # Generate service groups

    logger.info(__name__ + ": generate service groups")

    """
    Generate service groups
    """

    # Generate policies

    logger.info(__name__ + ": generate policies")

    """
    Generate firewall policies
    """

    # Generate NAT

    logger.info(__name__ + ": generate NAT")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.info(__name__ + ": generator module finished")

    return dst_config
