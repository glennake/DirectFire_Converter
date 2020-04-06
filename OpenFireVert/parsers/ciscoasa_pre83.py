#!/usr/bin/env python

# Import modules

import re

# Import common, logging and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Initialise common functions

cleanse_names = common.cleanse_names


def parse(logger, src_config):

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

    # Function to resolve default services from name to port number

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

    logger.log(2, __name__ + ": parse system")

    """
    Parse system objects such as hostname, DNS
    """

    # Parse interfaces

    """
    Parse interfaces
    """

    # Parse zones

    """
    Parse zones
    """

    # Parse static routes

    logger.log(2, __name__ + ": parse static routes")

    """
    Parse static routes
    """

    # Parse IPv4 network objects

    logger.log(2, __name__ + ": parse IPv4 network objects")

    for match in re.finditer(
        r"name ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}) (\S{1,})(?: description (.{1,}))?",
        src_config,
    ):

        data["network_objects"][match.group(2)] = {}
        data["network_objects"][match.group(2)]["type"] = "host"
        data["network_objects"][match.group(2)]["host"] = match.group(1)
        data["network_objects"][match.group(2)]["description"] = match.group(3)

    # If address object is a network, change its type and seperate address / mask

    for address, attributes in data["network_objects"].items():

        for match in re.finditer(
            r"network-object "
            + address
            + " ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})",
            src_config,
        ):

            data["network_objects"][address]["type"] = "network"
            data["network_objects"][address]["network"] = attributes["host"]
            data["network_objects"][address]["mask"] = match.group(1)

    # Parse IPv6 network objects

    logger.log(2, __name__ + ": parse IPv6 network objects")

    """
    Parse IPv6 network objects
    """

    # Parse network groups

    logger.log(2, __name__ + ": parse network groups")

    for match in re.finditer(
        r"object-group network ([\S]*)[\s](?: description .*[\s])?(?: (?:network-object (?:host .*|.* [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})[\s])){1,}",
        src_config,
    ):

        data["network_groups"][match.group(1)] = {}
        data["network_groups"][match.group(1)]["type"] = "group"
        data["network_groups"][match.group(1)]["description"] = ""
        data["network_groups"][match.group(1)]["members"] = []

        network_grp_desc = re.search(r" description (.*)", match.group(0))

        if network_grp_desc:
            data["network_groups"][match.group(1)][
                "description"
            ] = network_grp_desc.group(1)

        for match2 in re.finditer(
            r"(?:network-object (?:host (.*)|(.*) [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})){1,}",
            match.group(0),
        ):

            if match2.group(1):

                data["network_groups"][match.group(1)]["members"].append(
                    match2.group(1)
                )

            if match2.group(2):

                data["network_groups"][match.group(1)]["members"].append(
                    match2.group(2)
                )

    # Parse service objects

    logger.log(2, __name__ + ": parse service objects")

    """
    Parse service objects
    """

    # Parse service groups

    logger.log(2, __name__ + ": parse service groups")

    for match in re.finditer(
        r"object-group service ([\S]*)(?: ([\S]*))?[\s](?: description .*[\s])?(?: port-object (eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?(?:[\s])?| service-object ([\S]*)(?: )?(?:[\s])?(?:(eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?(?:[\s])?)?){1,}",
        src_config,
    ):

        data["service_groups"][match.group(1)] = {}
        data["service_groups"][match.group(1)]["type"] = "group"
        data["service_groups"][match.group(1)]["protocol"] = match.group(2)
        data["service_groups"][match.group(1)]["description"] = ""
        data["service_groups"][match.group(1)]["members"] = []

        service_grp_desc = re.search(r" description (.*)", match.group(0))

        if service_grp_desc:

            data["service_groups"][match.group(1)][
                "description"
            ] = service_grp_desc.group(1)

        ### Need to add the ability to parse nested group objects in here

        # Parse port objects in service group

        for match2 in re.finditer(
            r"(?:port-object (eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?)", match.group(0)
        ):

            if match2.group(1) == "range":

                service_port_first = resolve_default_service(match2.group(2))
                service_port_last = resolve_default_service(match2.group(3))

                service_name = service_port_first + "-" + service_port_last

            else:

                service_port = resolve_default_service(match2.group(2))

                service_name = service_port

            # Break tcp-udp service entries to seperate TCP and UDP service objects

            if match.group(2) == "tcp-udp":

                # Create a TCP service object and add to service group

                data["service_objects"]["tcp_" + service_name] = {}

                data["service_objects"]["tcp_" + service_name]["protocol"] = "6"

                if match2.group(1) == "range":

                    data["service_objects"]["tcp_" + service_name]["type"] = "range"
                    data["service_objects"]["tcp_" + service_name][
                        "port_first"
                    ] = service_port_first
                    data["service_objects"]["tcp_" + service_name][
                        "port_last"
                    ] = service_port_last

                else:

                    data["service_objects"]["tcp_" + service_name]["type"] = "service"
                    data["service_objects"]["tcp_" + service_name][
                        "port"
                    ] = service_port

                data["service_groups"][match.group(1)]["members"].append(
                    "tcp_" + service_name
                )

                # Create a UDP service object and add to service group

                data["service_objects"]["udp_" + service_name] = {}

                data["service_objects"]["udp_" + service_name]["protocol"] = "17"

                if match2.group(1) == "range":

                    data["service_objects"]["udp_" + service_name]["type"] = "range"
                    data["service_objects"]["udp_" + service_name][
                        "port_first"
                    ] = service_port_first
                    data["service_objects"]["udp_" + service_name][
                        "port_last"
                    ] = service_port_last

                else:

                    data["service_objects"]["udp_" + service_name]["type"] = "service"
                    data["service_objects"]["udp_" + service_name][
                        "port"
                    ] = service_port

                data["service_groups"][match.group(1)]["members"].append(
                    "udp_" + service_name
                )

            # Process single protocol service entries

            else:

                service_name = match.group(2) + "_" + service_name

                data["service_objects"][service_name] = {}

                data["service_objects"][service_name]["protocol"] = match.group(2)

                if match2.group(1) == "range":

                    data["service_objects"][service_name]["type"] = "range"
                    data["service_objects"][service_name][
                        "port_first"
                    ] = service_port_first
                    data["service_objects"][service_name][
                        "port_last"
                    ] = service_port_last

                else:

                    data["service_objects"][service_name]["type"] = "service"
                    data["service_objects"][service_name]["port"] = service_port

                data["service_groups"][match.group(1)]["members"].append(service_name)

        # Parse service objects in service group

        for match2 in re.finditer(
            r"service-object ([\S]*)(?:[\s])?(?:(eq|gt|lt|neq|range) ([\S]*)(?: ([\S]*))?)?",
            match.group(0),
        ):

            if match2.group(2):

                if match2.group(1) == "range":

                    service_port_first = resolve_default_service(match2.group(3))
                    service_port_last = resolve_default_service(match2.group(4))

                    service_name = (
                        match2.group(1)
                        + "_"
                        + service_port_first
                        + "-"
                        + service_port_last
                    )

                else:

                    service_port = resolve_default_service(match2.group(3))

                    service_name = match2.group(1) + "_" + service_port

            else:

                service_name = match2.group(1) + "_all"

            ### Need to add the ability to parse ICMP services with type and code values in here

            if match2.group(2):

                data["service_objects"][service_name] = {}

                data["service_objects"][service_name]["protocol"] = match2.group(1)

                if match2.group(2) == "range":

                    data["service_objects"][service_name]["type"] = "range"
                    data["service_objects"][service_name][
                        "port_first"
                    ] = service_port_first
                    data["service_objects"][service_name][
                        "port_last"
                    ] = service_port_last

                else:

                    data["service_objects"][service_name]["type"] = "service"
                    data["service_objects"][service_name]["port"] = service_port

            else:

                data["service_objects"][service_name] = {}
                data["service_objects"][service_name]["type"] = "service"
                data["service_objects"][service_name]["protocol"] = match2.group(1)

            if match2.group(1) == "icmp":

                data["service_objects"][service_name]["icmp_type"] = ""
                data["service_objects"][service_name]["icmp_code"] = ""

            data["service_groups"][match.group(1)]["members"].append(service_name)

        ### Need to parse protocol groups here

    # Parse firewall policies

    logger.log(2, __name__ + ": parse firewall policies")

    for match in re.finditer(
        r"access-list ([\S]{1,}) (remark .*|extended (permit|deny) ([a-z0-9]{1,6}|object-group [\S]{1,}) (host [\S]{1,}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|[\S]{1,} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|object-group [\S]*(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|interface(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|any(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?) (host [\S]{1,}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|[\S]{1,} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|object-group [\S]*(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|interface(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?|any(?: (?:eq|gt|lt|neq|range [\S]{1,}) [\S]{1,}| object-group [\S]{1,})?)(?: (log))?(?: (disable))?(?: (inactive))?)",
        src_config,
    ):

        if match.group(1) not in data["policies"]:

            data["policies"][match.group(1)] = {}

        data["policies"][match.group(1)][policy_id] = {}

        data["policies"][match.group(1)][policy_id]["id"] = policy_id
        data["policies"][match.group(1)][policy_id]["type"] = "policy"
        data["policies"][match.group(1)][policy_id]["src_interface"] = ""
        data["policies"][match.group(1)][policy_id]["dst_interface"] = ""
        data["policies"][match.group(1)][policy_id]["protocol"] = match.group(4)
        data["policies"][match.group(1)][policy_id]["src_address"] = ""
        data["policies"][match.group(1)][policy_id]["src_address_type"] = ""
        data["policies"][match.group(1)][policy_id]["dst_address"] = ""
        data["policies"][match.group(1)][policy_id]["dst_address_type"] = ""
        data["policies"][match.group(1)][policy_id]["src_service"] = ""
        data["policies"][match.group(1)][policy_id]["src_service_type"] = ""
        data["policies"][match.group(1)][policy_id]["dst_service"] = ""
        data["policies"][match.group(1)][policy_id]["dst_service_type"] = ""
        data["policies"][match.group(1)][policy_id]["action"] = match.group(3)
        data["policies"][match.group(1)][policy_id]["disabled"] = False
        data["policies"][match.group(1)][policy_id]["logging"] = False
        data["policies"][match.group(1)][policy_id]["comment"] = ""

        # Check if the entry is a remark

        if "remark" in match.group(2):

            data["policies"][match.group(1)][policy_id]["type"] = "remark"
            data["policies"][match.group(1)][policy_id]["comment"] = match.group(2)[7:]

        # If not then get all policy objects

        else:

            ### Need to add checks for policy service object group, protocol group and single protocol

            # Get source address(es) and port(s) if applicable

            policy_src_any = re.search(
                r"^(any)(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(5),
            )
            policy_src_group = re.search(
                r"object-group ([\S]*)(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(5),
            )
            policy_src_addr = re.search(
                r"([\S]{1,}) (?:(?:(?:255\.){3}(?:255|254|252|248|240|224|192|128|0+))|(?:(?:255\.){2}(?:255|254|252|248|240|224|192|128|0+)\.0)|(?:(?:255\.)(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){2})|(?:(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){3}))(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(5),
            )
            policy_src_host = re.search(
                r"host ([\S]{1,})(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(5),
            )
            policy_src_manual = re.search(
                r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(5),
            )

            # Check if any and parse vars

            if policy_src_any:

                data["policies"][match.group(1)][policy_id]["src_address"] = "any"
                data["policies"][match.group(1)][policy_id]["src_address_type"] = "any"
                policy_src = policy_src_any

            # Check if groups and parse vars

            if policy_src_group:

                data["policies"][match.group(1)][policy_id][
                    "src_address"
                ] = policy_src_group.group(1)
                data["policies"][match.group(1)][policy_id][
                    "src_address_type"
                ] = "group"
                policy_src = policy_src_group

            # Check if network object and parse vars

            if policy_src_addr:

                data["policies"][match.group(1)][policy_id][
                    "src_address"
                ] = policy_src_addr.group(1)
                data["policies"][match.group(1)][policy_id]["src_address_type"] = "host"
                policy_src = policy_src_addr

            # Check if host and parse vars

            if policy_src_host:

                data["policies"][match.group(1)][policy_id][
                    "src_address"
                ] = policy_src_host.group(1)
                data["policies"][match.group(1)][policy_id]["src_address_type"] = "host"
                policy_src = policy_src_host

            # Check if directly specified and parse vars

            ### Should probably create and reference a network object here

            if policy_src_manual:

                data["policies"][match.group(1)][policy_id][
                    "src_address"
                ] = policy_src_manual.group(1).replace(" ", "/")
                data["policies"][match.group(1)][policy_id][
                    "src_address_type"
                ] = "manual"
                policy_src = policy_src_manual

            # If we have a source address then look for source service

            if data["policies"][match.group(1)][policy_id]["src_address"]:

                if policy_src[2]:

                    if policy_src[2] == "object-group":

                        data["policies"][match.group(1)][policy_id][
                            "src_service"
                        ] = policy_src[3]
                        data["policies"][match.group(1)][policy_id][
                            "src_service_type"
                        ] = "group"

                    elif policy_src[2] == "range":

                        ### Should probably create and reference a service object here

                        data["policies"][match.group(1)][policy_id]["src_service"] = (
                            resolve_default_service(policy_src[3])
                            + "-"
                            + resolve_default_service(policy_src[4])
                        )
                        data["policies"][match.group(1)][policy_id][
                            "src_service_type"
                        ] = "range"

                    elif policy_src[2] == "eq":

                        data["policies"][match.group(1)][policy_id][
                            "src_service"
                        ] = resolve_default_service(policy_src[3])
                        data["policies"][match.group(1)][policy_id][
                            "src_service_type"
                        ] = "service"

                    ### Need to add support for other operators here - gt, lt, neq

                else:

                    data["policies"][match.group(1)][policy_id]["src_service"] = "any"
                    data["policies"][match.group(1)][policy_id][
                        "src_service_type"
                    ] = "any"

            # Get destination address(es) and port(s) if applicable

            policy_dst_any = re.search(
                r"^(any)(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(6),
            )
            policy_dst_group = re.search(
                r"object-group ([\S]*)(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(6),
            )
            policy_dst_addr = re.search(
                r"([\S]{1,}) (?:(?:(?:255\.){3}(?:255|254|252|248|240|224|192|128|0+))|(?:(?:255\.){2}(?:255|254|252|248|240|224|192|128|0+)\.0)|(?:(?:255\.)(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){2})|(?:(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){3}))(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(6),
            )
            policy_dst_host = re.search(
                r"host ([\S]{1,})(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(6),
            )
            policy_dst_manual = re.search(
                r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(?: (eq|gt|lt|neq|range|object-group) ([\S]{1,})(?: ([\S]{1,}))?)?",
                match.group(6),
            )

            # Check if any and parse vars

            if policy_dst_any:

                data["policies"][match.group(1)][policy_id]["dst_address"] = "any"
                data["policies"][match.group(1)][policy_id]["dst_address_type"] = "any"
                policy_dst = policy_dst_any

            # Check if group and parse vars

            if policy_dst_group:

                data["policies"][match.group(1)][policy_id][
                    "dst_address"
                ] = policy_dst_group.group(1)
                data["policies"][match.group(1)][policy_id][
                    "dst_address_type"
                ] = "group"
                policy_dst = policy_dst_group

            # Check if network object and parse vars

            if policy_dst_addr:

                data["policies"][match.group(1)][policy_id][
                    "dst_address"
                ] = policy_dst_addr.group(1)
                data["policies"][match.group(1)][policy_id]["dst_address_type"] = "host"
                policy_dst = policy_dst_addr

            # Check if host and parse vars

            if policy_dst_host:

                data["policies"][match.group(1)][policy_id][
                    "dst_address"
                ] = policy_dst_host.group(1)
                data["policies"][match.group(1)][policy_id]["dst_address_type"] = "host"
                policy_dst = policy_dst_host

            # Check if directly specified and parse vars

            ### Should probably create and reference a network object here

            if policy_dst_manual:

                data["policies"][match.group(1)][policy_id][
                    "dst_address"
                ] = policy_dst_manual.group(1).replace(" ", "/")
                data["policies"][match.group(1)][policy_id][
                    "dst_address_type"
                ] = "manual"
                policy_dst = policy_dst_manual

            # If we have a destination address then look for destination service

            if data["policies"][match.group(1)][policy_id]["dst_address"]:

                if policy_dst[2]:

                    if policy_dst[2] == "object-group":

                        data["policies"][match.group(1)][policy_id][
                            "dst_service"
                        ] = policy_dst[3]
                        data["policies"][match.group(1)][policy_id][
                            "dst_service_type"
                        ] = "group"

                    elif policy_dst[2] == "range":

                        ### Should probably create and reference a service object here

                        data["policies"][match.group(1)][policy_id]["dst_service"] = (
                            resolve_default_service(policy_dst[3])
                            + "-"
                            + resolve_default_service(policy_dst[4])
                        )
                        data["policies"][match.group(1)][policy_id][
                            "dst_service_type"
                        ] = "range"

                    elif policy_dst[2] == "eq":

                        data["policies"][match.group(1)][policy_id][
                            "dst_service"
                        ] = resolve_default_service(policy_dst[3])
                        data["policies"][match.group(1)][policy_id][
                            "dst_service_type"
                        ] = "service"

                    ### Need to add support for other operators here - gt, lt, neq

                else:

                    data["policies"][match.group(1)][policy_id]["dst_service"] = "any"
                    data["policies"][match.group(1)][policy_id][
                        "dst_service_type"
                    ] = "any"

            # Check if logging enabled

            if match.group(7) == "log":

                data["policies"][match.group(1)][policy_id]["logging"] = True

            # Check if policy disabled

            if match.group(8) == "disable":

                data["policies"][match.group(1)][policy_id]["disabled"] = True

            # Check if policy inactive

            if match.group(9) == "inactive":

                data["policies"][match.group(1)][policy_id]["disabled"] = True

        policy_id += 1

    # Parse NAT

    logger.log(3, __name__ + ": parse NAT not yet implemented")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
