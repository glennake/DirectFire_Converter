#!/usr/bin/env python

# Import modules

"""
Import any modules needed here
"""

# Import common, logging and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Initialise common functions

"""
Import any common functions needed here
"""


def generate(logger, parsed_data):

    logger.log(2, __name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generate system

    logger.log(2, __name__ + ": generate system")

    try:
        dst_config.append("hostname " + parsed_data["system"]["hostname"])
    except:
        logger.log(3, __name__ + ": hostname not found in parsed data")
        pass

    try:
        dst_config.append("domain-name " + data["system"]["domain"])
    except:
        logger.log(3, __name__ + ": domain name not found in parsed data")
        pass

    # Generate interfaces

    logger.log(2, __name__ + ": generate interfaces")

    """
    Generate interfaces
    """

    # Generate zones

    logger.log(2, __name__ + ": generate zones")

    """
    Generate zones
    """

    # Generate static routes

    logger.log(2, __name__ + ": generate static routes")

    for route_id, attributes in parsed_data["routes"].items():

        if attributes["gateway"] != "0.0.0.0":
            dst_config.append(
                "route "
                + attributes["interface"]
                + " "
                + attributes["network"]
                + " "
                + attributes["mask"]
                + " "
                + attributes["gateway"]
                + " "
                + attributes["distance"]
            )

    # Generate network objects

    logger.log(2, __name__ + ": generate network objects")

    for address, attributes in parsed_data["network_objects"].items():

        if attributes["type"] == "host":

            dst_config.append("object network " + address)
            dst_config.append(" host " + attributes["host"])

        elif attributes["type"] == "network":

            dst_config.append("object network " + address)
            dst_config.append(
                " subnet " + attributes["network"] + " " + attributes["mask"]
            )

        elif attributes["type"] == "range":

            dst_config.append("object network " + address)
            dst_config.append(
                " range "
                + attributes["address_first"]
                + " "
                + attributes["address_last"]
            )

        elif attributes["type"] == "domain":

            dst_config.append("object network " + address)
            dst_config.append(" fqdn " + attributes["fqdn"])

    # Generate network groups

    logger.log(2, __name__ + ": generate network groups")

    for group, attributes in parsed_data["network_groups"].items():

        dst_config.append("object-group network " + group)

        for member in attributes["members"]:
            dst_config.append(" network-object object " + member)

    # Generate service objects

    logger.log(2, __name__ + ": generate service objects")

    for service, attributes in parsed_data["service_objects"].items():

        if attributes["type"] == "service":

            if attributes["protocol"] == "6":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service tcp destination eq " + attributes["destination_port"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service udp destination eq " + attributes["destination_port"]
                )

            elif attributes["protocol"] == "1":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service icmp "
                    + attributes["icmp_type"]
                    + " "
                    + attributes["icmp_code"]
                )

        elif attributes["type"] == "range":

            if attributes["protocol"] == "6":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service tcp destination range "
                    + attributes["destination_port_first"]
                    + " "
                    + attributes["destination_port_last"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service udp destination range "
                    + attributes["destination_port_first"]
                    + " "
                    + attributes["destination_port_last"]
                )

    # Generate service groups

    logger.log(2, __name__ + ": generate service groups")

    for group, attributes in parsed_data["service_groups"].items():

        dst_config.append("object-group service " + group)

        for member in attributes["members"]:
            dst_config.append(" service-object object " + member)

    # Generate policies

    logger.log(2, __name__ + ": generate policies - not yet supported")

    access_lists = {}

    for policy, attributes in parsed_data["policies"].items():

        rule_command = ""

        if attributes["action"] == "allow":
            rule_action = "permit"
        else:
            rule_action = "deny"

        rule_command = "extended " + rule_action

        if attributes["dst_service"] == "any":
            rule_command = rule_command + " ip"
        else:
            if attributes["dst_service_type"] == "service":
                rule_command = rule_command + " object " + attributes["dst_service"]
            ### range needed here?
            elif attributes["dst_service_type"] == "group":
                rule_command = (
                    rule_command + " object-group " + attributes["dst_service"]
                )

        if attributes["src_address"] == "any":
            rule_command = rule_command + " any"
        elif attributes["src_address_type"] == "name":
            rule_command = rule_command + " object " + attributes["src_address"]
        elif attributes["src_address_type"] == "group":
            rule_command = rule_command + " object-group " + attributes["src_address"]

        if attributes["dst_address"] == "any":
            rule_command = rule_command + " any"
        elif attributes["dst_address_type"] == "name":
            rule_command = rule_command + " object " + attributes["dst_address"]
        elif attributes["dst_address_type"] == "group":
            rule_command = rule_command + " object-group " + attributes["dst_address"]

        if attributes["logging"] == True:
            rule_command = rule_command + " log"

        if attributes["enabled"] == False:
            rule_command = rule_command + " inactive"

        if attributes["policy_set"]:

            rule_command = (
                "access-list " + attributes["policy_set"] + " " + rule_command
            )

        else:

            rule_command = (
                "access-list " + attributes["src_interface"] + "_in " + rule_command
            )

        dst_config.append(rule_command)

    #     if attributes["src_interface"] not in access_lists:
    #         access_lists[attributes["src_interface"]] = []

    #     access_lists[attributes["src_interface"]].append(rule_command)

    # for access_list, commands in access_lists.items():
    #     for command in commands:
    #         dst_config.append(command)

    # for access_list in access_lists.keys():
    #     dst_config.append(
    #         "access-group " + access_list + "_in in interface " + access_list
    #     )

    # Generate NAT

    logger.log(2, __name__ + ": generate NAT ")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
