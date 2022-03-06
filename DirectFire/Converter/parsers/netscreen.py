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

    # Predefined network objects

    data["service_objects"]["ANY"] = {"type": "any"}
    data["service_objects"]["ANY-IPv4"] = {"type": "any"}
    data["service_objects"]["Any-IPv4"] = {"type": "any"}
    data["service_objects"]["ANY-IPv6"] = {"type": "any"}
    data["service_objects"]["Any-IPv6"] = {"type": "any"}

    # Predefined service objects

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
                protocol = row[1]
                timeout = "" if row[4] == "default" else int(row[4]) * 60

                if protocol in ["6", "17"]:
                    if name not in data["service_objects"]:
                        data["service_objects"][name] = {
                            "description": "",
                            "dst_ports": [dst_ports],
                            "protocols": [protocol],
                            "src_ports": [],
                            "timeout": timeout,
                            "type": "v2",
                        }
                    else:
                        data["service_objects"][name]["dst_ports"].append(dst_ports)

                elif protocol == "1":
                    data["service_objects"][name] = {
                        "description": "",
                        "icmp_code": row[6],  ### should this be a list of codes
                        "icmp_type": row[7],  ### should this be a list of types
                        "protocols": [protocol],
                        "timeout": timeout,
                        "type": "v2",
                    }

                else:
                    data["service_objects"][name] = {
                        "description": "",
                        "protocols": [protocol],
                        "timeout": timeout,
                        "type": "v2",
                    }

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

    for re_static_route in re.finditer(
        "^set route ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ") interface (.*?)(?: gateway ("
        + common.common_regex.ipv4_address
        + "))?(?: preference ([0-9]{1,3}))?$",
        src_config,
        re.MULTILINE,
    ):  ## add support for vrouter? e.g. set vrouter untrust-vr route ...

        route_prefix = re_static_route.group(2)

        route = {
            "blackhole": False,
            "description": "",
            "distance": re_static_route.group(5) or "20",
            "enabled": True,
            "gateway": re_static_route.group(4) or "",
            "interface": re_static_route.group(3),
            "mask": ipv4_prefix_to_mask(route_prefix),
            "network": re_static_route.group(1),
            "type": "static",
        }

        if route["interface"] == "null":
            route["blackhole"] = True

        data["routes"].append(route)

    # Parse IPv4 network objects

    logger.info(__name__ + ": parse IPv4 network objects")

    for re_address in re.finditer(
        "^set address (.*?) (.*?) ("
        + common.common_regex.ipv4_address
        + ") ("
        + common.common_regex.ipv4_mask
        + ")$",
        src_config,
        re.MULTILINE,
    ):

        zone = re_address.group(1).replace('"', "")
        obj_name = re_address.group(2).replace('"', "")
        network = re_address.group(3)
        mask = re_address.group(4)

        net_obj = {
            "description": "",
            "interface": "",
            "type": "network",
        }

        if mask == "255.255.255.255":

            net_obj["host"] = network
            net_obj["type"] = "host"

        else:

            net_obj["mask"] = mask
            net_obj["network"] = network

        data["network_objects"][obj_name] = net_obj

    for re_address in re.finditer(
        "^set address (.*?) (.*?) (" + common.common_regex.fqdn + ")$",
        src_config,
        re.MULTILINE,
    ):

        zone = re_address.group(1).replace('"', "")
        obj_name = re_address.group(2).replace('"', "")
        fqdn = re_address.group(3)

        net_obj = {
            "description": "",
            "interface": "",
            "type": "fqdn",
        }

        net_obj["fqdn"] = fqdn

        data["network_objects"][obj_name] = net_obj

    # Parse IPv6 network objects

    logger.info(__name__ + ": parse IPv6 network objects - not yet supported")

    """
    Parse IPv6 network objects
    """

    # Parse IPv4 network groups

    logger.info(__name__ + ": parse IPv4 network groups")

    for re_group in re.finditer(
        "^set group address (.*?) (.*?) add (.*?)$", src_config, re.MULTILINE,
    ):

        zone = re_group.group(1).replace('"', "")
        obj_name = re_group.group(2).replace('"', "")
        member = re_group.group(3).replace('"', "")

        if obj_name not in data["network_groups"]:
            grp_obj = {"description": "", "members": [], "type": "group"}
            data["network_groups"][obj_name] = grp_obj

        data["network_groups"][obj_name]["members"].append(member)

    # Parse IPv6 network groups

    logger.info(__name__ + ": parse IPv6 network groups - not yet supported")

    """
    Parse IPv6 network groups
    """

    # Parse service objects

    logger.info(__name__ + ": parse service objects")

    ## find first entry for tcp/udp service objects

    for re_service in re.finditer(
        "^set service (.*?) protocol (.*?)(?: src-port (.*?))? dst-port (.*?)(?: timeout ([0-9]{1,}))?$",
        src_config,
        re.MULTILINE,
    ):

        obj_name = re_service.group(1).replace('"', "")
        protocol = re_service.group(2)
        src_ports = re_service.group(3)
        dst_ports = re_service.group(4)
        dst_ports_split = dst_ports.split("-")
        timeout = str(re_service.group(5))

        svc_obj = {
            "description": "",
            "dst_ports": [],
            "protocols": [],
            "src_ports": [],
            "timeout": timeout or "",
            "type": "v2",
        }

        if dst_ports_split[0] == dst_ports_split[1]:
            svc_obj["dst_ports"].append(dst_ports_split[0])
        else:
            svc_obj["dst_ports"].append(dst_ports)

        if protocol == "tcp":
            svc_obj["protocols"].append("6")
            if not timeout:
                svc_obj["timeout"] = "1800"
        elif protocol == "udp":
            svc_obj["protocols"].append("17")
            if not timeout:
                svc_obj["timeout"] = "60"

        if src_ports:
            src_ports_split = src_ports.split("-")
            if src_ports_split[0] != "0" or src_ports_split[1] != "65535":
                if src_ports_split[0] == src_ports_split[1]:
                    svc_obj["src_ports"].append(src_ports_split[0])
                else:
                    svc_obj["src_ports"].append(src_ports)

        data["service_objects"][obj_name] = svc_obj

    ## find additional entries for tcp/udp service objects

    for re_service in re.finditer(
        "^set service (.*?) \+ (.*?)(?: src-port (.*?))? dst-port (.*?)$",
        src_config,
        re.MULTILINE,
    ):

        obj_name = re_service.group(1).replace('"', "")
        protocol = re_service.group(2)
        src_ports = re_service.group(3)
        src_ports_split = src_ports.split("-")
        dst_ports = re_service.group(4)
        dst_ports_split = dst_ports.split("-")

        if dst_ports_split[0] == dst_ports_split[1]:
            data["service_objects"][obj_name]["dst_ports"].append(dst_ports_split[0])
        else:
            data["service_objects"][obj_name]["dst_ports"].append(dst_ports)

        if (
            protocol == "tcp"
            and "6" not in data["service_objects"][obj_name]["protocols"]
        ):  ### how do these link to the port entry, will apply to all dst_ports
            data["service_objects"][obj_name]["protocols"].append("6")
        elif (
            protocol == "udp"
            and "17" not in data["service_objects"][obj_name]["protocols"]
        ):  ### how do these link to the port entry, will apply to all dst_ports
            data["service_objects"][obj_name]["protocols"].append("17")

        if src_ports_split[0] != "0" or src_ports_split[1] != "65535":
            if src_ports_split[0] == src_ports_split[1]:
                data["service_objects"][obj_name]["src_ports"].append(
                    src_ports_split[0]
                )
            else:
                data["service_objects"][obj_name]["src_ports"].append(src_ports)

    ## find icmp service objects

    for re_service in re.finditer(
        "^set service (.*?) protocol icmp type ([0-9]{1,}) code ([0-9]{1,})$",
        src_config,
        re.MULTILINE,
    ):

        obj_name = re_service.group(1).replace('"', "")
        icmp_type = str(re_service.group(2))
        icmp_code = str(re_service.group(3))

        svc_obj = {
            "description": "",
            "icmp_code": icmp_code,
            "icmp_type": icmp_type,
            "protocols": ["1"],
            "timeout": "60",
            "type": "v2",
        }

        data["service_objects"][obj_name] = svc_obj

    # Parse service groups

    logger.info(__name__ + ": parse service groups")

    for re_group in re.finditer(
        "^set group service (.*?) add (.*?)$", src_config, re.MULTILINE,
    ):

        obj_name = re_group.group(1).replace('"', "")
        member = re_group.group(2).replace('"', "")

        if obj_name not in data["service_groups"]:
            grp_obj = {"description": "", "members": [], "type": "group"}
            data["service_groups"][obj_name] = grp_obj

        data["service_groups"][obj_name]["members"].append(member)

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
