#!/usr/bin/env python

# Import modules

import logging
import sys
from traceback_with_variables import prints_tb, LoggerAsFile

import xml.etree.ElementTree as ET

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
interface_lookup = common.interface_lookup

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


@prints_tb(
    file_=LoggerAsFile(logger),
    num_context_lines=3,
    max_value_str_len=9999999,
    max_exc_str_len=9999999,
)
def parse(src_config, routing_info=""):

    logger.info(__name__ + ": parser module started")

    # Initialise data

    src_config_xml = ET.ElementTree(ET.fromstring(src_config))

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

    # Get context

    try:
        src_hardware_platform = src_config_xml.find("base-model").text
        logger.info(
            __name__ + ": source hardware platform is " + str(src_hardware_platform)
        )
    except:
        src_hardware_platform = None
        logger.info(__name__ + ": source hardware platform is unknown")

    try:
        src_software_version = src_config_xml.find("for-version").text
        logger.info(
            __name__ + ": source software version is " + str(src_software_version)
        )
    except:
        src_software_version = None
        logger.info(__name__ + ": source software version is unknown")

    # Parse system

    logger.info(__name__ + ": parse system")

    src_system = src_config_xml.find("system-parameters").find("device-conf")

    data["system"]["hostname"] = src_system.find("system-name").text
    logger.info(__name__ + ": system: hostname is " + data["system"]["hostname"])
    data["system"]["domain"] = src_system.find("domain-name").text
    logger.info(__name__ + ": system: domain name is " + data["system"]["domain"])

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces")

    interface_routes = []

    interfaces = src_config_xml.findall("./interface-list/interface")

    logger.info(
        __name__ + ": interfaces: found " + str(len(interfaces)) + " interfaces"
    )

    for interface in interfaces:

        interface_name = interface.find("name").text
        logger.info(__name__ + ": interfaces: parsing " + interface_name)

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
            "PPTP",
            "SSL-VPN",
            "WG-Loopback",
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

                    if physical_interface.find("enabled").text == "1":
                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is a physical interface",
                        )

                        # interface is enabled

                        data["interfaces"][interface_name]["enabled"] = True

                        # get interface node type

                        try:
                            intf_node_type = physical_interface.find(
                                "ip-node-type"
                            ).text
                            logger.info(
                                __name__
                                + ": interfaces: "
                                + interface_name
                                + ": ip-node-type is "
                                + intf_node_type,
                            )
                        except:
                            logger.info(
                                __name__
                                + ": interfaces: "
                                + interface_name
                                + ": could not find ip-node-type attribute, defaulting to IP4_ONLY",
                            )
                            intf_node_type = "IP4_ONLY"

                        # if ipv4

                        if intf_node_type == "IP4_ONLY":

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
                                data["interfaces"][interface_name][
                                    "ipv4_config"
                                ].append(interface_ip_member)

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
                                    len(
                                        data["interfaces"][interface_name][
                                            "ipv4_config"
                                        ]
                                    )
                                    == 0
                                ):
                                    interface_ip_member["type"] = "primary"
                                else:
                                    interface_ip_member["type"] = "secondary"

                                if interface_ip_member["ip_address"] not in [
                                    "",
                                    "0.0.0.0",
                                ]:
                                    data["interfaces"][interface_name][
                                        "ipv4_config"
                                    ].append(interface_ip_member)

                            logger.debug(
                                __name__
                                + ": interfaces: "
                                + interface_name
                                + ": ip addresses found "
                                + str(interface_ip_member),
                            )

                    elif physical_interface.find("enabled").text == "0":

                        data["interfaces"][interface_name]["enabled"] = False

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is disabled",
                        )

                        ### do something with disabled interfaces, these are missing ip-node-type
                        ### also need to add ipv6 support

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

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is external interface, default gateway is "
                            + interface_route["gateway"],
                        )

                    # set type

                    data["interfaces"][interface_name]["type"] = "interface"

                else:

                    intf_type = interface.find("./if-item-list/item/item-type").text

                    if intf_type == 2:  # VLAN interface

                        data["interfaces"][interface_name]["type"] = "vlan"

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is a VLAN interface",
                        )

                    if intf_type == 4:  # VPN tunnel interface

                        data["interfaces"][interface_name]["type"] = "vpn"

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is a VPN tunnel interface",
                        )

                    if intf_type == 5:  # SSL VPN tunnel interface

                        data["interfaces"][interface_name]["type"] = "sslvpn"

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is a SSL VPN tunnel interface",
                        )

                    elif intf_type == 13:  # Loopback interface

                        data["interfaces"][interface_name]["type"] = "loopback"

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is a loopback interface",
                        )

                    else:

                        data["interfaces"][interface_name]["type"] = "unknown"

                        logger.info(
                            __name__
                            + ": interfaces: "
                            + interface_name
                            + ": is an unknown interface type",
                        )

                    logger.debug(
                        __name__
                        + ": interfaces: "
                        + interface_name
                        + ": "
                        + str(ET.tostring(interface)),
                    )

        else:

            logger.info(
                __name__
                + ": interfaces: "
                + interface_name
                + ": is a default interface, ignoring"
            )

            logger.debug(
                __name__
                + ": interfaces: "
                + interface_name
                + ": "
                + str(ET.tostring(interface)),
            )

    # Parse zones

    logger.info(__name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.info(__name__ + ": parse static routes")

    src_routes = src_config_xml.findall("./system-parameters/route/route-entry")

    logger.info(
        __name__ + ": routes: found " + str(len(interface_routes)) + " interface routes"
    )

    for route_id, interface_route_config in enumerate(interface_routes):

        logger.info(__name__ + ": routes: parsing interface route " + str(route_id))

        route = {}
        route["network"] = "0.0.0.0"
        route["mask"] = "0.0.0.0"
        route["gateway"] = interface_route_config["gateway"]
        route["interface"] = interface_route_config["interface"]
        route["distance"] = "1"

        logger.info(
            __name__
            + ": routes: parsing interface route to "
            + route["gateway"]
            + " for interface "
            + route["interface"]
        )

        data["routes"].append(route)

    logger.info(__name__ + ": routes: found " + str(len(src_routes)) + " static routes")

    for route_id, route_config in enumerate(src_routes):

        logger.info(__name__ + ": routes: parsing static route " + str(route_id))

        route_gateway = route_config.find("gateway-ip").text

        route = {}
        route["network"] = route_config.find("dest-address").text
        route["mask"] = route_config.find("mask").text
        route["gateway"] = route_gateway
        route["interface"] = interface_lookup(
            route_gateway, data["interfaces"], data["routes"]
        )
        route["distance"] = route_config.find("metric").text

        data["routes"].append(route)

    # Parse network groups

    logger.info(__name__ + ": parse network groups")

    src_addr_grp = src_config_xml.findall("./address-group-list/address-group")

    logger.info(
        __name__
        + ": network_groups: found "
        + str(len(src_addr_grp))
        + " network groups"
    )

    for addr_grp in src_addr_grp:

        grp_name = cleanse_names(addr_grp.find("name").text)

        logger.info(
            __name__ + ": network_groups: parsing network group " + str(grp_name)
        )

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

    logger.info(__name__ + ": parse service groups")

    src_services = src_config_xml.findall("./service-list/service")

    logger.info(
        __name__
        + ": service_groups: found "
        + str(len(src_services))
        + " service groups"
    )

    for svc_group in src_services:

        grp_name = cleanse_names(svc_group.find("name").text)

        logger.info(
            __name__ + ": service_groups: parsing service group " + str(grp_name)
        )

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
                    data["service_objects"][mbr_name]["dst_port"] = mbr_port
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
                    data["service_objects"][mbr_name]["dst_port_first"] = mbr_port_first
                    data["service_objects"][mbr_name]["dst_port_last"] = mbr_port_last
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
                    data["service_objects"][mbr_name]["icmp_type"] = mbr_icmp_type
                    data["service_objects"][mbr_name]["icmp_code"] = mbr_icmp_code
                    data["service_objects"][mbr_name]["description"] = ""

                    data["service_groups"][grp_name]["members"].append(mbr_name)

    # Parse firewall policies

    logger.warning(__name__ + ": parse firewall policies - not yet supported")

    src_policies = src_config_xml.findall("./policy-list/policy")

    logger.info(__name__ + ": policies: found " + str(len(src_policies)) + " policies")

    for policy_id, policy_config in enumerate(src_policies):

        logger.info(__name__ + ": policies: parsing policy " + str(policy_id))

        policy = {}

        policy["action"] = ""
        policy["description"] = policy_config.find("description").text
        policy["dst_addresses"] = []
        policy["dst_interfaces"] = []
        policy["dst_services"] = []
        policy["enabled"] = False if policy_config.find("enable").text == "0" else True
        policy["logging"] = False if policy_config.find("log").text == "0" else True
        policy["name"] = policy_config.find("name").text
        policy["nat"] = ""  ### many values here - nat, global-1to1-nat, global-dnat
        policy["policy_set"] = ""
        policy["protocol"] = "any"
        policy["schedule"] = policy_config.find("schedule").text
        policy["src_addresses"] = []
        policy["src_interfaces"] = []
        policy["src_services"] = ["any"]
        policy["type"] = "policy"
        policy["users_excluded"] = []
        policy["users_included"] = []

        ## find desination addresses

        for dst_alias_name in policy_config.find("to-alias-list").findall("alias"):

            if dst_alias_name.text == "Any":

                dst_address = {}
                dst_address["name"] = "any"
                dst_address["type"] = "any"

                policy["dst_addresses"].append(dst_address)

            else:

                dst_address = {}
                dst_address["name"] = dst_alias_name.text
                dst_address["type"] = "network"  ## need to check if a group

                policy["dst_addresses"].append(dst_address)

        ## find desination services

        for dst_service_name in policy_config.findall("service"):

            if dst_service_name.text == "Any":

                dst_service = {}
                dst_service["name"] = "any"
                dst_service["type"] = "any"

                policy["dst_services"].append(dst_service)

            else:

                dst_service = {}
                dst_service["name"] = dst_service_name.text
                dst_service["type"] = "network"  ## need to check if a group

                policy["dst_services"].append(dst_service)

        ## find source addresses

        for src_alias_name in policy_config.find("from-alias-list").findall("alias"):

            if src_alias_name.text == "Any":

                src_address = {}
                src_address["name"] = "any"
                src_address["type"] = "any"

                policy["src_addresses"].append(src_address)

            else:

                src_address = {}
                src_address["name"] = src_alias_name.text
                src_address["type"] = "network"  ## need to check if a group

                policy["src_addresses"].append(src_address)

        ### need to lookup interface for destination alias

        ### need to lookup interface for source alias

        # data["policies"].append(policy)

    # Parse NAT

    logger.warning(__name__ + ": parse NAT - not yet supported")

    # Return parsed data

    logger.info(__name__ + ": parser module finished")

    return data
