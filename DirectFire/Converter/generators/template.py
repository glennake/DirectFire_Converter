#!/usr/bin/env python

# Import modules

"""
Import any modules needed here
"""

# Import common, logging and settings

import DirectFire.Converter.common as common
from DirectFire.Converter.logging import logger
import DirectFire.Converter.settings as settings

# Initialise common functions

"""
Import any common functions needed here
"""


def generate(logger, parsed_data):

    logger.log(2, __name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generator specific variables

    """
    Generator specific variables
    """

    # Generate system

    logger.log(2, __name__ + ": generate system")

    """
    Generate system objects such as hostname, DNS
    """

    # Generate interfaces

    logger.log(2, __name__ + ": generate interfaces")

    """
    Generate interfaces
    """

    # Generate zones

    logger.log(2, __name__ + ": generate zones")

    """
    Generate zones
    """

    # Generate static routes

    logger.log(2, __name__ + ": generate static routes")

    """
    Generate static routes
    """

    # Generate network objects

    logger.log(2, __name__ + ": generate network objects")

    """
    Generate network objects
    """

    # Generate network groups

    logger.log(2, __name__ + ": generate network groups")

    """
    Generate network groups
    """

    # Generate service objects

    logger.log(2, __name__ + ": generate service objects")

    """
    Generate service objects
    """

    # Generate service groups

    logger.log(2, __name__ + ": generate service groups")

    """
    Generate service groups
    """

    # Generate policies

    logger.log(2, __name__ + ": generate policies")

    """
    Generate firewall policies
    """

    # Generate NAT

    logger.log(2, __name__ + ": generate NAT")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
