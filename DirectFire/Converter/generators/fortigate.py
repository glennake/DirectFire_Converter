#!/usr/bin/env python

# Import modules

import logging
import sys

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


# Generator

def generate(parsed_data):

    logger.info(__name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generator specific variables

    cfglvl1 = "  "
    cfglvl2 = "    "
    cfglvl3 = "      "
    cfglvl4 = "        "
    cfglvl5 = "          "

    # Generate system

    logger.info(__name__ + ": generate system")

    dst_config.append("config system global")

    if "hostname" in parsed_data["system"]:
        dst_config.append(cfglvl1 + "set hostname " + parsed_data["system"]["hostname"])
    else:
        logger.warning(__name__ + ": hostname not found in parsed data")

    dst_config.append("end")

    dst_config.append("config system dns")

    if "domain" in parsed_data["system"]:
        dst_config.append(cfglvl1 + "set domain " + parsed_data["system"]["domain"])
    else:
        logger.warning(__name__ + ": domain name not found in parsed data")

    dst_config.append("end")

    # Generate interfaces

    logger.info(__name__ + ": generate interfaces")

    dst_config.append("config system interface")

    logger.info(
        __name__
        + ": interfaces: found "
        + str(len(parsed_data["interfaces"]))
        + " interfaces"
    )

    for interface, attributes in parsed_data["interfaces"].items():

        logger.info(__name__ + ": interfaces: generating " + interface)

        if attributes["type"] == "interface":

            dst_config.append(cfglvl1 + "edit " + interface)
            dst_config.append(cfglvl2 + "set vdom root")

            if attributes["ipv4_config"]:

                dst_config.append(cfglvl2 + "set mode static")

                last_ipv4 = len(attributes["ipv4_config"]) - 1

                for i in range(len(attributes["ipv4_config"])):

                    if i == 0:

                        dst_config.append(
                            cfglvl2
                            + "set ip "
                            + attributes["ipv4_config"][i]["ip_address"]
                            + " "
                            + attributes["ipv4_config"][i]["mask"]
                        )

                    else:

                        if i == 1:

                            dst_config.append(cfglvl2 + "set secondary-IP enable")
                            dst_config.append(cfglvl2 + "config secondaryip")

                        dst_config.append(cfglvl3 + "edit " + str(i))
                        dst_config.append(
                            cfglvl4
                            + "set ip "
                            + attributes["ipv4_config"][i]["ip_address"]
                            + " "
                            + attributes["ipv4_config"][i]["mask"]
                        )
                        dst_config.append(cfglvl3 + "next")

                        if i == last_ipv4:

                            dst_config.append(cfglvl2 + "end")

            dst_config.append(cfglvl1 + "next")

        ### need to add support for sub interfaces and switch interfaces

    dst_config.append("end")

    # Generate zones

    logger.warning(__name__ + ": generate zones - not yet supported")

    """
    Generate zones
    """

    # Generate static routes

    logger.info(__name__ + ": generate static routes")

    dst_config.append("config router static")

    logger.info(
        __name__ + ": routes: found " + str(len(parsed_data["routes"])) + " routes"
    )

    for route_id, attributes in enumerate(parsed_data["routes"]):

        logger.info(__name__ + ": routes: generating route " + str(route_id))

        dst_config.append(cfglvl1 + "edit " + str(route_id))
        dst_config.append(
            cfglvl2 + "set dst " + attributes["network"] + " " + attributes["mask"]
        )
        dst_config.append(cfglvl2 + "set device " + attributes["interface"])
        dst_config.append(cfglvl2 + "set gateway " + attributes["gateway"])
        dst_config.append(cfglvl2 + "set distance " + attributes["distance"])
        dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate network objects

    logger.info(__name__ + ": generate network objects")

    dst_config.append("config firewall address")

    logger.info(
        __name__
        + ": network_objects: found "
        + str(len(parsed_data["network_objects"]))
        + " network objects"
    )

    for address, attributes in parsed_data["network_objects"].items():

        logger.info(
            __name__ + ": network_objects: generating network object " + address
        )

        dst_config.append(cfglvl1 + 'edit "' + address + '"')

        if attributes["type"] == "host":
            dst_config.append(cfglvl2 + "set type ipmask")
            dst_config.append(
                cfglvl2 + "set subnet " + attributes["host"] + " 255.255.255.255"
            )

            if attributes["interface"]:
                dst_config.append(
                    cfglvl2 + "set associated-interface " + attributes["interface"]
                )

        elif attributes["type"] == "network":
            dst_config.append(cfglvl2 + "set type ipmask")
            dst_config.append(
                cfglvl2
                + "set subnet "
                + attributes["network"]
                + " "
                + attributes["mask"]
            )

            if attributes["interface"]:
                dst_config.append(
                    cfglvl2 + "set associated-interface " + attributes["interface"]
                )

        elif attributes["type"] == "range":
            dst_config.append(cfglvl2 + "set type iprange")
            dst_config.append(cfglvl2 + "set start-ip " + attributes["address_first"])
            dst_config.append(cfglvl2 + "set end-ip " + attributes["address_last"])

            if attributes["interface"]:
                dst_config.append(
                    cfglvl2 + "set associated-interface " + attributes["interface"]
                )

        dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate network groups

    logger.info(__name__ + ": generate network groups")

    dst_config.append("config firewall addrgrp")

    logger.info(
        __name__
        + ": network_groups: found "
        + str(len(parsed_data["network_groups"]))
        + " network groups"
    )

    for group, attributes in parsed_data["network_groups"].items():

        logger.info(__name__ + ": network_groups: generating network group " + group)

        grp_members = ""

        if attributes["type"] == "group":

            dst_config.append('  edit "' + group + '"')

            for member in attributes["members"]:
                grp_members = grp_members + ' "' + member + '"'

            if grp_members:
                dst_config.append(cfglvl2 + "set member" + grp_members)

            dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate service objects

    logger.info(__name__ + ": generate service objects")

    dst_config.append("config firewall service custom")

    logger.info(
        __name__
        + ": service_objects: found "
        + str(len(parsed_data["service_objects"]))
        + " service objects"
    )

    for service, attributes in parsed_data["service_objects"].items():

        logger.info(
            __name__ + ": service_objects: generating service object " + service
        )

        dst_config.append('  edit "' + service + '"')

        if attributes["type"] == "service":

            if attributes["protocol"] in ["1", "icmp", "Icmp", "ICMP"]:

                dst_config.append(cfglvl2 + "set protocol ICMP")

                if attributes["icmp_type"]:
                    dst_config.append(
                        cfglvl2 + "set icmptype " + attributes["icmp_type"]
                    )

                if attributes["icmp_code"]:
                    dst_config.append(
                        cfglvl2 + "set icmpcode " + attributes["icmp_code"]
                    )

            elif attributes["protocol"] in ["6", "tcp", "Tcp", "TCP"]:

                dst_config.append(cfglvl2 + "set protocol TCP/UDP/SCTP")

                if attributes["dst_port"]:
                    dst_config.append(
                        cfglvl2 + "set tcp-portrange " + attributes["dst_port"]
                    )

            elif attributes["protocol"] in ["17", "udp", "Udp", "UDP"]:

                dst_config.append(cfglvl2 + "set protocol TCP/UDP/SCTP")

                if attributes["dst_port"]:
                    dst_config.append(
                        cfglvl2 + "set udp-portrange " + attributes["dst_port"]
                    )

            else:

                dst_config.append(cfglvl2 + "set protocol IP")
                dst_config.append(
                    cfglvl2 + "set protocol-number " + attributes["protocol"]
                )

        if attributes["type"] == "range":

            if attributes["protocol"] in ["6", "tcp", "Tcp", "TCP"]:

                dst_config.append(cfglvl2 + "set protocol TCP/UDP/SCTP")
                dst_config.append(
                    cfglvl2
                    + "set tcp-portrange "
                    + attributes["dst_port_first"]
                    + "-"
                    + attributes["dst_port_last"]
                )

            elif attributes["protocol"] in ["17", "udp", "Udp", "UDP"]:

                dst_config.append(cfglvl2 + "set protocol TCP/UDP/SCTP")
                dst_config.append(
                    cfglvl2
                    + "set udp-portrange "
                    + attributes["dst_port_first"]
                    + "-"
                    + attributes["dst_port_last"]
                )

        dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate service groups

    logger.info(__name__ + ": generate service groups")

    dst_config.append("config firewall service group")

    logger.info(
        __name__
        + ": service_groups: found "
        + str(len(parsed_data["service_groups"]))
        + " service groups"
    )

    for group, attributes in parsed_data["service_groups"].items():

        logger.info(__name__ + ": service_groups: generating service group " + group)

        grp_members = ""

        if attributes["type"] == "group":

            dst_config.append('  edit "' + group + '"')

            for member in attributes["members"]:
                grp_members = grp_members + ' "' + member + '"'

            if grp_members:
                dst_config.append(cfglvl2 + "set member" + grp_members)

            dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate policies

    logger.warning(__name__ + ": generate policies - not yet supported")

    dst_config.append("config firewall policy")

    logger.info(
        __name__
        + ": policies: found "
        + str(len(parsed_data["policies"]))
        + " policies"
    )

    for policy_id, attributes in enumerate(parsed_data["policies"]):

        logger.info(__name__ + ": policies: generating policy " + policy_id)

        dst_config.append(cfglvl1 + "edit " + str(policy_id))

        dst_config.append(
            cfglvl2
            + "set srcintf "
            + " ".join(list(map(str, attributes["src_interfaces"])))
        )

        dst_config.append(
            cfglvl2
            + "set dstintf "
            + " ".join(list(map(str, attributes["dst_interfaces"])))
        )

        # dst_config.append(
        #     cfglvl2
        #     + "set srcaddr "
        #     + " ".join(list(map(str, attributes["src_addresses"])))
        # )

        # dst_config.append(
        #     cfglvl2
        #     + "set dstaddr "
        #     + " ".join(list(map(str, attributes["dst_addresses"])))
        # )

        if attributes["description"]:
            dst_config.append(cfglvl2 + "set description " + attributes["description"])

        dst_config.append(cfglvl1 + "next")

    dst_config.append("end")

    # Generate NAT

    logger.warning(__name__ + ": generate NAT - not yet supported")

    # Return generated config

    logger.info(__name__ + ": generator module finished")

    return dst_config
