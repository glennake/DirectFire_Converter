#!/usr/bin/env python

# Import modules

import logging
import sys

import re

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
common.common_regex()

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

    # Parse system

    logger.info(__name__ + ": parse system")

    re_match = re.search('(?:set hostname "(.*?)"\n)', src_config)
    data["system"]["hostname"] = re_match.group(1)

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces - not yet supported")

    """
    Parse interfaces
    """

    # Parse zones

    logger.info(__name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.info(__name__ + ": parse static routes")

    re_match = re.search("\nconfig router static\n(?:.*?)\nend", src_config, re.DOTALL)
    routes_block = re_match.group(0).strip()

    for route_match in re.finditer(
        "    edit [0-9]{1,}\n(?:.*?)\n    next", routes_block, re.DOTALL
    ):

        route_config = route_match.group(0)

        if (
            "set virtual-wan-link enable" not in route_config
        ):  ### need to add vwl support

            route = {}

            re_match = re.search(
                "set dst ("
                + common.common_regex.ipv4_address
                + ") ("
                + common.common_regex.ipv4_mask
                + ")\n",
                route_config,
            )

            route["network"] = re_match.group(1)
            route["mask"] = re_match.group(2)

            re_match = re.search(
                "set gateway ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})\n",
                route_config,
            )

            route["gateway"] = re_match.group(1)

            re_match = re.search('set device "?(.*?)"?\n', route_config)
            route["interface"] = re_match.group(1)

            re_match = re.search("set distance ([0-9]{1,})\n", route_config)
            route["distance"] = re_match.group(1)

            route["source"] = []

            route["type"] = "static"

            data["routes"].append(route)

    # Parse IPv4 network objects

    logger.info(__name__ + ": parse IPv4 network objects")

    re_match = re.search(
        "\nconfig firewall address\n(?:.*?)\nend", src_config, re.DOTALL
    )

    network_objects_block = re_match.group(0).strip()

    for network_object_match in re.finditer(
        '    edit "?(.*?)"?\n(?:.*?)?\n?    next', network_objects_block, re.DOTALL
    ):

        network_object = network_object_match.group(0)
        network_object_name = network_object_match.group(1)

        data["network_objects"][network_object_name] = {}

        re_match = re.search("set type (.*?)\n", network_object)

        if re_match:

            network_object_type = re_match.group(1)

            if network_object_type == "fqdn":

                data["network_objects"][network_object_name]["type"] = "fqdn"

                re_match = re.search(
                    'set fqdn "?(' + common.common_regex.fqdn + ')"?\n', network_object
                )

                data["network_objects"][network_object_name]["fqdn"] = re_match.group(1)

            elif network_object_type == "geography":

                data["network_objects"][network_object_name]["type"] = "geography"

                re_match = re.search(
                    "set country (" + common.common_regex.country_code + ")\n",
                    network_object,
                )

                data["network_objects"][network_object_name][
                    "country_code"
                ] = re_match.group(1)

            elif network_object_type == "ipmask":

                re_match = re.search(
                    "set subnet ("
                    + common.common_regex.ipv4_address
                    + ") ("
                    + common.common_regex.ipv4_mask
                    + ")\n",
                    network_object,
                )

                if re_match:  # if a subnet is found

                    network_object_network = re_match.group(1)
                    network_object_mask = re_match.group(2)

                    if (
                        network_object_mask == "255.255.255.255"
                    ):  # if mask is 255.255.255.255 then its a host

                        data["network_objects"][network_object_name]["type"] = "host"
                        data["network_objects"][network_object_name][
                            "network"
                        ] = network_object_network
                        data["network_objects"][network_object_name][
                            "mask"
                        ] = network_object_mask

                    else:  # else its a network

                        data["network_objects"][network_object_name]["type"] = "network"
                        data["network_objects"][network_object_name][
                            "network"
                        ] = network_object_network
                        data["network_objects"][network_object_name][
                            "mask"
                        ] = network_object_mask

                else:  # default is 0.0.0.0 0.0.0.0

                    network_object_network = re_match.group(1)
                    network_object_mask = re_match.group(2)

                    data["network_objects"][network_object_name]["type"] = "network"
                    data["network_objects"][network_object_name][
                        "network"
                    ] = network_object_network
                    data["network_objects"][network_object_name][
                        "mask"
                    ] = network_object_mask

            elif network_object_type == "iprange":

                data["network_objects"][network_object_name]["type"] = "range"

                re_match = re.search(
                    "set start-ip (" + common.common_regex.ipv4_address + ")\n",
                    network_object,
                )

                data["network_objects"][network_object_name][
                    "address_first"
                ] = re_match.group(1)

                re_match = re.search(
                    "set end-ip (" + common.common_regex.ipv4_address + ")\n",
                    network_object,
                )

                data["network_objects"][network_object_name][
                    "address_last"
                ] = re_match.group(1)

            elif network_object_type == "mac":

                data["network_objects"][network_object_name]["type"] = "mac"

                re_match = re.search(
                    "set start-mac (" + common.common_regex.mac_address + ")\n",
                    network_object,
                )

                data["network_objects"][network_object_name][
                    "mac_first"
                ] = re_match.group(1)

                re_match = re.search(
                    "set end-mac (" + common.common_regex.mac_address + ")\n",
                    network_object,
                )

                data["network_objects"][network_object_name][
                    "mac_last"
                ] = re_match.group(1)

            ### add support for other types - dynamic, interface-subnet, wildcard

        else:  # default type is ipmask

            re_match = re.search(
                "set subnet ("
                + common.common_regex.ipv4_address
                + ") ("
                + common.common_regex.ipv4_mask
                + ")\n",
                network_object,
            )

            if re_match:  # if a subnet is found

                network_object_network = re_match.group(1)
                network_object_mask = re_match.group(2)

                if (
                    network_object_network != "0.0.0.0"
                    and network_object_mask == "255.255.255.255"
                ):  # if mask is 255.255.255.255 then its a host

                    data["network_objects"][network_object_name]["type"] = "host"
                    data["network_objects"][network_object_name][
                        "network"
                    ] = network_object_network
                    data["network_objects"][network_object_name][
                        "mask"
                    ] = network_object_mask

                else:  # else its a network

                    data["network_objects"][network_object_name]["type"] = "network"
                    data["network_objects"][network_object_name][
                        "network"
                    ] = network_object_network
                    data["network_objects"][network_object_name][
                        "mask"
                    ] = network_object_mask

            else:  # default is 0.0.0.0 0.0.0.0

                data["network_objects"][network_object_name]["type"] = "network"
                data["network_objects"][network_object_name]["network"] = "0.0.0.0"
                data["network_objects"][network_object_name]["mask"] = "0.0.0.0"

    # Parse IPv6 network objects

    logger.info(__name__ + ": parse IPv6 network objects")

    re_match = re.search(
        "\nconfig firewall address6\n(?:.*?)\nend", src_config, re.DOTALL
    )

    network6_objects_block = re_match.group(0).strip()

    for network6_object_match in re.finditer(
        '    edit "?(.*?)"?\n(?:.*?)?\n?    next', network6_objects_block, re.DOTALL
    ):

        network6_object = network6_object_match.group(0)
        network6_object_name = network6_object_match.group(1)

        data["network6_objects"][network6_object_name] = {}

        re_match = re.search("set type (.*?)\n", network6_object)

        if re_match:

            network6_object_type = re_match.group(1)

            if network6_object_type == "fqdn":

                data["network6_objects"][network6_object_name]["type"] = "fqdn"

                re_match = re.search(
                    'set fqdn "?(' + common.common_regex.fqdn + ')"?\n', network6_object
                )

                data["network6_objects"][network6_object_name]["fqdn"] = re_match.group(
                    1
                )

            elif network6_object_type == "ipprefix":

                re_match = re.search(
                    "set ip6 ("
                    + common.common_regex.ipv6_address
                    + ")("
                    + common.common_regex.ipv6_mask
                    + ")\n",
                    network6_object,
                )

                if re_match:  # if a subnet is found

                    network6_object_network = re_match.group(1)
                    network6_object_mask = re_match.group(2)

                    data["network6_objects"][network6_object_name]["type"] = "network"
                    data["network6_objects"][network6_object_name][
                        "network"
                    ] = network6_object_network
                    data["network6_objects"][network6_object_name][
                        "mask"
                    ] = network6_object_mask

                else:  # ::/0 is default

                    data["network6_objects"][network6_object_name]["type"] = "network"
                    data["network6_objects"][network6_object_name]["network"] = "::"
                    data["network6_objects"][network6_object_name]["mask"] = "/0"

            elif network6_object_type == "iprange":

                data["network6_objects"][network6_object_name]["type"] = "range"

                re_match = re.search(
                    "set start-ip (" + common.common_regex.ipv6_address + ")\n",
                    network6_object,
                )

                data["network6_objects"][network6_object_name][
                    "address_first"
                ] = re_match.group(1)

                re_match = re.search(
                    "set end-ip (" + common.common_regex.ipv6_address + ")\n",
                    network6_object,
                )

                data["network6_objects"][network6_object_name][
                    "address_last"
                ] = re_match.group(1)

            ### add support for other types - dynamic, template

        else:  # default type is ipprefix

            re_match = re.search(
                "set ip6 ("
                + common.common_regex.ipv6_address
                + ")("
                + common.common_regex.ipv6_mask
                + ")\n",
                network6_object,
            )

            if re_match:  # if a subnet is found

                network6_object_network = re_match.group(1)
                network6_object_mask = re_match.group(2)

                data["network6_objects"][network6_object_name]["type"] = "network"
                data["network6_objects"][network6_object_name][
                    "network"
                ] = network6_object_network
                data["network6_objects"][network6_object_name][
                    "mask"
                ] = network6_object_mask

            else:  # ::/0 is default

                data["network6_objects"][network6_object_name]["type"] = "network"
                data["network6_objects"][network6_object_name]["network"] = "::"
                data["network6_objects"][network6_object_name]["mask"] = "/0"

    # Parse IPv4 network groups

    logger.info(__name__ + ": parse IPv4 network groups")

    re_match = re.search(
        "\nconfig firewall addrgrp\n(?:.*?)\nend", src_config, re.DOTALL
    )

    network_groups_block = re_match.group(0).strip()

    for network_group_match in re.finditer(
        '    edit "?(.*?)"?\n(?:.*?)?\n?    next', network_groups_block, re.DOTALL
    ):

        network_group = network_group_match.group(0)
        network_group_name = network_group_match.group(1)

        data["network_groups"][network_group_name] = {}

        data["network_groups"][network_group_name]["type"] = "group"

        re_match = re.search('set member(?: "?(?:.*?)"?){1,}\n', network_group)

        if re_match:

            network_group_members = (
                re_match.group(0)
                .replace("set member ", "")
                .replace('"', "")
                .rstrip()
                .split(" ")
            )

            data["network_groups"][network_group_name][
                "members"
            ] = network_group_members

    # Parse IPv6 network groups

    logger.info(__name__ + ": parse IPv6 network groups")

    re_match = re.search(
        "\nconfig firewall addrgrp6\n(?:.*?)(?:\n)?end", src_config, re.DOTALL
    )

    network6_groups_block = re_match.group(0).strip()

    for network6_group_match in re.finditer(
        '    edit "?(.*?)"?\n(?:.*?)?\n?    next', network6_groups_block, re.DOTALL
    ):

        network6_group = network6_group_match.group(0)
        network6_group_name = network6_group_match.group(1)

        data["network6_groups"][network6_group_name] = {}

        data["network6_groups"][network6_group_name]["type"] = "group"

        re_match = re.search('set member(?: "?(?:.*?)"?){1,}\n', network6_group)

        if re_match:

            network6_group_members = (
                re_match.group(0)
                .replace("set member ", "")
                .replace('"', "")
                .rstrip()
                .split(" ")
            )

            data["network6_groups"][network6_group_name][
                "members"
            ] = network6_group_members

    # Parse service objects

    logger.info(__name__ + ": parse service objects - not yet supported")

    """
    Parse service objects
    """

    # Parse service groups

    logger.info(__name__ + ": parse service groups - not yet supported")

    """
    Parse service groups
    """

    # Parse firewall policies

    logger.info(__name__ + ": parse firewall policies - not yet supported")

    """
    Parse firewall policies
    """

    # Parse NAT

    logger.info(__name__ + ": parse NAT - not yet supported")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.info(__name__ + ": parser module finished")

    return data
