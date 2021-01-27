#!/usr/bin/env python

# Import modules

import logger
import sys

import re

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names
common.common_regex()
interface_lookup = common.interface_lookup

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

    names = {}

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

    # Function to resolve name object to ip address

    def lookup_name(name):

        if not names:

            # parse names

            for re_match in re.finditer(
                "name ("
                + common.common_regex.ipv4_address
                + ") ([A-Za-z0-9-_.]{1,63})(?: description (.*))?",
                src_config,
            ):

                matched_name = re_match.group(2)

                names[matched_name] = {}

                names[matched_name]["ip_address"] = re_match.group(1)

                if re_match.group(3):  ## if description found
                    names[matched_name]["description"] = re_match.group(3)

                else:  ## if description not found
                    names[matched_name]["description"] = re_match.group(3)

        # lookup name

        if name in names:  ## if name found return it

            name_object = names[name]

        else:  ## if name not found return what was passed

            name_object = {}
            name_object["ip_address"] = name
            name_object["description"] = ""

        # return name object

        return name_object

    # Function to resolve icmp type from name to type code

    def resolve_named_icmp(icmp):

        try:

            int(icmp)

        except:

            if icmp == "echo-reply":
                icmp = "0"
            elif icmp == "unreachable":
                icmp = "3"
            elif icmp == "destination-unreachable":
                icmp = "3"
            elif icmp == "source-quench":
                icmp = "4"
            elif icmp == "redirect":
                icmp = "5"
            elif icmp == "alternate-address":
                icmp = "6"
            elif icmp == "echo":
                icmp = "8"
            elif icmp == "echo-request":
                icmp = "8"
            elif icmp == "router-advertisement":
                icmp = "9"
            elif icmp == "router-solicitation":
                icmp = "10"
            elif icmp == "time-exceeded":
                icmp = "11"
            elif icmp == "parameter-problem":
                icmp = "12"
            elif icmp == "timestamp-request":
                icmp = "13"
            elif icmp == "timestamp-reply":
                icmp = "14"
            elif icmp == "information-request":
                icmp = "15"
            elif icmp == "information-reply":
                icmp = "16"
            elif icmp == "mask-request":
                icmp = "17"
            elif icmp == "mask-reply":
                icmp = "18"
            elif icmp == "traceroute":
                icmp = "30"
            elif icmp == "conversion-error":
                icmp = "31"
            elif icmp == "mobile-redirect":
                icmp = "32"

        return icmp

    # Function to resolve protocols from name to protocol number

    def resolve_named_protocol(protocol):

        try:

            int(protocol)

        except:

            if protocol == "ah":
                protocol = "51"
            elif protocol == "eigrp":
                protocol = "88"
            elif protocol == "esp":
                protocol = "50"
            elif protocol == "gre":
                protocol = "47"
            elif protocol == "icmp":
                protocol = "1"
            elif protocol == "icmp6":
                protocol = "58"
            elif protocol == "igmp":
                protocol = "2"
            elif protocol == "igrp":
                protocol = "9"
            elif protocol == "ip":
                protocol = "0"
            elif protocol == "ipinip":
                protocol = "4"
            elif protocol == "ipsec":
                protocol = "50"
            elif protocol == "nos":
                protocol = "94"
            elif protocol == "ospf":
                protocol = "89"
            elif protocol == "pcp":
                protocol = "108"
            elif protocol == "pim":
                protocol = "103"
            elif protocol == "pptp":
                protocol = "47"
            elif protocol == "snp":
                protocol = "109"
            elif protocol == "tcp":
                protocol = "6"
            elif protocol == "tcp-udp":
                protocol = "0"
            elif protocol == "udp":
                protocol = "17"

        return protocol

    # Function to resolve services from name to port number

    def resolve_named_service(service):

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
                service = "750"
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

    logger.warning(__name__ + ": parse system - not yet supported")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse interfaces

    logger.info(__name__ + ": parse interfaces")

    for re_match in re.finditer("interface (.*)\n(?: .*\n){1,}!", src_config,):

        ## split interface config and parse nameif

        interface_config = str(re_match.group(0)).split("\n")

        interface_name = re_match.group(1)

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

            if "description" in line:
                data["interfaces"][interface_name]["description"] = (
                    str(line[13:]).strip().lstrip()
                )

            ## find shutdown

            if "shutdown" in line:
                data["interfaces"][interface_name]["enabled"] = False

            ## find ip config

            if "ip address" in line and "no ip address" not in line:

                ip_address_line = line.split(" ")

                ip_config = {}
                ip_config["ip_address"] = ip_address_line[3]
                ip_config["mask"] = ip_address_line[4]

                data["interfaces"][interface_name]["ipv4_config"].append(ip_config)

            ## find vlan

            if "vlan" in line:
                data["interfaces"][interface_name]["vlan_id"] = (
                    str(line[6:]).strip().lstrip()
                )

    # Parse zones

    logger.warning(__name__ + ": parse zones - not yet supported")

    """
    Parse zones
    """

    # Parse static routes

    logger.info(__name__ + ": parse static routes")

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
        route["source"] = []
        route["type"] = "static"

        ## check if network is a name object

        name_object = lookup_name(route_config[2])

        if name_object:
            route["network"] = name_object["ip_address"]

        else:
            route["network"] = route_config[2]

        ## add to routes

        data["routes"].append(route)

    # Parse network groups

    logger.info(__name__ + ": parse network groups")

    for re_match in re.finditer("object-group network (.*)\n(?: .*\n){1,}", src_config):

        network_groups = str(re_match.group(0)).split("\n")

        network_group_name = network_groups[0][21:]

        data["network_groups"][network_group_name] = {}
        data["network_groups"][network_group_name]["description"] = ""
        data["network_groups"][network_group_name]["members"] = []
        data["network_groups"][network_group_name]["type"] = "group"

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

            if "network-object host" in member:  ## if host member

                network_object = member[21:]

                name_object = lookup_name(network_object)

                if name_object:  ## check for associated name object

                    data["network_objects"][network_object] = {}
                    data["network_objects"][network_object]["type"] = "host"
                    data["network_objects"][network_object]["host"] = name_object[
                        "ip_address"
                    ]

                    if name_object["description"]:
                        data["network_objects"][network_object][
                            "description"
                        ] = name_object["description"]

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

            elif "network-object" in member:  ## if network member

                network_config = str(member[16:]).split(" ")

                name_object = lookup_name(network_config[0])

                if network_config[1] == "255.255.255.255":  # is a host

                    network_object = network_config[0]

                    if name_object:  ## check for associated name object

                        data["network_objects"][network_object] = {}
                        data["network_objects"][network_object]["type"] = "host"
                        data["network_objects"][network_object]["host"] = name_object[
                            "ip_address"
                        ]

                        if name_object["description"]:
                            data["network_objects"][network_object][
                                "description"
                            ] = name_object["description"]

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
                        ] = name_object["ip_address"]
                        data["network_objects"][network_object][
                            "mask"
                        ] = network_config[1]

                        if name_object["description"]:
                            data["network_objects"][network_object][
                                "description"
                            ] = name_object["description"]

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

            elif "group-object" in member:  ## if group member

                network_group = member[14:]

                data["network_groups"][network_group_name]["members"].append(
                    network_group
                )

    # Parse service groups

    logger.info(__name__ + ": parse service groups")

    ## parse service groups

    for re_match in re.finditer("object-group service (.*)\n(?: .*\n){1,}", src_config):

        service_groups = str(re_match.group(0)).split("\n")

        group_config = service_groups[0][21:].split(" ")

        group_name = group_config[0]

        operator = ""

        if len(group_config) > 1:
            group_protocol = group_config[1]

        data["service_groups"][group_name] = {}
        data["service_groups"][group_name]["description"] = ""
        data["service_groups"][group_name]["members"] = []
        data["service_groups"][group_name]["type"] = "group"

        ## check for description and set start index

        if "description" in service_groups[1]:
            data["service_groups"][group_name]["description"] = service_groups[1][13:]
            i = 2

        else:
            i = 1

        ## loop through service group entries

        for member in service_groups[i:]:

            service_name = ""

            member_config = member.lstrip().split(" ")

            if member_config[0] == "port-object":  ## if port member

                if group_protocol:
                    service_name = str(group_protocol) + "_" + member_config[2]

                else:
                    service_name = member_config[2]

                operator = member_config[1]

                ## check operator

                if operator == "eq":  ## single port

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name][
                            "dst_port"
                        ] = resolve_named_service(member_config[2])
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(group_protocol)
                        data["service_objects"][service_name]["src_port"] = ""
                        data["service_objects"][service_name]["type"] = "service"

                    ## add service object to the group

                    data["service_groups"][group_name]["members"].append(service_name)

                elif operator == "range":  ## port range

                    service_name = service_name + "-" + member_config[3]

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name][
                            "dst_port_first"
                        ] = resolve_named_service(member_config[2])
                        data["service_objects"][service_name][
                            "dst_port_last"
                        ] = resolve_named_service(member_config[3])
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(group_protocol)
                        data["service_objects"][service_name]["src_port_first"] = ""
                        data["service_objects"][service_name]["src_port_last"] = ""
                        data["service_objects"][service_name]["type"] = "range"

                    ## add service object to the group

                    data["service_groups"][group_name]["members"].append(service_name)

                else:

                    logger.error(
                        __name__
                        + ": service group operator "
                        + operator
                        + " not supported",
                    )

            elif member_config[0] == "service-object":  ## if service member

                member_protocol = member_config[1]

                service_name = member_protocol

                if member_protocol in [
                    "tcp",
                    "tcp-udp",
                    "udp",
                ]:  ## if tcp or udp protocol

                    operator = member_config[2]

                    ## check operator

                    if operator == "eq":  ## single port

                        service_name = service_name + "_" + member_config[3]

                        if service_name not in data["service_objects"]:

                            data["service_objects"][service_name] = {}
                            data["service_objects"][service_name]["description"] = ""
                            data["service_objects"][service_name][
                                "dst_port"
                            ] = resolve_named_service(member_config[3])
                            data["service_objects"][service_name][
                                "protocol"
                            ] = resolve_named_protocol(member_protocol)
                            data["service_objects"][service_name]["src_port"] = ""
                            data["service_objects"][service_name]["type"] = "service"

                        ## add service object to the group

                        data["service_groups"][group_name]["members"].append(
                            service_name
                        )

                    elif operator == "range":  ## port range

                        service_name = (
                            service_name
                            + "_"
                            + member_config[3]
                            + "-"
                            + member_config[4]
                        )

                        if service_name not in data["service_objects"]:

                            data["service_objects"][service_name] = {}
                            data["service_objects"][service_name]["description"] = ""
                            data["service_objects"][service_name][
                                "dst_port_first"
                            ] = resolve_named_service(member_config[3])
                            data["service_objects"][service_name][
                                "dst_port_last"
                            ] = resolve_named_service(member_config[4])
                            data["service_objects"][service_name][
                                "protocol"
                            ] = resolve_named_protocol(group_protocol)
                            data["service_objects"][service_name]["src_port_first"] = ""
                            data["service_objects"][service_name]["src_port_last"] = ""
                            data["service_objects"][service_name]["type"] = "range"

                        ## add service object to the group

                        data["service_groups"][group_name]["members"].append(
                            service_name
                        )

                    else:

                        logger.error(
                            __name__
                            + ": service group operator "
                            + operator
                            + " not supported",
                        )

                elif member_protocol == "icmp":  ## if icmp protocol

                    if len(member_config) > 2:
                        icmp_type = member_config[2]
                        service_name = service_name + "_" + icmp_type

                    else:
                        icmp_type = ""

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name]["icmp_code"] = ""
                        data["service_objects"][service_name][
                            "icmp_type"
                        ] = resolve_named_icmp(icmp_type)
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(member_protocol)
                        data["service_objects"][service_name]["type"] = "service"

                    ## add service object to the group

                    data["service_groups"][group_name]["members"].append(service_name)

                else:  ## else another protocol

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name]["dst_port"] = ""
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(member_protocol)
                        data["service_objects"][service_name]["src_port"] = ""
                        data["service_objects"][service_name]["type"] = "service"

                    ## add service object to the group

                    data["service_groups"][group_name]["members"].append(service_name)

            elif member_config[0] == "group-object":  ## if group member

                service_group = member[14:]

                ## add group object to the group

                data["service_groups"][group_name]["members"].append(service_group)

    ## parse protocol groups

    for re_match in re.finditer(
        "object-group protocol (.*)\n(?: .*\n){1,}", src_config
    ):

        service_groups = str(re_match.group(0)).split("\n")

        group_config = service_groups[0][22:].split(" ")

        group_name = group_config[0]

        data["service_groups"][group_name] = {}
        data["service_groups"][group_name]["description"] = ""
        data["service_groups"][group_name]["members"] = []
        data["service_groups"][group_name]["type"] = "group"

        ## check for description and set start index

        if "description" in service_groups[1]:
            data["service_groups"][group_name]["description"] = service_groups[1][13:]
            i = 2

        else:
            i = 1

        for member in service_groups[i:]:

            member_config = member.lstrip().split(" ")

            if member_config[0] == "protocol-object":  ## if protocol member

                member_protocol = member_config[1]

                service_name = member_protocol

                if member_protocol == "icmp":

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name]["icmp_code"] = ""
                        data["service_objects"][service_name]["icmp_type"] = ""
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(member_protocol)
                        data["service_objects"][service_name]["type"] = "service"

                else:

                    if service_name not in data["service_objects"]:

                        data["service_objects"][service_name] = {}
                        data["service_objects"][service_name]["description"] = ""
                        data["service_objects"][service_name]["dst_port"] = ""
                        data["service_objects"][service_name][
                            "protocol"
                        ] = resolve_named_protocol(member_protocol)
                        data["service_objects"][service_name]["src_port"] = ""
                        data["service_objects"][service_name]["type"] = "service"

                ## add service object to the group

                data["service_groups"][group_name]["members"].append(service_name)

    ## parse icmp-type groups

    for re_match in re.finditer(
        "object-group icmp-type (.*)\n(?: .*\n){1,}", src_config
    ):

        service_groups = str(re_match.group(0)).split("\n")

        group_config = service_groups[0][23:].split(" ")

        group_name = group_config[0]

        data["service_groups"][group_name] = {}
        data["service_groups"][group_name]["description"] = ""
        data["service_groups"][group_name]["members"] = []
        data["service_groups"][group_name]["type"] = "group"

        ## check for description and set start index

        if "description" in service_groups[1]:
            data["service_groups"][group_name]["description"] = service_groups[1][13:]
            i = 2

        else:
            i = 1

        for member in service_groups[i:]:

            member_config = member.lstrip().split(" ")

            member_protocol = "icmp"

            if member_config[0] == "icmp-object":  ## if icmp member

                icmp_type = member_config[1]

                service_name = member_protocol + "_" + icmp_type

                if service_name not in data["service_objects"]:

                    data["service_objects"][service_name] = {}
                    data["service_objects"][service_name]["description"] = ""
                    data["service_objects"][service_name]["icmp_code"] = ""
                    data["service_objects"][service_name][
                        "icmp_type"
                    ] = resolve_named_icmp(icmp_type)
                    data["service_objects"][service_name][
                        "protocol"
                    ] = resolve_named_protocol(member_protocol)
                    data["service_objects"][service_name]["type"] = "service"

                ## add service object to the group

                data["service_groups"][group_name]["members"].append(service_name)

    # Parse firewall policies

    logger.info(__name__ + ": parse firewall policies")

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
                            ] = name_object["ip_address"]

                            if name_object["description"]:
                                data["network_objects"][network_object][
                                    "description"
                                ] = name_object["description"]

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
                                ] = name_object["ip_address"]

                                if name_object["description"]:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object["description"]

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
                                ] = name_object["ip_address"]
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]

                                if name_object["description"]:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object["description"]

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
                            ] = name_object["ip_address"]

                            if name_object["description"]:
                                data["network_objects"][network_object][
                                    "description"
                                ] = name_object["description"]

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
                                ] = name_object["ip_address"]

                                if name_object["description"]:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object["description"]

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
                                ] = name_object["ip_address"]
                                data["network_objects"][network_object][
                                    "mask"
                                ] = acl_rule[i + 1]

                                if name_object["description"]:
                                    data["network_objects"][network_object][
                                        "description"
                                    ] = name_object["description"]

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

                ## parse source services

                src_service = {}
                src_service["name"] = "any"
                src_service["type"] = "any"

                policy["src_services"].append(src_service)

                ## parse destination services

                if [i] in acl_rule:

                    if acl_rule[i] == "object":

                        dst_service = {}
                        dst_service["name"] = "any"
                        dst_service["type"] = "any"

                        policy["dst_services"].append(dst_service)

                    elif acl_rule[i] == "object-group":

                        dst_service = {}
                        dst_service["name"] = "any"
                        dst_service["type"] = "any"

                        policy["dst_services"].append(dst_service)

                    elif acl_rule[i] == "eq":

                        rule_protocol = policy["protocol"]

                        if rule_protocol in data["service_objects"]:

                            service_name = rule_protocol + "_" + acl_rule[i + 1]

                            if service_name not in data["service_objects"]:

                                data["service_objects"][service_name] = {}
                                data["service_objects"][service_name][
                                    "description"
                                ] = ""
                                data["service_objects"][service_name][
                                    "dst_port"
                                ] = resolve_named_service(acl_rule[i + 1])
                                data["service_objects"][service_name][
                                    "protocol"
                                ] = resolve_named_protocol(rule_protocol)
                                data["service_objects"][service_name]["src_port"] = ""
                                data["service_objects"][service_name][
                                    "type"
                                ] = "service"

                            dst_service = {}
                            dst_service["name"] = service_name
                            dst_service["type"] = "service"

                            policy["dst_services"].append(dst_service)

                        elif rule_protocol in data["service_objects"]:

                            for member in data["service_objects"][rule_protocol][
                                "members"
                            ]:

                                if rule_protocol == "ip":
                                    service_name = "tcp-ucp" + "_" + acl_rule[i + 1]

                                else:
                                    service_name = rule_protocol + "_" + acl_rule[i + 1]

                                if service_name not in data["service_objects"]:

                                    data["service_objects"][service_name] = {}
                                    data["service_objects"][service_name][
                                        "description"
                                    ] = ""
                                    data["service_objects"][service_name][
                                        "dst_port"
                                    ] = resolve_named_service(acl_rule[i + 1])
                                    data["service_objects"][service_name][
                                        "protocol"
                                    ] = resolve_named_protocol(rule_protocol)
                                    data["service_objects"][service_name][
                                        "src_port"
                                    ] = ""
                                    data["service_objects"][service_name][
                                        "type"
                                    ] = "service"

                                dst_service = {}
                                dst_service["name"] = service_name
                                dst_service["type"] = "service"

                                policy["dst_services"].append(dst_service)

                    elif acl_rule[i] == "range":

                        dst_service = {}
                        dst_service["name"] = "any"
                        dst_service["type"] = "any"

                        policy["dst_services"].append(dst_service)

                    else:

                        if not policy["dst_services"]:

                            dst_service = {}
                            dst_service["name"] = "any"
                            dst_service["type"] = "any"

                            policy["dst_services"].append(dst_service)

                ## check remaining entries for ACL args

                for acl_args in acl_rule[i:]:

                    if "inactive" in acl_args:
                        policy["enabled"] = False

                    if "log" in acl_args:
                        policy["logging"] = True

                ## append to policy list

                data["policies"].append(policy)

            else:  ## other ACL types not supported

                logger.warning(
                    __name__ + ": ACL type " + acl_rule[2] + " not supported"
                )

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

    logger.warning(__name__ + ": parse NAT - not yet supported")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.info(__name__ + ": parser module finished")

    return data
