#!/usr/bin/env python

# Import modules

import logging
import re
import sys


# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

"""
Initialise common functions here
"""

# Initiate logging

logger = logging.getLogger(__name__)

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

    # Predefined service objects

    predefined_services = {}

    def _add_predefined_service(
        description, dst_ports, name, protocols, src_ports, timeout, type,
    ):
        predefined_services[name] = {}
        predefined_services[name]["description"] = description
        predefined_services[name]["dst_ports"] = dst_ports
        predefined_services[name]["protocols"] = protocols
        predefined_services[name]["src_ports"] = src_ports
        predefined_services[name]["timeout"] = timeout
        predefined_services[name]["type"] = type

    _add_predefined_service(
        description="",
        dst_ports=[],
        name="ANY",
        protocols=["0"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[],
        timeout="",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["5190-5194"],
        name="AOL",
        protocols=["6"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="1800",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["5678"],
        name="APPLE-ICHAT-SNATMAP",
        protocols=["17"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="60",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["179"],
        name="BGP",
        protocols=["6"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="1800",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["19"],
        name="CHARGEN",
        protocols=["6", "17"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="60",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["67", "68"],
        name="DHCP-Relay",
        protocols=["17"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="60",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["9"],
        name="DISCARD",
        protocols=["6", "17"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="60",  # seconds
        type="v2",
    )

    _add_predefined_service(
        description="",
        dst_ports=["53"],
        name="DNS",
        protocols=["6", "17"],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
        src_ports=[""],
        timeout="60",  # seconds
        type="v2",
    )

    # _add_predefined_service(
    #     description="DESCRIPTION",
    #     dst_ports=[""],
    #     name="NAME",
    #     protocols=["6", "17"], # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
    #     src_ports=[""],
    #     timeout="", # seconds
    #     type="v2",
    # )

    # Parse system

    logger.info(__name__ + ": parse system")

    re_hostname = re.search("^set hostname (.*?)$", src_config, re.MULTILINE)

    if re_hostname:
        data["system"]["hostname"] = re_hostname.group(1)

    logger.info(__name__ + ": parse system - domain")

    re_domain = re.search("^set domain (.*?)$", src_config, re.MULTILINE)

    if re_domain:
        data["system"]["domain"] = re_domain.group(1)

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces")

    ## physical interfaces and sub interfaces

    interfaces_config = {}

    for re_interface in re.finditer(
        "^set interface (.*?) (.*?)$", src_config, re.MULTILINE
    ):

        interface_name = re_interface.group(1).replace('"', "")

        if interface_name not in interfaces_config:
            interfaces_config[interface_name] = []

        interfaces_config[interface_name].append(re_interface.group(2))

        if interface_name not in data["interfaces"]:
            data["interfaces"][interface_name] = {}
            data["interfaces"][interface_name]["enabled"] = True
            data["interfaces"][interface_name]["description"] = ""
            data["interfaces"][interface_name]["ipv4_config"] = []
            data["interfaces"][interface_name]["ipv6_config"] = []
            data["interfaces"][interface_name]["physical_interfaces"] = []
            data["interfaces"][interface_name]["type"] = "interface"
            data["interfaces"][interface_name]["vlan_id"] = ""
            data["interfaces"][interface_name]["vlan_name"] = ""

    for interface in data["interfaces"]:
        if "disable" in interfaces_config[interface]:
            data["interfaces"][interface]["enabled"] = False

    # Parse zones

    logger.info(__name__ + ": parse zones")

    zones_config = {}

    for re_zone in re.finditer(
        '^set zone(?: id [0-9]{1,})? "(.*?)"(?: (.*?))?$', src_config, re.MULTILINE
    ):

        zone_name = re_zone.group(1)

        if zone_name not in zones_config:
            zones_config[zone_name] = []

        zones_config[zone_name].append(re_zone.group(2))

        if zone_name not in data["zones"]:
            data["zones"][zone_name] = {}
            data["zones"][zone_name]["allow_intrazone"] = True
            data["zones"][zone_name]["description"] = ""
            data["zones"][zone_name]["enabled"] = True
            data["zones"][zone_name]["members"] = []

    for zone in data["zones"]:
        if "block" in zones_config[zone]:
            data["zones"][zone_name]["allow_intrazone"] = False

    for interface in data["interfaces"]:
        for str in interfaces_config[interface]:
            if "zone " in str:
                re_zone = re.search('zone "(.*?)"', str)
                zone_name = re_zone.group(1)
                data["zones"][zone_name]["members"].append(interface)

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
