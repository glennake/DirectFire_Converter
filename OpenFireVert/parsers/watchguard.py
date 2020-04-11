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

    logger.log(2, __name__ + ": parse interfaces - not yet supported")

    """
    Parse interfaces
    """

    # Parse zones

    logger.log(2, __name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    src_routes = src_config_xml.findall("./system-parameters/route/route-entry")

    routes_key = 1

    for route in src_routes:

        data["routes"][routes_key] = {}
        data["routes"][routes_key]["network"] = route.find("dest-address").text
        data["routes"][routes_key]["mask"] = route.find("mask").text
        data["routes"][routes_key]["gateway"] = route.find("gateway-ip").text
        ### need to parse interfaces then can lookup and add to route
        # data["routes"][routes_key]["interface"] = interface_lookup()
        data["routes"][routes_key]["distance"] = route.find("metric").text
        data["routes"][routes_key][
            "interface"
        ] = ""  # need to resolve interface from gateway

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
        data["policies"][policy_id]["dst_address"] = []
        data["policies"][policy_id]["dst_interface"] = []
        data["policies"][policy_id]["dst_service"] = []
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
        data["policies"][policy_id]["nat_src_address"] = ""
        data["policies"][policy_id]["policy_set"] = ""
        data["policies"][policy_id]["protocol"] = "any"
        data["policies"][policy_id]["schedule"] = policy.find("schedule").text
        data["policies"][policy_id]["src_address"] = []
        data["policies"][policy_id]["src_interface"] = []
        data["policies"][policy_id]["src_service"] = ["any"]
        data["policies"][policy_id]["type"] = "policy"
        data["policies"][policy_id]["users"] = []

        ## find desination addresses

        for dst_alias in policy.find("to-alias-list").findall("alias"):
            if dst_alias.text == "Any":
                data["policies"][policy_id]["dst_address"].append("any")
            else:
                data["policies"][policy_id]["dst_address"].append(dst_alias.text)

        ## find desination services

        for dst_service in policy.findall("service"):
            if dst_service.text == "Any":
                data["policies"][policy_id]["dst_service"].append("any")
            else:
                data["policies"][policy_id]["dst_service"].append(dst_service.text)

        ## find source addresses

        for src_alias in policy.find("from-alias-list").findall("alias"):
            if src_alias.text == "Any":
                data["policies"][policy_id]["src_address"].append("any")
            else:
                data["policies"][policy_id]["src_address"].append(src_alias.text)

        ### need to lookup interface for destination alias

        ### need to lookup interface for source alias

        policy_id += 1

    # Parse NAT

    logger.log(3, __name__ + ": parse NAT - not yet supported")

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
