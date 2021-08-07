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
                    'set country "(' + common.common_regex.country_code + ')"\n',
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

            elif network_object_type == "interface-subnet":

                re_match = re.search(
                    "set subnet ("
                    + common.common_regex.ipv4_address
                    + ") ("
                    + common.common_regex.ipv4_mask
                    + ")\n",
                    network_object,
                )

                if re_match:  # if a subnet is found

                    network_object_network = re_match.group(
                        1
                    )  ### probably need to change this from interfaces IP address to subnets network address
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
                        "host"
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

            members = re_match.group(0)
            members = members.replace('set member "', "").rstrip().rstrip('"')

            network_group_members = members.split('" "')

            data["network_groups"][network_group_name][
                "members"
            ] = network_group_members

    # Parse IPv6 network groups

    logger.info(__name__ + ": parse IPv6 network groups")

    re_match = re.search(
        "\nconfig firewall addrgrp6\n(?:.*?)(?:\n)?end", src_config, re.DOTALL
    )

    if re_match:
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

                members = re_match.group(0)
                members = members.replace('set member "', "").rstrip().rstrip('"')

                network6_group_members = members.split('" "')

                data["network6_groups"][network6_group_name][
                    "members"
                ] = network6_group_members

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

            group_nets = []

            route["network"] = ""
            route["mask"] = ""
            route["gateway"] = ""
            route["interface"] = ""
            route["distance"] = ""
            route["blackhole"] = False
            route["type"] = "static"

            re_match_dst = re.search(
                "set dst ("
                + common.common_regex.ipv4_address
                + ") ("
                + common.common_regex.ipv4_mask
                + ")\n",
                route_config,
            )
            if re_match_dst:
                route["network"] = re_match_dst.group(1)
                route["mask"] = re_match_dst.group(2)
            else:
                route["network"] = "0.0.0.0"
                route["mask"] = "0.0.0.0"

            re_match_dstaddr = re.search('set dstaddr "(.*)"\n', route_config,)
            if re_match_dstaddr:
                route_addr = re_match_dstaddr.group(1)
                if route_addr in data["network_objects"]:
                    ### need to add support for more network object types - e.g. range etc
                    if data["network_objects"][route_addr]["type"] == "network":
                        route["network"] = data["network_objects"][route_addr][
                            "network"
                        ]
                        route["mask"] = data["network_objects"][route_addr]["mask"]
                    elif data["network_objects"][route_addr]["type"] == "host":
                        route["network"] = data["network_objects"][route_addr][
                            "network"
                        ]
                        route["mask"] = data["network_objects"][route_addr]["mask"]

                elif route_addr in data["network_groups"]:
                    group_nets = data["network_groups"][route_addr]["members"]

                else:
                    logger.info(
                        __name__
                        + ": parse static routes: could not find "
                        + route_addr
                        + " in parsed network objects"
                    )

            re_match_gwy = re.search(
                "set gateway ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})\n",
                route_config,
            )
            if re_match_gwy:
                route["gateway"] = re_match_gwy.group(1)

            re_match_int = re.search('set device "?(.*?)"?\n', route_config)
            if re_match_int:
                route["interface"] = re_match_int.group(1)

            re_match_bh = re.search("set blackhole enable\n", route_config)
            if re_match_bh:
                route["blackhole"] = True

            re_match_dist = re.search("set distance ([0-9]{1,})\n", route_config)
            if re_match_dist:
                route["distance"] = re_match_dist.group(1)

            route["source"] = []

            route["type"] = "static"

            if group_nets:
                for member in group_nets:
                    ### need to add support for more network object types - e.g. range etc
                    if data["network_objects"][member]["type"] == "network":
                        route["network"] = data["network_objects"][member]["network"]
                        route["mask"] = data["network_objects"][member]["mask"]
                    elif data["network_objects"][member]["type"] == "host":
                        route["network"] = data["network_objects"][member]["host"]
                        route["mask"] = data["network_objects"][member]["mask"]

                    data["routes"].append(dict(route))

            else:
                data["routes"].append(route)

    # Parse service objects

    logger.info(__name__ + ": parse service objects")

    re_match = re.search(
        "\nconfig firewall service custom\n(?:.*?)\nend", src_config, re.DOTALL
    )
    service_block = re_match.group(0).strip()

    for service_match in re.finditer(
        '    edit "([A-Za-z0-9-_]{1,})"\n(?:.*?)\n    next', service_block, re.DOTALL
    ):

        service_config = service_match.group(0)
        service_name = service_match.group(1)

        service = {}

        service["description"] = ""
        service["dst_port"] = ""
        service["protocol"] = ""
        service["src_port"] = ""
        service["type"] = ""

        re_match_comment = re.search('set comment "(.*)"\n', service_config,)
        if re_match_comment:
            service["description"] = re_match_comment.group(1)
        del re_match_comment

        re_match_protocol = re.search("set protocol (.*)\n", service_config,)
        if re_match_protocol and re_match_protocol.group(1) != "TCP/UDP/SCTP":
            protocol = re_match_protocol.group(1)

            if protocol == "IP":
                pass
            elif protocol == "ICMP":
                pass
            elif protocol == "ICMP6":
                pass

            data["service_objects"][service_name] = service

        else:
            re_match_portrange = re.search(
                "set (tcp|udp|sctp)-portrange (.*)\n", service_config,
            )
            if re_match_portrange:
                service["protocol"] = re_match_portrange.group(1)
                ports = re_match_portrange.group(2).split(" ")

                if len(ports) == 1:
                    dst_src_ports = ports[0].split(":")

                    service["dst_port"] = dst_src_ports[0]

                    if len(dst_src_ports) > 1:
                        service["src_port"] = dst_src_ports[1]

                    data["service_objects"][service_name] = service

                else:
                    members = []
                    for i, p in enumerate(ports):
                        sub_service_name = service_name + "_" + str(i + 1)

                        dst_src_ports = p.split(":")
                        service["dst_port"] = dst_src_ports[0]

                        if len(dst_src_ports) > 1:
                            service["src_port"] = dst_src_ports[1]

                        data["service_objects"][sub_service_name] = dict(service)
                        members.append(sub_service_name)

                    data["service_groups"][service_name] = {}
                    data["service_groups"][service_name]["type"] = "group"
                    data["service_groups"][service_name]["members"] = members

    # Parse service groups

    logger.info(__name__ + ": parse service groups")

    re_match = re.search(
        "\nconfig firewall service group\n(?:.*?)\nend", src_config, re.DOTALL
    )

    service_groups_block = re_match.group(0).strip()

    for service_group_match in re.finditer(
        '    edit "?(.*?)"?\n(?:.*?)?\n?    next', service_groups_block, re.DOTALL
    ):

        service_group = service_group_match.group(0)
        service_group_name = service_group_match.group(1)

        data["service_groups"][service_group_name] = {}

        data["service_groups"][service_group_name]["type"] = "group"

        re_match = re.search('set member(?: "?(?:.*?)"?){1,}\n', service_group)

        if re_match:

            members = re_match.group(0)
            members = members.replace('set member "', "").rstrip().rstrip('"')

            service_group_members = members.split('" "')

            data["service_groups"][service_group_name][
                "members"
            ] = service_group_members

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
