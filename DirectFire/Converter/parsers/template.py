#!/usr/bin/env python

# Import modules

import logger
import sys
from traceback_with_variables import prints_tb, LoggerAsFile

"""
Import any modules needed here
"""

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names

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


# Parser


def parse(src_config, routing_info=""):

    logger.info(__name__ + ": parser module started")

    # Initialise data

    """
    May need to process XML to ET, JSON etc here
    """

    # Initialise variables

    data = {}

    data["system"] = {}

    data["interfaces"] = {}
    data["zones"] = {}

    data["routes"] = []
    data["routes6"] = []

    data["network_objects"] = {}
    data["network6_objects"] = {}
    data["network_groups"] = {}
    data["network6_groups"] = {}

    data["service_objects"] = {}
    data["service_groups"] = {}

    data["policies"] = []

    data["nat"] = []

    # Parser specific variables

    """
    Parser specific variables
    """

    # Parse system

    logger.info(__name__ + ": parse system")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces")

    """
    Parse interfaces
    """

    # Parse zones

    logger.info(__name__ + ": parse zones")

    """
    Parse zones
    """

    # Parse static routes

    logger.info(__name__ + ": parse static routes")

    """
    Parse static routes
    """

    # Parse IPv4 network objects

    logger.info(__name__ + ": parse IPv4 network objects")

    """
    Parse IPv4 network objects
    """

    # Parse IPv6 network objects

    logger.info(__name__ + ": parse IPv6 network objects")

    """
    Parse IPv6 network objects
    """

    # Parse IPv4 network groups

    logger.info(__name__ + ": parse IPv4 network groups")

    """
    Parse IPv4 network groups
    """

    # Parse IPv6 network groups

    logger.info(__name__ + ": parse IPv6 network groups")

    """
    Parse IPv6 network groups
    """

    # Parse service objects

    logger.info(__name__ + ": parse service objects")

    """
    Parse service objects
    """

    # Parse service groups

    logger.info(__name__ + ": parse service groups")

    """
    Parse service groups
    """

    # Parse firewall policies

    logger.info(__name__ + ": parse firewall policies")

    """
    Parse firewall policies
    """

    # Parse NAT

    logger.info(__name__ + ": parse NAT")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.info(__name__ + ": parser module finished")

    return data
