#!/usr/bin/env python

# Import modules

import logging
import sys
from traceback_with_variables import prints_tb, LoggerAsFile

"""
Import any modules needed here
"""

# Import common, logging and settings

import DirectFire.Converter.common as common
import DirectFire.Converter.settings as settings

# Initialise common functions

"""
Import any common functions needed here
"""

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


# Generator


def generate(parsed_data):

    logger.info(__name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generator specific variables

    """
    Generator specific variables
    """

    # Generate system

    logger.info(__name__ + ": generate system")

    try:
        dst_config.append("hostname " + parsed_data["system"]["hostname"])
    except:
        logger.warning(__name__ + ": hostname not found in parsed data")
        pass

    try:
        dst_config.append("domain-name " + data["system"]["domain"])
    except:
        logger.warning(__name__ + ": domain name not found in parsed data")
        pass

    # Generate interfaces

    logger.warning(__name__ + ": generate interfaces - not yet supported")

    """
    Generate interfaces
    """

    # Generate zones

    logger.warning(__name__ + ": generate zones - not yet supported")

    """
    Generate zones
    """

    # Generate static routes

    logger.info(__name__ + ": generate static routes")

    for route_id, attributes in enumerate(parsed_data["routes"]):

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

    logger.info(__name__ + ": generate network objects")

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

    logger.info(__name__ + ": generate network groups")

    for group, attributes in parsed_data["network_groups"].items():

        dst_config.append("object-group network " + group)

        for member in attributes["members"]:
            dst_config.append(" network-object object " + member)

    # Generate service objects

    logger.info(__name__ + ": generate service objects")

    for service, attributes in parsed_data["service_objects"].items():

        if attributes["type"] == "service":

            if attributes["protocol"] == "6":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service tcp destination eq " + attributes["dst_port"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service udp destination eq " + attributes["dst_port"]
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
                    + attributes["dst_port_first"]
                    + " "
                    + attributes["dst_port_last"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service udp destination range "
                    + attributes["dst_port_first"]
                    + " "
                    + attributes["dst_port_last"]
                )

    # Generate service groups

    logger.info(__name__ + ": generate service groups")

    for group, attributes in parsed_data["service_groups"].items():

        dst_config.append("object-group service " + group)

        for member in attributes["members"]:
            dst_config.append(" service-object object " + member)

    # Generate policies

    logger.info(__name__ + ": generate policies - not yet supported")

    # access_lists = {}

    for policy_id, attributes in enumerate(parsed_data["policies"]):

        rule_command = ""

        if attributes["action"] == "allow":
            rule_action = "permit"
        else:
            rule_action = "deny"

        rule_command = "extended " + rule_action

        ## generate destination services

        if len(attributes["dst_services"]) == 1:

            if attributes["dst_services"][0]["name"] == "any":
                rule_command = rule_command + " ip"
            else:
                if attributes["dst_services"][0]["type"] == "service":
                    rule_command = (
                        rule_command
                        + " object "
                        + attributes["dst_services"][0]["name"]
                    )
                ### range needed here?
                elif attributes["dst_services"][0]["type"] == "group":
                    rule_command = (
                        rule_command
                        + " object-group "
                        + attributes["dst_services"][0]["name"]
                    )

        else:

            ## need to create object group and reference here
            pass

        ## generate source address

        if len(attributes["src_addresses"]) == 1:

            if attributes["src_addresses"][0]["name"] == "any":
                rule_command = rule_command + " any"
            elif attributes["dst_services"][0]["type"] == "host":
                rule_command = (
                    rule_command + " object " + attributes["src_addresses"][0]["name"]
                )
            elif attributes["dst_services"][0]["type"] == "range":
                rule_command = (
                    rule_command + " object " + attributes["src_addresses"][0]["name"]
                )
            elif attributes["dst_services"][0]["type"] == "network":
                rule_command = (
                    rule_command + " object " + attributes["src_addresses"][0]["name"]
                )
            elif attributes["dst_services"][0]["type"] == "group":
                rule_command = (
                    rule_command
                    + " object-group "
                    + attributes["src_addresses"][0]["name"]
                )

        else:

            ## need to create object group and reference here
            pass

        ## generate destination address

        if len(attributes["src_addresses"]) == 1:

            if attributes["dst_addresses"][0]["name"] == "any":
                rule_command = rule_command + " any"
            elif attributes["dst_addresses"][0]["type"] == "host":
                rule_command = (
                    rule_command + " object " + attributes["dst_addresses"][0]["name"]
                )
            elif attributes["dst_addresses"][0]["type"] == "range":
                rule_command = (
                    rule_command + " object " + attributes["dst_addresses"][0]["name"]
                )
            elif attributes["dst_addresses"][0]["type"] == "network":
                rule_command = (
                    rule_command + " object " + attributes["dst_addresses"][0]["name"]
                )
            elif attributes["dst_addresses"][0]["type"] == "group":
                rule_command = (
                    rule_command
                    + " object-group "
                    + attributes["dst_addresses"][0]["name"]
                )

        else:

            ## need to create object group and reference here
            pass

        ## generate policy flags

        if attributes["logging"] == True:
            rule_command = rule_command + " log"

        if attributes["enabled"] == False:
            rule_command = rule_command + " inactive"

        ## add to acl

        if attributes["policy_set"]:

            rule_command = (
                "access-list " + attributes["policy_set"] + " " + rule_command
            )

            dst_config.append(rule_command)

        else:

            for interface in attributes["src_interfaces"]:

                rule_command = "access-list " + interface + "_in " + rule_command

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

    logger.warning(__name__ + ": generate NAT - not yet supported")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.info(__name__ + ": generator module finished")

    return dst_config
