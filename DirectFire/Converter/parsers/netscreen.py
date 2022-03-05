#!/usr/bin/env python

# Import modules

import csv
import logging
import re
import sys


# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

common.common_regex()
ipv4_prefix_to_mask = common.ipv4_prefix_to_mask

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

    def _add_service_object(
        description, dst_ports, name, protocols, src_ports, timeout, type,
    ):
        data["service_objects"][name] = {}
        data["service_objects"][name]["description"] = description
        data["service_objects"][name]["dst_ports"] = dst_ports
        data["service_objects"][name]["protocols"] = protocols
        data["service_objects"][name]["src_ports"] = src_ports
        data["service_objects"][name]["timeout"] = timeout
        data["service_objects"][name]["type"] = type

    filepath_predefined_services = (
        f"{settings.BASE_DIR}/resources/netscreen/predefined_services.csv"
    )

    with open(filepath_predefined_services, newline="") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:

            if row[1] != "RPC":

                name = row[0]
                dst_ports = row[2]
                dst_ports = dst_ports.replace("/", "-")
                protocols = row[1]
                timeout = "" if row[4] == "default" else int(row[4]) * 60

                _add_service_object(
                    description="",
                    dst_ports=[dst_ports],
                    name=name,
                    protocols=[protocols],  # ANY: 0, ICMP: 1, TCP: 6, UDP: 17
                    src_ports=[],
                    timeout=timeout,  # seconds
                    type="v2",
                )

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

        interface = re_interface.group(1).replace('"', "")

        if interface not in interfaces_config:
            interfaces_config[interface] = []

        interfaces_config[interface].append(re_interface.group(2))

        if interface not in data["interfaces"]:
            data["interfaces"][interface] = {}
            data["interfaces"][interface]["enabled"] = True
            data["interfaces"][interface]["description"] = ""
            data["interfaces"][interface]["ipv4_config"] = []
            data["interfaces"][interface]["ipv6_config"] = []
            data["interfaces"][interface]["physical_interfaces"] = []
            data["interfaces"][interface]["type"] = "interface"
            data["interfaces"][interface]["vlan_id"] = ""
            data["interfaces"][interface]["vlan_name"] = ""

    for interface in data["interfaces"]:
        if "disable" in interfaces_config[interface]:
            data["interfaces"][interface]["enabled"] = False

        if "." in interface:
            phys_interface = interface.split(".")
            data["interfaces"][interface]["physical_interfaces"].append(
                phys_interface[0]
            )
            data["interfaces"][interface]["type"] = "subinterface"

        if "vlan" in interface:
            data["interfaces"][interface]["type"] = "vlan"

    ## find interface description

    for re_description in re.finditer(
        "^set interface (.*?) description (.*?)$", src_config, re.MULTILINE,
    ):
        interface = re_description.group(1).replace('"', "")
        data["interfaces"][interface]["description"] = re_description.group(2)

    ## find interface ipv4 configurations

    for re_ipv4 in re.finditer(
        "^set interface (.*?) ip ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ")$",
        src_config,
        re.MULTILINE,
    ):
        interface = re_ipv4.group(1).replace('"', "")
        ipv4 = {}
        ipv4["ip_address"] = re_ipv4.group(2)
        ipv4["mask"] = ipv4_prefix_to_mask(re_ipv4.group(3))
        data["interfaces"][interface]["ipv4_config"].append(ipv4)

    ## find interface ipv6 configurations

    for re_ipv6 in re.finditer(
        "^set interface (.*?) ipv6 ip ("
        + common.common_regex.ipv6_address
        + ")("
        + common.common_regex.ipv6_mask
        + ")$",
        src_config,
        re.MULTILINE,
    ):
        interface = re_ipv6.group(1).replace('"', "")
        ipv6 = {}
        ipv6["ip_address"] = re_ipv6.group(2)
        ipv6["mask"] = re_ipv6.group(3)
        data["interfaces"][interface]["ipv6_config"].append(ipv6)

    ## find interface vlan tag configurations

    for re_vlan_id in re.finditer(
        "^set interface (.*?) tag (" + common.common_regex.vlan_id + ")",
        src_config,
        re.MULTILINE,
    ):
        interface = re_vlan_id.group(1).replace('"', "")
        data["interfaces"][interface]["vlan_id"] = re_vlan_id.group(2)

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

    ## check if intrazone traffic is blocked

    for zone in data["zones"]:
        if "block" in zones_config[zone]:
            data["zones"][zone_name]["allow_intrazone"] = False

    ## find zone interface members

    for interface in data["interfaces"]:
        for string in interfaces_config[interface]:
            if "zone " in string:
                re_zone = re.search('zone "(.*?)"', string)
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
