#!/usr/bin/env python

# Import modules

"""
Import any modules needed here
"""

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

    # Generate system

    logger.log(2, __name__ + ": generate system")

    """
    Generate system objects such as hostname, DNS
    """

    # Generate routes

    logger.log(2, __name__ + ": generate routes")

    """
    Generate static routes
    """

    # Generate address objects

    logger.log(2, __name__ + ": generate address objects")

    """
    Generate address objects
    """

    # Generate address groups

    """
    Generate address groups
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

    logger.log(2, __name__ + ": generate policies - not yet supported")

    """
    Generate firewall policies
    """

    # Generate NAT

    logger.log(2, __name__ + ": generate NAT ")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
