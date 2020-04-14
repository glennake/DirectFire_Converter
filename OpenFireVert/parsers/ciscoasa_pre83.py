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
interface_lookup = common.interface_lookup


def parse(logger, src_config, routing_info=""):

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

    route_id = 1
    route6_id = 1
    policy_id = 1
    nat_id = 1

    ## add default network objects

    data["network_objects"]["any"] = {}
    data["network_objects"]["any"]["type"] = "any"

    data["network_objects"]["any4"] = {}
    data["network_objects"]["any4"]["type"] = "any"

    ## define default protocols

    default_protocol_list = [
        "ah",
        "eigrp",
        "esp",
        "gre",
        "icmp",
        "icmp6",
        "igmp",
        "igrp",
        "ip",
        "ipinip",
        "ipsec",
        "nos",
        "ospf",
        "pcp",
        "pim",
        "pptp",
        "snp",
        "tcp",
        "udp",
    ]

    # Function to resolve default services from name to port number

    def lookup_name(name):

        name_object = re.search(
            "name ("
            + common.common_regex.ipv4_address
            + ") "
            + name
            + "(?: description (.*))?",
            src_config,
        )

        return name_object

    def resolve_default_service(service):

        try:

            int(service)

        except:

            if service == "aol":
                service = "5190"
            elif service == "bgp":
                service = "179"
            elif service == "biff":
                service = "512"
            elif service == "bootpc":
                service = "68"
            elif service == "bootps":
                service = "67"
            elif service == "chargen":
                service = "19"
            elif service == "cifs":
                service = "3020"
            elif service == "citrix-ica":
                service = "1494"
            elif service == "cmd":
                service = "514"
            elif service == "ctiqbe":
                service = "2748"
            elif service == "daytime":
                service = "13"
            elif service == "discard":
                service = "9"
            elif service == "domain":
                service = "53"
            elif service == "dnsix":
                service = "195"
            elif service == "echo":
                service = "7"
            elif service == "exec":
                service = "512"
            elif service == "finger":
                service = "79"
            elif service == "ftp":
                service = "21"
            elif service == "ftp-data":
                service = "20"
            elif service == "gopher":
                service = "70"
            elif service == "http":
                service = "80"
            elif service == "https":
                service = "443"
            elif service == "h323":
                service = "1720"
            elif service == "hostname":
                service = "101"
            elif service == "ident":
                service = "113"
            elif service == "imap4":
                service = "143"
            elif service == "irc":
                service = "194"
            elif service == "isakmp":
                service = "500"
            elif service == "kerberos":
                service = "88"
            elif service == "klogin":
                service = "543"
            elif service == "kshell":
                service = "544"
            elif service == "ldap":
                service = "389"
            elif service == "ldaps":
                service = "636"
            elif service == "lpd":
                service = "515"
            elif service == "login":
                service = "513"
            elif service == "lotusnotes":
                service = "1352"
            elif service == "mobile-ip":
                service = "434"
            elif service == "nameserver":
                service = "42"
            elif service == "netbios-ns":
                service = "137"
            elif service == "netbios-dgm":
                service = "138"
            elif service == "netbios-ssn":
                service = "139"
            elif service == "nfs":
                service = "2049"
            elif service == "nntp":
                service = "119"
            elif service == "ntp":
                service = "123"
            elif service == "pcanywhere-status":
                service = "5632"
            elif service == "pcanywhere-data":
                service = "5631"
            elif service == "pim-auto-rp":
                service = "496"
            elif service == "pop2":
                service = "109"
            elif service == "pop3":
                service = "110"
            elif service == "pptp":
                service = "1723"
            elif service == "radius":
                service = "1645"
            elif service == "radius-acct":
                service = "1646"
            elif service == "rip":
                service = "520"
            elif service == "rsh":
                service = "514"
            elif service == "rtsp":
                service = "554"
            elif service == "secureid-udp":
                service = "5510"
            elif service == "sip":
                service = "5060"
            elif service == "smtp":
                service = "25"
            elif service == "snmp":
                service = "161"
            elif service == "snmptrap":
                service = "162"
            elif service == "sqlnet":
                service = "1521"
            elif service == "ssh":
                service = "22"
            elif service == "sunrpc":
                service = "111"
            elif service == "syslog":
                service = "514"
            elif service == "tacacs":
                service = "49"
            elif service == "talk":
                service = "517"
            elif service == "telnet":
                service = "23"
            elif service == "tftp":
                service = "69"
            elif service == "time":
                service = "37"
            elif service == "uucp":
                service = "540"
            elif service == "who":
                service = "513"
            elif service == "whois":
                service = "43"
            elif service == "www":
                service = "80"
            elif service == "xdmcp":
                service = "177"

        return service

    # Parse system

    logger.log(2, __name__ + ": parse system - not yet supported")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse interfaces

    logger.log(2, __name__ + ": parse interfaces")

    for re_match in re.finditer("interface (.*)\n(?: .*\n){1,}!", src_config,):

        ## split interface config and parse nameif

        interface_config = str(re_match.group(0)).split("\n")

        for line in interface_config:

            ## find nameif

            if " nameif" in line and " no nameif" not in line:
                interface_name = line[8:]

        ## create interface object

        interface_phys_name = re_match.group(1)

        if "." in interface_phys_name:  ## sub interface

            sub_interface = interface_phys_name.split(".")

            data["interfaces"][interface_name] = {}
            data["interfaces"][interface_name]["physical_interfaces"] = []
            data["interfaces"][interface_name]["type"] = "subinterface"
            data["interfaces"][interface_name]["vlan_id"] = sub_interface[1]
            data["interfaces"][interface_name]["vlan_name"] = ""

            data["interfaces"][interface_name]["physical_interfaces"].append(
                sub_interface[0]
            )

        else:  ## physical interface

            data["interfaces"][interface_name] = {}
            data["interfaces"][interface_name]["physical_interfaces"] = []
            data["interfaces"][interface_name]["type"] = "interface"
            data["interfaces"][interface_name]["vlan_id"] = ""
            data["interfaces"][interface_name]["vlan_name"] = ""

            data["interfaces"][interface_name]["physical_interfaces"].append(
                interface_phys_name
            )

        data["interfaces"][interface_name]["description"] = ""
        data["interfaces"][interface_name]["enabled"] = True
        data["interfaces"][interface_name]["ipv4_config"] = []
        data["interfaces"][interface_name]["ipv6_config"] = []

        ## parse interface config

        for line in interface_config:

            ## find description

            if " description" in line:
                data["interfaces"][interface_name]["description"] = line[13:]

            ## find shutdown

            if " shutdown" in line:
                data["interfaces"][interface_name]["enabled"] = False

            ## find ip config

            if " ip address" in line and " no ip address" not in line:

                ip_address_line = line.split(" ")

                ip_config = {}
                ip_config["ip_address"] = ip_address_line[3]
                ip_config["mask"] = ip_address_line[4]

                data["interfaces"][interface_name]["ipv4_config"].append(ip_config)

    # Parse zones

    logger.log(2, __name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    for re_match in re.finditer("^route .*$", src_config, re.MULTILINE):

        ## split route config

        route_config = str(re_match.group(0)).split(" ")

        route = {}

        route["description"] = ""
        route["distance"] = route_config[5]
        route["gateway"] = route_config[4]
        route["interface"] = route_config[1]
        route["mask"] = route_config[3]
        route["network"] = ""
        route["source"] = ""
        route["type"] = "static"

        ## check if network is a name object

        name_object = lookup_name(route_config[2])

        if name_object:
            route["network"] = name_object.group(1)

        else:
            route["network"] = route_config[2]

        ## add to routes

        data["routes"].append(route)

    # Parse IPv4 network objects

    # logger.log(2, __name__ + ": parse IPv4 network objects")

    # for re_match in re.finditer(
    #     r"name ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}) (\S{1,})(?: description (.{1,}))?",
    #     src_config,
    # ):

    #     data["network_objects"][re_match.group(2)] = {}
    #     data["network_objects"][re_match.group(2)]["type"] = "host"
    #     data["network_objects"][re_match.group(2)]["host"] = re_match.group(1)
    #     data["network_objects"][re_match.group(2)]["description"] = re_match.group(3)

    # # If address object is a network, change its type and seperate address / mask

    # for address, attributes in data["network_objects"].items():

    #     for re_match in re.finditer(
    #         r"network-object "
    #         + address
    #         + " ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})",
    #         src_config,
    #     ):

    #         data["network_objects"][address]["type"] = "network"
    #         data["network_objects"][address]["network"] = attributes["host"]
    #         data["network_objects"][address]["mask"] = re_match.group(1)

    # Parse network groups

    logger.log(2, __name__ + ": parse network groups")

    for re_match in re.finditer("object-group network (.*)\n(?: .*\n){1,}", src_config):

        network_groups = str(re_match.group(0)).split("\n")

        network_group_name = network_groups[0][21:]

        data["network_groups"][network_group_name] = {}
        data["network_groups"][network_group_name]["description"] = ""
        data["network_groups"][network_group_name]["members"] = []

        ## check for description and set start index

        if " description" in network_groups[1]:
            data["network_groups"][network_group_name]["description"] = network_groups[
                1
            ][13:]
            i = 2

        else:
            i = 1

        ## loop through network group entries

        for member in network_groups[i:]:

            if " network-object host" in member:  ## if host member

                network_object = member[21:]

                name_object = lookup_name(network_object)

                if name_object:  ## check for associated name object

                    data["network_objects"][network_object] = {}
                    data["network_objects"][network_object]["type"] = "host"
                    data["network_objects"][network_object]["host"] = name_object.group(
                        1
                    )

                    if name_object.group(2):
                        data["network_objects"][network_object][
                            "description"
                        ] = name_object.group(2)

                    else:
                        data["network_objects"][network_object]["description"] = ""

                else:  ## else is a directly defined host

                    data["network_objects"][network_object] = {}
                    data["network_objects"][network_object]["type"] = "host"
                    data["network_objects"][network_object]["host"] = network_object
                    data["network_objects"][network_object]["description"] = ""

                ## add network object to the group

                data["network_groups"][network_group_name]["members"].append(
                    network_object
                )

            elif " network-object" in member:  ## if network member

                network_config = str(member[16:]).split(" ")

                name_object = lookup_name(network_config[0])

                if network_config[1] == "255.255.255.255":  # is a host

                    network_object = network_config[0]

                    if name_object:  ## check for associated name object

                        data["network_objects"][network_object] = {}
                        data["network_objects"][network_object]["type"] = "host"
                        data["network_objects"][network_object][
                            "host"
                        ] = name_object.group(1)

                        if name_object.group(2):
                            data["network_objects"][network_object][
                                "description"
                            ] = name_object.group(2)

                        else:
                            data["network_objects"][network_object]["description"] = ""

                    else:  ## else is a directly defined host

                        data["network_objects"][network_object] = {}
                        data["network_objects"][network_object]["type"] = "host"
                        data["network_objects"][network_object]["host"] = network_object
                        data["network_objects"][network_object]["description"] = ""

                else:  ## is a network

                    network_object = network_config[0] + "_" + network_config[1]

                    if name_object:  ## check for associated name object

                        data["network_objects"][network_object] = {}
                        data["network_objects"][network_object]["type"] = "network"
                        data["network_objects"][network_object][
                            "network"
                        ] = name_object.group(1)
                        data["network_objects"][network_object][
                            "mask"
                        ] = network_config[1]

                        if name_object.group(2):
                            data["network_objects"][network_object][
                                "description"
                            ] = name_object.group(2)

                        else:
                            data["network_objects"][network_object]["description"] = ""

                    else:  ## else is a directly defined network

                        data["network_objects"][network_object] = {}
                        data["network_objects"][network_object]["type"] = "network"
                        data["network_objects"][network_object][
                            "network"
                        ] = network_config[0]
                        data["network_objects"][network_object][
                            "mask"
                        ] = network_config[1]
                        data["network_objects"][network_object]["description"] = ""

                ## add network object to the group

                data["network_groups"][network_group_name]["members"].append(
                    network_object
                )

            elif " group-object" in member:  ## if group member

                network_group = member[14:]

                data["network_groups"][network_group_name]["members"].append(
                    network_group
                )

    # for re_match in re.finditer(
    #     r"object-group network ([\S]*)[\s](?: description .*[\s])?(?: (?:network-object (?:host .*|.* [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})[\s])){1,}",
    #     src_config,
    # ):

    #     data["network_groups"][re_match.group(1)] = {}
    #     data["network_groups"][re_match.group(1)]["type"] = "group"
    #     data["network_groups"][re_match.group(1)]["description"] = ""
    #     data["network_groups"][re_match.group(1)]["members"] = []

    #     network_grp_desc = re.search(r" description (.*)", re_match.group(0))

    #     if network_grp_desc:
    #         data["network_groups"][re_match.group(1)][
    #             "description"
    #         ] = network_grp_desc.group(1)

    #     for re_match2 in re.finditer(
    #         r"(?:network-object (?:host (.*)|(.*) [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})){1,}",
    #         re_match.group(0),
    #     ):

    #         if re_match2.group(1):

    #             data["network_groups"][re_match.group(1)]["members"].append(
    #                 re_match2.group(1)
    #             )

    #         if re_match2.group(2):

    #             data["network_groups"][re_match.group(1)]["members"].append(
    #                 re_match2.group(2)
    #             )

    # Parse service groups

    logger.log(2, __name__ + ": parse service groups")

    for re_match in re.finditer(
        r"object-group service ([\S]*)(?: ([\S]*))?[\s](?: description .*[\s])?(?: port-object (eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?(?:[\s])?| service-object ([\S]*)(?: )?(?:[\s])?(?:(eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?(?:[\s])?)?){1,}",
        src_config,
    ):

        data["service_groups"][re_match.group(1)] = {}
        data["service_groups"][re_match.group(1)]["type"] = "group"
        data["service_groups"][re_match.group(1)]["protocol"] = re_match.group(2)
        data["service_groups"][re_match.group(1)]["description"] = ""
        data["service_groups"][re_match.group(1)]["members"] = []

        service_grp_desc = re.search(r" description (.*)", re_match.group(0))

        if service_grp_desc:

            data["service_groups"][re_match.group(1)][
                "description"
            ] = service_grp_desc.group(1)

        ### Need to add the ability to parse nested group objects in here

        # Parse port objects in service group

        for re_match2 in re.finditer(
            r"(?:port-object (eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?)",
            re_match.group(0),
        ):

            if re_match2.group(1) == "range":

                service_port_first = resolve_default_service(re_match2.group(2))
                service_port_last = resolve_default_service(re_match2.group(3))

                service_name = service_port_first + "-" + service_port_last

            else:

                service_port = resolve_default_service(re_match2.group(2))

                service_name = service_port

            # Break tcp-udp service entries to seperate TCP and UDP service objects

            if re_match.group(2) == "tcp-udp":

                # Create a TCP service object and add to service group

                data["service_objects"]["tcp_" + service_name] = {}

                data["service_objects"]["tcp_" + service_name]["protocol"] = "6"

                if re_match2.group(1) == "range":

                    data["service_objects"]["tcp_" + service_name]["type"] = "range"
                    data["service_objects"]["tcp_" + service_name][
                        "destination_port_first"
                    ] = service_port_first
                    data["service_objects"]["tcp_" + service_name][
                        "destination_port_last"
                    ] = service_port_last

                else:

                    data["service_objects"]["tcp_" + service_name]["type"] = "service"
                    data["service_objects"]["tcp_" + service_name][
                        "destination_port"
                    ] = service_port

                data["service_groups"][re_match.group(1)]["members"].append(
                    "tcp_" + service_name
                )

                # Create a UDP service object and add to service group

                data["service_objects"]["udp_" + service_name] = {}

                data["service_objects"]["udp_" + service_name]["protocol"] = "17"

                if re_match2.group(1) == "range":

                    data["service_objects"]["udp_" + service_name]["type"] = "range"
                    data["service_objects"]["udp_" + service_name][
                        "destination_port_first"
                    ] = service_port_first
                    data["service_objects"]["udp_" + service_name][
                        "destination_port_last"
                    ] = service_port_last

                else:

                    data["service_objects"]["udp_" + service_name]["type"] = "service"
                    data["service_objects"]["udp_" + service_name][
                        "destination_port"
                    ] = service_port

                data["service_groups"][re_match.group(1)]["members"].append(
                    "udp_" + service_name
                )

            # Process single protocol service entries

            else:

                service_name = re_match.group(2) + "_" + service_name

                data["service_objects"][service_name] = {}

                data["service_objects"][service_name]["protocol"] = re_match.group(2)

                if re_match2.group(1) == "range":

                    data["service_objects"][service_name]["type"] = "range"
                    data["service_objects"][service_name][
                        "destination_port_first"
                    ] = service_port_first
                    data["service_objects"][service_name][
                        "destination_port_last"
                    ] = service_port_last

                else:

                    data["service_objects"][service_name]["type"] = "service"
                    data["service_objects"][service_name][
                        "destination_port"
                    ] = service_port

                data["service_groups"][re_match.group(1)]["members"].append(
                    service_name
                )

        # Parse service objects in service group

        for re_match2 in re.finditer(
            r"service-object ([\S]*)(?:[\s])?(?:(eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?)?",
            re_match.group(0),
        ):

            if re_match2.group(2):

                if re_match2.group(1) == "range":

                    service_port_first = resolve_default_service(re_match2.group(3))
                    service_port_last = resolve_default_service(re_match2.group(4))

                    service_name = (
                        re_match2.group(1)
                        + "_"
                        + service_port_first
                        + "-"
                        + service_port_last
                    )

                else:

                    service_port = resolve_default_service(re_match2.group(3))

                    service_name = re_match2.group(1) + "_" + service_port

            else:

                service_name = re_match2.group(1) + "_all"

            ### Need to add the ability to parse ICMP services with type and code values in here

            if re_match2.group(2):

                data["service_objects"][service_name] = {}

                data["service_objects"][service_name]["protocol"] = re_match2.group(1)

                if re_match2.group(2) == "range":

                    data["service_objects"][service_name]["type"] = "range"
                    data["service_objects"][service_name][
                        "destination_port_first"
                    ] = service_port_first
                    data["service_objects"][service_name][
                        "destination_port_last"
                    ] = service_port_last

                else:

                    data["service_objects"][service_name]["type"] = "service"
                    data["service_objects"][service_name][
                        "destination_port"
                    ] = service_port

            else:

                data["service_objects"][service_name] = {}
                data["service_objects"][service_name]["type"] = "service"
                data["service_objects"][service_name]["protocol"] = re_match2.group(1)

            if re_match2.group(1) == "icmp":

                data["service_objects"][service_name]["icmp_type"] = ""
                data["service_objects"][service_name]["icmp_code"] = ""

            data["service_groups"][re_match.group(1)]["members"].append(service_name)

        ### Need to parse protocol groups here

    # Parse firewall policies

    logger.log(2, __name__ + ": parse firewall policies")

    ## parse policy interface mappings

    acl_interface_mappings = {}

    for re_match in re.finditer(
        "^access-group (.*) (in|out) interface (.*)$", src_config, re.MULTILINE
    ):

        acl_name = re_match.group(1)
        acl_direction = re_match.group(2)
        acl_interface = re_match.group(3)

        acl_interface_mappings[acl_name] = {}

        if acl_direction == "out":
            acl_interface_mappings[acl_name]["src_interface"] = ""
            acl_interface_mappings[acl_name]["dst_interface"] = acl_interface

        else:
            acl_interface_mappings[acl_name]["src_interface"] = acl_interface
            acl_interface_mappings[acl_name]["dst_interface"] = ""

    ## parse access list rules

    acl_remark = ""

    for match in re.finditer("^access-list .*", src_config, re.MULTILINE):

        acl_rule = match.group(0).split(" ")

        if acl_rule[1] in acl_interface_mappings:

            if acl_rule[2] == "remark":  ## ACL remark entry

                acl_remark = match.group(0).replace(
                    "access-list " + acl_rule[1] + " remark ", ""
                )

            elif acl_rule[2] == "extended":  ## ACL extended entry

                policy = {}

                policy["action"] = ""
                policy["description"] = ""
                policy["dst_addresses"] = []
                policy["dst_interfaces"] = []
                policy["dst_services"] = []
                policy["enabled"] = True
                policy["logging"] = False
                policy["name"] = ""
                policy["nat"] = ""
                policy["policy_set"] = acl_rule[1]
                policy["protocol"] = ""
                policy["schedule"] = ""
                policy["src_addresses"] = []
                policy["src_interfaces"] = []
                policy["src_services"] = []
                policy["type"] = "policy"
                policy["users_excluded"] = []
                policy["users_included"] = []

                ## map interface

                if policy["policy_set"] in acl_interface_mappings:

                    if acl_interface_mappings[policy["policy_set"]]["src_interface"]:

                        policy["src_interfaces"].append(
                            acl_interface_mappings[policy["policy_set"]][
                                "src_interface"
                            ]
                        )

                    if acl_interface_mappings[policy["policy_set"]]["dst_interface"]:

                        policy["src_interfaces"].append(
                            acl_interface_mappings[policy["policy_set"]][
                                "dst_interface"
                            ]
                        )

                ## parse action

                if acl_rule[3] == "permit":
                    policy["action"] = "allow"

                elif acl_rule[3] == "deny":
                    policy["action"] = "discard"

                ## start index from current position

                i = 4

                ## add remark if found in previous line then reset variable

                if acl_remark:
                    policy["description"] = acl_remark
                    acl_remark = ""

                ## parse protocol

                if acl_rule[4] in ["object", "object-group"]:
                    policy["dst_services"].append(acl_rule[5])
                    policy["protocol"] = acl_rule[5]
                    i = i + 2

                elif acl_rule[4] in ["ip"]:
                    policy["dst_services"].append("any")
                    policy["protocol"] = acl_rule[4]
                    i = i + 1

                else:
                    policy["protocol"] = acl_rule[4]
                    i = i + 1

                ## parse source addresses

                if acl_rule[i] == "object":  ## source object

                    src_address = {}
                    src_address["name"] = acl_rule[i + 1]
                    src_address["type"] = "network"

                    policy["src_addresses"].append(src_address)

                    i = i + 2

                elif acl_rule[i] == "object-group":  ## source object-group

                    src_address = {}
                    src_address["name"] = acl_rule[i + 1]
                    src_address["type"] = "group"

                    policy["src_addresses"].append(src_address)

                    i = i + 2

                elif acl_rule[i] == "host":  ## source host

                    name_object = lookup_name(acl_rule[i + 1])

                    if name_object:  ## check for associated name object

                        network_object = acl_rule[i + 1]

                        if network_object not in data["network_objects"]:

                            data["network_objects"][network_object] = {}
                            data["network_objects"][network_object]["type"] = "host"
                            data["network_objects"][network_object][
                                "host"
                            ] = name_object.group(1)

                            if name_object.group(2):
                                data["network_objects"][network_object][
                                    "description"
                                ] = name_object.group(2)

                            else:
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    else:  ## otherwise manually defined host address

                        network_object = acl_rule[i + 1]

                        if network_object not in data["network_objects"]:

                            data["network_objects"][network_object] = {}
                            data["network_objects"][network_object]["type"] = "host"
                            data["network_objects"][network_object]["host"] = acl_rule[
                                i + 1
                            ]
                            data["network_objects"][network_object]["description"] = ""

                    src_address = {}
                    src_address["name"] = network_object
                    src_address["type"] = "network"

                    policy["src_addresses"].append(src_address)

                    i = i + 2

                elif acl_rule[i] in ["any", "any4", "any6"]:  ## source any

                    src_address = {}
                    src_address["name"] = "any"
                    src_address["type"] = "any"

                    policy["src_addresses"].append(src_address)

                    i = i + 1

                else:

                    name_object = lookup_name(acl_rule[i])

                    if acl_rule[i + 1] == "255.255.255.255":  ## check if a host

                        if name_object:  ## check for associated name object

                            network_object = acl_rule[i]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object]["type"] = "host"
                                data["network_objects"][network_object][
                                    "host"
                                ] = name_object.group(1)

                                if name_object.group(2):
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object.group(2)

                                else:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = ""

                        else:  ## otherwise manually defined host

                            network_object = acl_rule[i]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object]["type"] = "host"
                                data["network_objects"][network_object][
                                    "host"
                                ] = acl_rule[i]
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    else:  ## else is a network

                        if name_object:  ## check for associated name object

                            network_object = acl_rule[i] + "_" + acl_rule[i + 1]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object][
                                    "type"
                                ] = "network"
                                data["network_objects"][network_object][
                                    "network"
                                ] = name_object.group(1)
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]

                                if name_object.group(2):
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object.group(2)

                                else:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = ""

                        else:  ## otherwise manually defined network/mask

                            network_object = acl_rule[i] + "_" + acl_rule[i + 1]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object][
                                    "type"
                                ] = "network"
                                data["network_objects"][network_object][
                                    "network"
                                ] = acl_rule[i]
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    src_address = {}
                    src_address["name"] = network_object
                    src_address["type"] = "network"

                    policy["src_addresses"].append(src_address)

                    i = i + 2

                ## parse destination addresses

                if acl_rule[i] == "object":  ## destination object

                    dst_address = {}
                    dst_address["name"] = acl_rule[i + 1]
                    dst_address["type"] = "network"

                    policy["dst_addresses"].append(dst_address)

                    i = i + 2

                elif acl_rule[i] == "object-group":  ## destination object-group

                    dst_address = {}
                    dst_address["name"] = acl_rule[i + 1]
                    dst_address["type"] = "group"

                    policy["dst_addresses"].append(dst_address)

                    i = i + 2

                elif acl_rule[i] == "host":  ## destination host

                    name_object = lookup_name(acl_rule[i + 1])

                    if name_object:  ## check for associated name object

                        network_object = acl_rule[i + 1]

                        if network_object not in data["network_objects"]:

                            data["network_objects"][network_object] = {}
                            data["network_objects"][network_object]["type"] = "host"
                            data["network_objects"][network_object][
                                "host"
                            ] = name_object.group(1)

                            if name_object.group(2):
                                data["network_objects"][network_object][
                                    "description"
                                ] = name_object.group(2)

                            else:
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    else:  ## otherwise manually defined host address

                        network_object = acl_rule[i + 1]

                        if network_object not in data["network_objects"]:

                            data["network_objects"][network_object] = {}
                            data["network_objects"][network_object]["type"] = "host"
                            data["network_objects"][network_object]["host"] = acl_rule[
                                i + 1
                            ]
                            data["network_objects"][network_object]["description"] = ""

                    dst_address = {}
                    dst_address["name"] = network_object
                    dst_address["type"] = "network"

                    policy["dst_addresses"].append(dst_address)

                    i = i + 2

                elif acl_rule[i] in ["any", "any4", "any6"]:  ## destination any

                    dst_address = {}
                    dst_address["name"] = "any"
                    dst_address["type"] = "any"

                    policy["dst_addresses"].append(dst_address)

                    i = i + 1

                else:

                    name_object = lookup_name(acl_rule[i])

                    if acl_rule[i + 1] == "255.255.255.255":  ## check if a host

                        if name_object:  ## check for associated name object

                            network_object = acl_rule[i]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object]["type"] = "host"
                                data["network_objects"][network_object][
                                    "host"
                                ] = name_object.group(1)

                                if name_object.group(2):
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object.group(2)

                                else:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = ""

                        else:  ## otherwise manually defined host

                            network_object = acl_rule[i]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object]["type"] = "host"
                                data["network_objects"][network_object][
                                    "host"
                                ] = acl_rule[i]
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    else:  ## else is a network

                        if name_object:  ## check for associated name object

                            network_object = acl_rule[i] + "_" + acl_rule[i + 1]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object][
                                    "type"
                                ] = "network"
                                data["network_objects"][network_object][
                                    "network"
                                ] = name_object.group(1)
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]

                                if name_object.group(2):
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object.group(2)

                                else:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = ""

                        else:  ## otherwise manually defined network/mask

                            network_object = acl_rule[i] + "_" + acl_rule[i + 1]

                            if network_object not in data["network_objects"]:

                                data["network_objects"][network_object] = {}
                                data["network_objects"][network_object][
                                    "type"
                                ] = "network"
                                data["network_objects"][network_object][
                                    "network"
                                ] = acl_rule[i]
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]
                                data["network_objects"][network_object][
                                    "description"
                                ] = ""

                    dst_address = {}
                    dst_address["name"] = network_object
                    dst_address["type"] = "network"

                    policy["dst_addresses"].append(dst_address)

                    i = i + 2

                ## check remaining entries for ACL args

                for acl_args in acl_rule[i:]:

                    if "inactive" in acl_args:
                        policy["enabled"] = False

                    if "log" in acl_args:
                        policy["logging"] = True

                ## append to policy list

                data["policies"].append(policy)

            else:  ## other ACL types not supported

                logger.log(3, __name__ + ": ACL type " + acl_rule[2] + " not supported")

                acl_remark = ""

    for id, policy in enumerate(data["policies"]):

        ## check all source interfaces in src_interfaces

        for src_address in policy["src_addresses"]:

            ## check if a network object or group

            if (
                src_address["type"] == "group"
            ):  ## if a group use name of the first member
                name = data["network_groups"][src_address["name"]]["members"][0]

                while (
                    name in data["network_groups"]
                ):  ## repeat through nested groups until a network object found
                    name = data["network_groups"][name]["members"][0]

            else:  ## if a network object use name as is

                name = src_address["name"]

            ## resolve source interface

            if name == "any":  ## handle any

                if policy["dst_interfaces"]:

                    src_interface = "any"

                elif not policy["src_interfaces"] and not policy["dst_interfaces"]:

                    src_interface = "any"

            else:  ## handle network objects

                if data["network_objects"][name]["type"] == "host":
                    ip_address = data["network_objects"][name]["host"]

                elif data["network_objects"][name]["type"] == "network":
                    ip_address = data["network_objects"][name]["network"]

                elif data["network_objects"][name]["type"] == "range":
                    ip_address = data["network_objects"][name]["address_first"]

                ## pass to interface lookup function

                src_interface = interface_lookup(
                    ip_address, data["interfaces"], data["routes"]
                )

            ## if we have a src_interface back from lookup then add to policy

            if src_interface:

                if src_interface not in policy["src_interfaces"]:

                    data["policies"][id]["src_interfaces"].append(src_interface)

        ## check all destination interfaces in dst_interfaces

        for dst_address in policy["dst_addresses"]:

            ## check if a network object or group

            if (
                dst_address["type"] == "group"
            ):  ## if a group use name of the first member
                name = data["network_groups"][dst_address["name"]]["members"][0]

                while (
                    name in data["network_groups"]
                ):  ## repeat through nested groups until a network object found
                    name = data["network_groups"][name]["members"][0]

            else:  ## if a network object use name as is

                name = dst_address["name"]

            ## resolve destination interface

            if name == "any":  ## handle any

                if policy["src_interfaces"]:

                    dst_interface = "any"

                elif not policy["dst_interfaces"] and not policy["dst_interfaces"]:

                    dst_interface = "any"

            else:  ## handle network objects

                if data["network_objects"][name]["type"] == "host":
                    ip_address = data["network_objects"][name]["host"]

                elif data["network_objects"][name]["type"] == "network":
                    ip_address = data["network_objects"][name]["network"]

                elif data["network_objects"][name]["type"] == "range":
                    ip_address = data["network_objects"][name]["address_first"]

                ## pass to interface lookup function

                dst_interface = interface_lookup(
                    ip_address, data["interfaces"], data["routes"]
                )

            ## if we have a dst_interface back from lookup then add to policy

            if dst_interface:

                if dst_interface not in policy["dst_interfaces"]:

                    data["policies"][id]["dst_interfaces"].append(dst_interface)

    # Parse NAT

    logger.log(3, __name__ + ": parse NAT - not yet supported")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
