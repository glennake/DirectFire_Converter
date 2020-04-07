#!/usr/bin/env python

# Import modules

import re

# Import common, logging and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
common.common_regex()
ipv4_prefix_to_mask = common.ipv4_prefix_to_mask


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

    re_match = re.search("(set system host-name (.*?)\n)", src_config)

    if re_match:
        data["system"]["hostname"] = re_match.group(1)

    # Parse interfaces

    """
    Parse interfaces
    """

    # Parse zones

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    for re_match in re.finditer(
        "set routing-options static route ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ") next-hop ("
        + common.common_regex.ipv4_address
        + ")",
        src_config,
    ):

        data["routes"][route_id] = {}

        data["routes"][route_id]["network"] = re_match.group(1)
        data["routes"][route_id]["mask"] = ipv4_prefix_to_mask(re_match.group(2))
        data["routes"][route_id]["gateway"] = re_match.group(3)
        data["routes"][route_id]["distance"] = ""  ### need to parse distance
        data["routes"][route_id]["type"] = "static"

        route_id += 1

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
