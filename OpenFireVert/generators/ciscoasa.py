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

    # Generate routes

    logger.log(2, __name__ + ": generate routes")

    for route_id, attributes in parsed_data["routes"].items():

        if attributes["gateway"] != "0.0.0.0":
            dst_config.append(
                "route "
                + attributes["interface"]
                + " "
                + attributes["destination"].replace("/", " ")
                + " "
                + attributes["gateway"]
                + " "
                + attributes["distance"]
            )

    # Generate address objects

    logger.log(2, __name__ + ": generate address objects")

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

    # Generate address groups

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
                dst_config.append(" service tcp destination eq " + attributes["port"])

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(" service udp destination eq " + attributes["port"])

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
                    + attributes["port_first"]
                    + " "
                    + attributes["port_last"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("object service " + service)
                dst_config.append(
                    " service udp destination range "
                    + attributes["port_first"]
                    + " "
                    + attributes["port_last"]
                )

    # Generate service groups

    logger.log(2, __name__ + ": generate service groups")

    for group, attributes in parsed_data["service_groups"].items():

        dst_config.append("object-group service " + group)

        for member in attributes["members"]:
            dst_config.append(" service-object object " + member)

    # Generate policies

    logger.log(2, __name__ + ": generate policies - not yet supported")

    """
    Generate firewall policies
    """

    # Generate NAT

    logger.log(2, __name__ + ": generate NAT ")

    """
    Generate NAT policies
    """

    # Return generated config

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
