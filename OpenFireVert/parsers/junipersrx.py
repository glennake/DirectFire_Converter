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
ipv4_prefix_to_mask = common.ipv4_prefix_to_mask


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

    # Define default services

    default_services = {}

    default_services["any"] = {}
    default_services["any"]["protocol"] = "ip"
    default_services["any"]["type"] = "object"

    default_services["junos-icmp-all"] = {}
    default_services["junos-icmp-all"]["protocol"] = "icmp"
    default_services["junos-icmp-all"]["direction"] = "destination"
    default_services["junos-icmp-all"]["port"] = ""
    default_services["junos-icmp-all"]["type"] = "object"

    default_services["junos-icmp-ping"] = {}
    default_services["junos-icmp-ping"]["protocol"] = "icmp"
    default_services["junos-icmp-ping"]["direction"] = "destination"
    default_services["junos-icmp-ping"]["port"] = "echo"
    default_services["junos-icmp-ping"]["type"] = "object"

    default_services["junos-ssh"] = {}
    default_services["junos-ssh"]["protocol"] = "tcp"
    default_services["junos-ssh"]["direction"] = "destination"
    default_services["junos-ssh"]["port"] = "22"
    default_services["junos-ssh"]["type"] = "object"

    default_services["junos-http"] = {}
    default_services["junos-http"]["protocol"] = "tcp"
    default_services["junos-http"]["direction"] = "destination"
    default_services["junos-http"]["port"] = "80"
    default_services["junos-http"]["type"] = "object"

    default_services["junos-https"] = {}
    default_services["junos-https"]["protocol"] = "tcp"
    default_services["junos-https"]["direction"] = "destination"
    default_services["junos-https"]["port"] = "443"
    default_services["junos-https"]["type"] = "object"

    default_services["junos-smtp"] = {}
    default_services["junos-smtp"]["protocol"] = "tcp"
    default_services["junos-smtp"]["direction"] = "destination"
    default_services["junos-smtp"]["port"] = "25"
    default_services["junos-smtp"]["type"] = "object"

    default_services["junos-radius"] = {}
    default_services["junos-radius"]["protocol"] = "udp"
    default_services["junos-radius"]["direction"] = "destination"
    default_services["junos-radius"]["port"] = "1812"
    default_services["junos-radius"]["type"] = "object"

    default_services["junos-radacct"] = {}
    default_services["junos-radacct"]["protocol"] = "udp"
    default_services["junos-radacct"]["direction"] = "destination"
    default_services["junos-radacct"]["port"] = "1813"
    default_services["junos-radacct"]["type"] = "object"

    default_services["junos-syslog"] = {}
    default_services["junos-syslog"]["protocol"] = "udp"
    default_services["junos-syslog"]["direction"] = "destination"
    default_services["junos-syslog"]["port"] = "161"
    default_services["junos-syslog"]["type"] = "object"

    default_services["junos-ntp"] = {}
    default_services["junos-ntp"]["protocol"] = "udp"
    default_services["junos-ntp"]["direction"] = "destination"
    default_services["junos-ntp"]["port"] = "123"
    default_services["junos-ntp"]["type"] = "object"

    default_services["junos-ftp"] = {}
    default_services["junos-ftp"]["protocol"] = "tcp"
    default_services["junos-ftp"]["direction"] = "destination"
    default_services["junos-ftp"]["port"] = "21"
    default_services["junos-ftp"]["type"] = "object"

    default_services["junos-telnet"] = {}
    default_services["junos-telnet"]["protocol"] = "tcp"
    default_services["junos-telnet"]["direction"] = "destination"
    default_services["junos-telnet"]["port"] = "23"
    default_services["junos-telnet"]["type"] = "object"

    default_services["junos-ms-sql"] = {}
    default_services["junos-ms-sql"]["protocol"] = "tcp"
    default_services["junos-ms-sql"]["direction"] = "destination"
    default_services["junos-ms-sql"]["port"] = "1433"
    default_services["junos-ms-sql"]["type"] = "object"

    default_services["junos-smb-session"] = {}
    default_services["junos-smb-session"]["protocol"] = "tcp"
    default_services["junos-smb-session"]["direction"] = "destination"
    default_services["junos-smb-session"]["port"] = "445"
    default_services["junos-smb-session"]["type"] = "object"

    default_services["junos-ms-rpc"] = {}
    default_services["junos-ms-rpc"]["protocol"] = "tcp"
    default_services["junos-ms-rpc"]["direction"] = "destination"
    default_services["junos-ms-rpc"]["port"] = "135"
    default_services["junos-ms-rpc"]["type"] = "object"

    default_services["junos-ms-rpc-tcp"] = {}
    default_services["junos-ms-rpc-tcp"]["protocol"] = "tcp"
    default_services["junos-ms-rpc-tcp"]["direction"] = "destination"
    default_services["junos-ms-rpc-tcp"]["port"] = "135"
    default_services["junos-ms-rpc-tcp"]["type"] = "object"

    default_services["junos-ms-rpc-udp"] = {}
    default_services["junos-ms-rpc-udp"]["protocol"] = "udp"
    default_services["junos-ms-rpc-udp"]["direction"] = "destination"
    default_services["junos-ms-rpc-udp"]["port"] = "135"
    default_services["junos-ms-rpc-udp"]["type"] = "object"

    default_services["junos-ldap"] = {}
    default_services["junos-ldap"]["protocol"] = "tcp"
    default_services["junos-ldap"]["direction"] = "destination"
    default_services["junos-ldap"]["port"] = "389"
    default_services["junos-ldap"]["type"] = "object"

    default_services["junos-nbname"] = {}
    default_services["junos-nbname"]["protocol"] = "udp"
    default_services["junos-nbname"]["direction"] = "destination"
    default_services["junos-nbname"]["port"] = "137"
    default_services["junos-nbname"]["type"] = "object"

    default_services["junos-dns-udp"] = {}
    default_services["junos-dns-udp"]["protocol"] = "udp"
    default_services["junos-dns-udp"]["direction"] = "destination"
    default_services["junos-dns-udp"]["port"] = "53"
    default_services["junos-dns-udp"]["type"] = "object"

    default_services["junos-dns-tcp"] = {}
    default_services["junos-dns-tcp"]["protocol"] = "tcp"
    default_services["junos-dns-tcp"]["direction"] = "destination"
    default_services["junos-dns-tcp"]["port"] = "53"
    default_services["junos-dns-tcp"]["type"] = "object"

    default_services["junos-pop3"] = {}
    default_services["junos-pop3"]["protocol"] = "tcp"
    default_services["junos-pop3"]["direction"] = "destination"
    default_services["junos-pop3"]["port"] = "110"
    default_services["junos-pop3"]["type"] = "object"

    default_services["junos-imap"] = {}
    default_services["junos-imap"]["protocol"] = "tcp"
    default_services["junos-imap"]["direction"] = "destination"
    default_services["junos-imap"]["port"] = "143"
    default_services["junos-imap"]["type"] = "object"

    default_services["junos-ike"] = {}
    default_services["junos-ike"]["protocol"] = "udp"
    default_services["junos-ike"]["direction"] = "destination"
    default_services["junos-ike"]["port"] = "500"
    default_services["junos-ike"]["type"] = "object"

    default_services["junos-tacacs"] = {}
    default_services["junos-tacacs"]["protocol"] = "tcp"
    default_services["junos-tacacs"]["direction"] = "destination"
    default_services["junos-tacacs"]["port"] = "49"
    default_services["junos-tacacs"]["type"] = "object"

    default_services["junos-tacacs-ds"] = {}
    default_services["junos-tacacs-ds"]["protocol"] = "tcp"
    default_services["junos-tacacs-ds"]["direction"] = "destination"
    default_services["junos-tacacs-ds"]["port"] = "65"
    default_services["junos-tacacs-ds"]["type"] = "object"

    default_services["junos-tftp"] = {}
    default_services["junos-tftp"]["protocol"] = "udp"
    default_services["junos-tftp"]["direction"] = "destination"
    default_services["junos-tftp"]["port"] = "69"
    default_services["junos-tftp"]["type"] = "object"

    default_services["junos-nfs"] = {}
    default_services["junos-nfs"]["protocol"] = "udp"
    default_services["junos-nfs"]["direction"] = "destination"
    default_services["junos-nfs"]["port"] = "111"
    default_services["junos-nfs"]["type"] = "object"

    default_services["junos-nfsd-tcp"] = {}
    default_services["junos-nfsd-tcp"]["protocol"] = "udp"
    default_services["junos-nfsd-tcp"]["direction"] = "destination"
    default_services["junos-nfsd-tcp"]["port"] = "2049"
    default_services["junos-nfsd-tcp"]["type"] = "object"

    default_services["junos-nfsd-udp"] = {}
    default_services["junos-nfsd-udp"]["protocol"] = "udp"
    default_services["junos-nfsd-udp"]["direction"] = "destination"
    default_services["junos-nfsd-udp"]["port"] = "2049"
    default_services["junos-nfsd-udp"]["type"] = "object"

    default_services["junos-netbios-session"] = {}
    default_services["junos-netbios-session"]["protocol"] = "tcp"
    default_services["junos-netbios-session"]["direction"] = "destination"
    default_services["junos-netbios-session"]["port"] = "139"
    default_services["junos-netbios-session"]["type"] = "object"

    default_services["junos-winframe"] = {}
    default_services["junos-winframe"]["protocol"] = "tcp"
    default_services["junos-winframe"]["direction"] = "destination"
    default_services["junos-winframe"]["port"] = "1494"
    default_services["junos-winframe"]["type"] = "object"

    default_services["junos-sccp"] = {}
    default_services["junos-sccp"]["protocol"] = "tcp"
    default_services["junos-sccp"]["direction"] = "destination"
    default_services["junos-sccp"]["port"] = "2000"
    default_services["junos-sccp"]["type"] = "object"

    # default_services['junos-'] = {}
    # default_services['junos-']['protocol'] = ''
    # default_services['junos-']['direction'] = ''
    # default_services['junos-']['port'] = ''
    # default_services['junos-']['type'] = 'object'

    # Parse system

    logger.log(2, __name__ + ": parse system")

    re_match = re.search("set system host-name (.*?)\n", src_config)

    if re_match:
        data["system"]["hostname"] = re_match.group(1)

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

    for route_match in re.finditer(
        "set routing-options static route ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ") next-hop ("
        + common.common_regex.ipv4_address
        + ")",
        src_config,
    ):

        route_network = route_match.group(1)
        route_prefix = route_match.group(2)
        route_gateway = route_match.group(3)

        data["routes"][route_id] = {}

        data["routes"][route_id]["network"] = route_network
        data["routes"][route_id]["mask"] = ipv4_prefix_to_mask(route_prefix)
        data["routes"][route_id]["gateway"] = route_gateway

        re_match = re.search(
            "set routing-options static route "
            + route_network
            + route_prefix
            + " preference ([0-9]{1,3})",
            src_config,
        )

        if re_match:
            data["routes"][route_id]["distance"] = re_match.group(1)
        else:
            data["routes"][route_id][
                "distance"
            ] = "5"  ## default admin distance for static routes is 5

        data["routes"][route_id]["type"] = "static"

        route_id += 1

    # Parse IPv4 network objects

    logger.log(2, __name__ + ": parse IPv4 network objects")

    ## host and network objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) ("
        + common.common_regex.ipv4_address
        + ")("
        + common.common_regex.ipv4_prefix
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_network = re_match.group(2)
        network_object_prefix = re_match.group(3)

        data["network_objects"][network_object_name] = {}

        if network_object_prefix == "/32":

            data["network_objects"][network_object_name]["type"] = "host"
            data["network_objects"][network_object_name][
                "host"
            ] = network_object_network

        else:

            data["network_objects"][network_object_name]["type"] = "network"
            data["network_objects"][network_object_name][
                "network"
            ] = network_object_network
            data["network_objects"][network_object_name]["mask"] = ipv4_prefix_to_mask(
                network_object_prefix
            )

    ## fqdn objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) dns-name ("
        + common.common_regex.fqdn
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_fqdn = re_match.group(2)

        data["network_objects"][network_object_name] = {}

        data["network_objects"][network_object_name]["type"] = "fqdn"
        data["network_objects"][network_object_name]["fqdn"] = network_object_fqdn

    ## range objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address (.*?) range-address ("
        + common.common_regex.ipv4_address
        + ") to ("
        + common.common_regex.ipv4_address
        + ")\n",
        src_config,
    ):

        network_object_name = re_match.group(1)
        network_object_address_first = re_match.group(2)
        network_object_address_last = re_match.group(3)

        data["network_objects"][network_object_name] = {}

        data["network_objects"][network_object_name]["type"] = "range"
        data["network_objects"][network_object_name][
            "address_first"
        ] = network_object_address_first
        data["network_objects"][network_object_name][
            "address_last"
        ] = network_object_address_last

    ## find description

    for network_object in data["network_objects"].keys():

        re_match = re.search(
            "address " + network_object + ' description "?(.*?)"?\n', src_config
        )

        if re_match:
            data["network_objects"][network_object]["description"] = re_match.group(1)

        else:
            data["network_objects"][network_object]["description"] = ""

    # Parse IPv6 network objects

    logger.log(2, __name__ + ": parse IPv6 network objects - not yet supported")

    """
    Parse IPv6 network objects
    """

    # Parse IPv4 network groups

    logger.log(2, __name__ + ": parse IPv4 network groups - not yet supported")

    ## address sets with address objects

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address-set (.*?) address (.*?)\n",
        src_config,
    ):

        network_group_name = re_match.group(1)
        network_group_member = re_match.group(2)

        if network_group_name in data["network_groups"]:
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

        else:
            data["network_groups"][network_group_name] = {}
            data["network_groups"][network_group_name]["members"] = []
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

    ## address sets with nested address sets

    for re_match in re.finditer(
        "set security (?:zones security-zone (?:.*?) )?address-book(?: global)? address-set (.*?) address-set (.*?)\n",
        src_config,
    ):

        network_group_name = re_match.group(1)
        network_group_member = re_match.group(2)

        if network_group_name in data["network_groups"]:
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

        else:
            data["network_groups"][network_group_name] = {}
            data["network_groups"][network_group_name]["members"] = []
            data["network_groups"][network_group_name]["members"].append(
                network_group_member
            )

    ## find description

    for network_group in data["network_groups"].keys():

        re_match = re.search(
            "address-set " + network_group + ' description "?(.*?)"?\n', src_config
        )

        if re_match:
            data["network_groups"][network_group]["description"] = re_match.group(1)

        else:
            data["network_groups"][network_group]["description"] = ""

    # Parse IPv6 network groups

    logger.log(2, __name__ + ": parse IPv6 network groups - not yet supported")

    """
    Parse IPv6 network groups
    """

    # Parse service objects

    logger.log(2, __name__ + ": parse service objects - not yet supported")

    """
    Parse service objects
    """

    # Parse service groups

    logger.log(2, __name__ + ": parse service groups - not yet supported")

    """
    Parse service groups
    """

    # Parse firewall policies

    logger.log(2, __name__ + ": parse firewall policies - not yet supported")

    """
    Parse firewall policies
    """

    ## remember any, any-ipv4 and any-ipv6

    # Parse NAT

    logger.log(2, __name__ + ": parse NAT - not yet supported")

    """
    Parse NAT policies
    """

    # Return parsed data

    logger.log(2, __name__ + ": parser module finished")

    return data
