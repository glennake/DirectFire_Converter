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

cleanse_names = common.cleanse_names


def parse(logger, src_config):

    logger.log(2, __name__ + ": parser module started")

    # Initialise data

    """
    May need to process XML to ET, JSON etc here
    """

    # Initialise variables

    data = {}

    data["system"] = {}
    data["interfaces"] = {}
    data["zones"] = {}
    data["routes"] = {}

    data["network_objects"] = {}
    data["network6_objects"] = {}
    data["network_groups"] = {}

    data["service_objects"] = {}
    data["service_groups"] = {}

    data["policies"] = {}

    data["nat"] = {}

    route_id = 1
    policy_id = 1
    nat_id = 1

    # Parse system

    logger.log(2, __name__ + ": parse system")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse routes

    logger.log(2, __name__ + ": parse routes")

    """
    Parse static routes
    """

    # Parse address objects

    logger.log(2, __name__ + ": parse address objects")

    """
    Parse address objects
    """

    # Parse address groups

    logger.log(2, __name__ + ": parse address groups")

    """
    Parse address groups
    """

    # Parse service objects

    logger.log(2, __name__ + ": parse service objects")

    """
    Parse service objects
    """

    # Parse service groups

    logger.log(2, __name__ + ": parse service groups")

    """
    Parse service groups
    """

    # Parse policies

    logger.log(2, __name__ + ": parse policies")

    """
    Parse firewall policies
    """

    # Parse NAT

    logger.log(2, __name__ + ": parse NAT")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
