#!/usr/bin/env python

# Import modules

import xml.etree.ElementTree as ET

# Import common, logging and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
interface_lookup = common.interface_lookup


def parse(logger, src_config):

    logger.log(2, __name__ + ": parser module started")

    # Initialise XML element tree

    src_config_xml = ET.ElementTree(ET.fromstring(src_config))

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

    src_system = src_config_xml.find("system-parameters").find("device-conf")

    data["system"]["hostname"] = src_system.find("system-name").text
    data["system"]["domain"] = src_system.find("domain-name").text

    # Parse interfaces

    logger.log(2, __name__ + ": parse interfaces")

    interface_routes = []

    interfaces = src_config_xml.findall("./interface-list/interface")

    for interface in interfaces:

        interface_name = interface.find("name").text

        data["interfaces"][interface_name] = {}
        data["interfaces"][interface_name]["enabled"] = True
        data["interfaces"][interface_name]["description"] = (
            interface.find("description").text if interface.find("description") else ""
        )
        data["interfaces"][interface_name]["ipv4_config"] = []
        data["interfaces"][interface_name]["mtu"] = ""
        data["interfaces"][interface_name]["physical_interfaces"] = []
        data["interfaces"][interface_name]["type"] = "interface"
        data["interfaces"][interface_name]["vlan_id"] = ""
        data["interfaces"][interface_name]["vlan_name"] = ""

        if interface_name not in [
            "Any",
            "Any-BOVPN",
            "Any-External",
            "Any-Multicast",
            "Any-MUVPN",
            "Any-Optional",
            "Any-Trusted",
            "Any-VPN",
            "Firebox",
            "Tunnel-Switch",
        ]:

            data["interfaces"][interface_name] = {}
            data["interfaces"][interface_name]["enabled"] = True
            data["interfaces"][interface_name]["description"] = (
                interface.find("description").text
                if interface.find("description")
                else ""
            )
            data["interfaces"][interface_name]["ipv4_config"] = []
            data["interfaces"][interface_name]["ipv6_config"] = []
            data["interfaces"][interface_name]["mtu"] = ""
            data["interfaces"][interface_name]["physical_interfaces"] = []
            data["interfaces"][interface_name]["vlan_id"] = ""
            data["interfaces"][interface_name]["vlan_name"] = ""

            interface_items = interface.findall("./if-item-list/item")

            for item in interface_items:

                physical_interface = item.find("physical-if")

                if physical_interface:

                    # find interface enabled

                    if physical_interface.find("mtu").text == "0":
                        data["interfaces"][interface_name]["enabled"] = False
                    else:
                        data["interfaces"][interface_name]["enabled"] = True

                    # if ipv4

                    if physical_interface.find("ip-node-type").text == "IP4_ONLY":

                        # find interface primary ip config

                        interface_ip_member = {}
                        interface_ip_member["ip_address"] = physical_interface.find(
                            "ip"
                        ).text
                        interface_ip_member["mask"] = physical_interface.find(
                            "netmask"
                        ).text
                        interface_ip_member["type"] = "primary"

                        if interface_ip_member["ip_address"] not in ["", "0.0.0.0"]:
                            data["interfaces"][interface_name]["ipv4_config"].append(
                                interface_ip_member
                            )

                        # find interface secondary ip config

                        secondary_ip = physical_interface.findall(
                            "./secondary-ip-list/secondary-ip"
                        )

                        for ipv4_config in secondary_ip:

                            interface_ip_member = {}
                            interface_ip_member["ip_address"] = ipv4_config.find(
                                "ip"
                            ).text
                            interface_ip_member["mask"] = ipv4_config.find(
                                "netmask"
                            ).text

                            if (
                                len(data["interfaces"][interface_name]["ipv4_config"])
                                == 0
                            ):
                                interface_ip_member["type"] = "primary"
                            else:
                                interface_ip_member["type"] = "secondary"

                            if interface_ip_member["ip_address"] not in ["", "0.0.0.0"]:
                                data["interfaces"][interface_name][
                                    "ipv4_config"
                                ].append(interface_ip_member)

                    ### need to add ipv6 support

                    # find interface mtu

                    data["interfaces"][interface_name]["mtu"] = physical_interface.find(
                        "mtu"
                    ).text

                    # if an external interface add an interface route

                    external_interface = physical_interface.find("external-if")

                    if external_interface:

                        interface_route = {}
                        interface_route["gateway"] = physical_interface.find(
                            "default-gateway"
                        ).text
                        interface_route["interface"] = interface_name

                        interface_routes.append(interface_route)

                    # set type

                    data["interfaces"][interface_name]["type"] = "interface"

                else:

                    # probably a VPN tunnel interface

                    data["interfaces"][interface_name]["type"] = "vpn"

    # Parse zones

    logger.log(2, __name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    src_routes = src_config_xml.findall("./system-parameters/route/route-entry")

    routes_key = 1

    for interface_route in interface_routes:

        data["routes"][routes_key] = {}
        data["routes"][routes_key]["network"] = "0.0.0.0"
        data["routes"][routes_key]["mask"] = "0.0.0.0"
        data["routes"][routes_key]["gateway"] = interface_route["gateway"]
        data["routes"][routes_key]["interface"] = interface_route["interface"]
        data["routes"][routes_key]["distance"] = "1"

        routes_key += 1

    for route in src_routes:

        route_gateway = route.find("gateway-ip").text

        data["routes"][routes_key] = {}
        data["routes"][routes_key]["network"] = route.find("dest-address").text
        data["routes"][routes_key]["mask"] = route.find("mask").text
        data["routes"][routes_key]["gateway"] = route_gateway
        data["routes"][routes_key]["interface"] = interface_lookup(
            route_gateway, data["interfaces"]
        )
        data["routes"][routes_key]["distance"] = route.find("metric").text

        routes_key += 1

    # Parse network groups

    logger.log(2, __name__ + ": parse network groups")

    src_addr_grp = src_config_xml.findall("./address-group-list/address-group")

    for addr_grp in src_addr_grp:

        grp_name = cleanse_names(addr_grp.find("name").text)

        data["network_groups"][grp_name] = {}
        data["network_groups"][grp_name]["type"] = "group"
        data["network_groups"][grp_name]["description"] = addr_grp.find(
            "description"
        ).text
        data["network_groups"][grp_name]["members"] = []

        members = addr_grp.findall("./addr-group-member/member")

        for member in members:

            mbr_type = member.find("type").text

            if mbr_type == "1":  # host

                mbr_host = member.find("host-ip-addr").text
                mbr_name = "host_" + mbr_host

                data["network_objects"][mbr_name] = {}
                data["network_objects"][mbr_name]["type"] = "host"
                data["network_objects"][mbr_name]["host"] = mbr_host
                data["network_objects"][mbr_name]["description"] = ""

                data["network_groups"][grp_name]["members"].append(mbr_name)

            elif mbr_type == "2":  # network

                mbr_network = member.find("ip-network-addr").text
                mbr_mask = member.find("ip-mask").text
                mbr_name = "net_" + mbr_network + "_" + mbr_mask

                data["network_objects"][mbr_name] = {}
                data["network_objects"][mbr_name]["type"] = "network"
                data["network_objects"][mbr_name]["network"] = mbr_network
                data["network_objects"][mbr_name]["mask"] = mbr_mask
                data["network_objects"][mbr_name]["description"] = ""

                data["network_groups"][grp_name]["members"].append(mbr_name)

            elif mbr_type == "3":  # ip range

                mbr_address_first = member.find("start-ip-addr").text
                mbr_address_last = member.find("end-ip-addr").text
                mbr_name = "range_" + mbr_address_first + "-" + mbr_address_last

                data["network_objects"][mbr_name] = {}
                data["network_objects"][mbr_name]["type"] = "range"
                data["network_objects"][mbr_name]["address_first"] = mbr_address_first
                data["network_objects"][mbr_name]["address_last"] = mbr_address_last
                data["network_objects"][mbr_name]["description"] = ""

                data["network_groups"][grp_name]["members"].append(mbr_name)

    # Parse service groups

    logger.log(2, __name__ + ": parse service groups")

    src_services = src_config_xml.findall("./service-list/service")

    for svc_group in src_services:

        grp_name = cleanse_names(svc_group.find("name").text)

        data["service_groups"][grp_name] = {}
        data["service_groups"][grp_name]["type"] = "group"
        data["service_groups"][grp_name]["description"] = svc_group.find(
            "description"
        ).text
        data["service_groups"][grp_name]["members"] = []

        members = svc_group.findall("./service-item/member")

        protocols_with_ports = ["6", "17"]

        for member in members:

            mbr_protocol = member.find("protocol").text
            mbr_type = member.find("type").text

            if mbr_protocol in protocols_with_ports:

                if mbr_type == "1":  # single port

                    mbr_port = member.find("server-port").text
                    mbr_name = "svc_" + mbr_protocol + "_" + mbr_port

                    data["service_objects"][mbr_name] = {}
                    data["service_objects"][mbr_name]["type"] = "service"
                    data["service_objects"][mbr_name]["protocol"] = mbr_protocol
                    data["service_objects"][mbr_name]["destination_port"] = mbr_port
                    data["service_objects"][mbr_name]["description"] = ""

                    data["service_groups"][grp_name]["members"].append(mbr_name)

                elif mbr_type == "2":  # port range

                    mbr_port_first = member.find("start-server-port").text
                    mbr_port_last = member.find("end-server-port").text
                    mbr_name = (
                        "svc_"
                        + mbr_protocol
                        + "_"
                        + mbr_port_first
                        + "-"
                        + mbr_port_last
                    )

                    data["service_objects"][mbr_name] = {}
                    data["service_objects"][mbr_name]["type"] = "range"
                    data["service_objects"][mbr_name]["protocol"] = mbr_protocol
                    data["service_objects"][mbr_name][
                        "destination_port_first"
                    ] = mbr_port_first
                    data["service_objects"][mbr_name][
                        "destination_port_last"
                    ] = mbr_port_last
                    data["service_objects"][mbr_name]["description"] = ""

                    data["service_groups"][grp_name]["members"].append(mbr_name)

            elif mbr_protocol == "1":

                if mbr_type == "1":  # single type / code

                    mbr_icmp_type = member.find("icmp-type").text
                    mbr_icmp_code = member.find("icmp-code").text
                    mbr_name = (
                        "svc_"
                        + mbr_protocol
                        + "_"
                        + mbr_icmp_type
                        + "_"
                        + mbr_icmp_code
                    )

                    data["service_objects"][mbr_name] = {}
                    data["service_objects"][mbr_name]["type"] = "service"
                    data["service_objects"][mbr_name]["protocol"] = mbr_protocol
                    data["service_objects"][mbr_name]["icmp-type"] = mbr_icmp_type
                    data["service_objects"][mbr_name]["icmp-code"] = mbr_icmp_code
                    data["service_objects"][mbr_name]["description"] = ""

                    data["service_groups"][grp_name]["members"].append(mbr_name)

    # Parse firewall policies

    logger.log(2, __name__ + ": parse firewall policies")

    src_policies = src_config_xml.findall("./policy-list/policy")

    for policy in src_policies:

        data["policies"][policy_id] = {}

        data["policies"][policy_id]["action"] = ""
        data["policies"][policy_id]["description"] = policy.find("description").text
        data["policies"][policy_id]["dst_addresses"] = []
        data["policies"][policy_id]["dst_interfaces"] = []
        data["policies"][policy_id]["dst_services"] = []
        data["policies"][policy_id]["enabled"] = (
            False if policy.find("enable").text == "0" else True
        )
        data["policies"][policy_id]["id"] = policy_id
        data["policies"][policy_id]["logging"] = (
            False if policy.find("log").text == "0" else True
        )
        data["policies"][policy_id]["name"] = policy.find("name").text
        data["policies"][policy_id][
            "nat"
        ] = ""  ### many values here - nat, global-1to1-nat, global-dnat
        data["policies"][policy_id]["policy_set"] = ""
        data["policies"][policy_id]["protocol"] = "any"
        data["policies"][policy_id]["schedule"] = policy.find("schedule").text
        data["policies"][policy_id]["src_addresses"] = []
        data["policies"][policy_id]["src_interfaces"] = []
        data["policies"][policy_id]["src_services"] = ["any"]
        data["policies"][policy_id]["type"] = "policy"
        data["policies"][policy_id]["users_excluded"] = []
        data["policies"][policy_id]["users_included"] = []

        ## find desination addresses

        for dst_alias in policy.find("to-alias-list").findall("alias"):
            if dst_alias.text == "Any":
                data["policies"][policy_id]["dst_addresses"].append("any")
            else:
                data["policies"][policy_id]["dst_addresses"].append(dst_alias.text)

        ## find desination services

        for dst_service in policy.findall("service"):
            if dst_service.text == "Any":
                data["policies"][policy_id]["dst_services"].append("any")
            else:
                data["policies"][policy_id]["dst_services"].append(dst_service.text)

        ## find source addresses

        for src_alias in policy.find("from-alias-list").findall("alias"):
            if src_alias.text == "Any":
                data["policies"][policy_id]["src_addresses"].append("any")
            else:
                data["policies"][policy_id]["src_addresses"].append(src_alias.text)

        ### need to lookup interface for destination alias

        ### need to lookup interface for source alias

        policy_id += 1

    # Parse NAT

    logger.log(3, __name__ + ": parse NAT - not yet supported")

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
