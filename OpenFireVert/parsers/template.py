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


def parse(logger, src_config, routing_info=""):

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
    data["routes6"] = {}

    data["network_objects"] = {}
    data["network6_objects"] = {}
    data["network_groups"] = {}
    data["network6_groups"] = {}

    data["service_objects"] = {}
    data["service_groups"] = {}

    data["policies"] = {}

    data["nat"] = {}

    route_id = 1
    route6_id = 1
    policy_id = 1
    nat_id = 1

    # Parse system

    logger.log(2, __name__ + ": parse system")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse interfaces

    logger.log(2, __name__ + ": parse interfaces")

    """
    Parse interfaces
    """

    # Parse zones

    logger.log(2, __name__ + ": parse zones")

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    """
    Parse static routes
    """

    # Parse IPv4 network objects

    logger.log(2, __name__ + ": parse IPv4 network objects")

    """
    Parse IPv4 network objects
    """

    # Parse IPv6 network objects

    logger.log(2, __name__ + ": parse IPv6 network objects")

    """
    Parse IPv6 network objects
    """

    # Parse IPv4 network groups

    logger.log(2, __name__ + ": parse IPv4 network groups")

    """
    Parse IPv4 network groups
    """

    # Parse IPv6 network groups

    logger.log(2, __name__ + ": parse IPv6 network groups")

    """
    Parse IPv6 network groups
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

    # Parse firewall policies

    logger.log(2, __name__ + ": parse firewall policies")

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
