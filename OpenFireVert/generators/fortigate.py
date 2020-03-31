#!/usr/bin/env python

# Import common and settings

import OpenFireVert.common as common
import OpenFireVert.settings as settings


def generate(logger, parsed_data):

    logger.log(2, __name__ + ": generator module started")

    # Initialise variables

    dst_config = []

    # Generate system

    logger.log(2, __name__ + ": generate system")

    dst_config.append("config system global")
    dst_config.append("  set hostname " + parsed_data["system"]["hostname"])
    dst_config.append("end")

    dst_config.append("config system dns")
    dst_config.append("  set domain " + parsed_data["system"]["domain"])
    dst_config.append("end")

    # Generate routes

    logger.log(2, __name__ + ": generate routes")

    dst_config.append("config router static")

    for route_id, attributes in parsed_data["routes"].items():

        dst_config.append("  edit " + str(route_id))
        dst_config.append(
            "    set dst " + attributes["network"] + " " + attributes["mask"]
        )
        dst_config.append("    set gateway " + attributes["gateway"])
        dst_config.append("    set distance " + attributes["distance"])
        dst_config.append("  next")

    dst_config.append("end")

    # Generate address objects

    logger.log(2, __name__ + ": generate address objects")

    dst_config.append("config firewall address")

    for address, attributes in parsed_data["network_objects"].items():

        dst_config.append('  edit "' + address + '"')

        if attributes["type"] == "host":

            dst_config.append("    set type ipmask")
            dst_config.append(
                "    set subnet " + attributes["host"] + " 255.255.255.255"
            )

        elif attributes["type"] == "network":

            dst_config.append("    set type ipmask")
            dst_config.append(
                "    set subnet " + attributes["network"] + " " + attributes["mask"]
            )

        elif attributes["type"] == "range":

            dst_config.append("    set type iprange")
            dst_config.append("    set start-ip " + attributes["address_first"])
            dst_config.append("    set end-ip " + attributes["address_last"])

        dst_config.append("  next")

    dst_config.append("end")

    # Generate address groups

    logger.log(2, __name__ + ": generate address groups")

    dst_config.append("config firewall addrgrp")

    for group, attributes in parsed_data["network_groups"].items():

        grp_members = ""

        if attributes["type"] == "group":

            dst_config.append('  edit "' + group + '"')

            for member in attributes["members"]:
                grp_members = grp_members + ' "' + member + '"'

            if grp_members:
                dst_config.append("    set member" + grp_members)

            dst_config.append("  next")

    dst_config.append("end")

    # Generate service objects

    logger.log(2, __name__ + ": generate service objects")

    dst_config.append("config firewall service custom")

    for service, attributes in parsed_data["service_objects"].items():

        dst_config.append('  edit "' + service + '"')

        if attributes["type"] == "service":

            if attributes["protocol"] == "1":

                dst_config.append("    set protocol ICMP")
                dst_config.append("    set icmptype " + attributes["icmp-type"])
                dst_config.append("    set icmpcode " + attributes["icmp-code"])

            elif attributes["protocol"] == "6":

                dst_config.append("    set protocol TCP/UDP/SCTP")
                dst_config.append("    set tcp-portrange " + attributes["port"])

            elif attributes["protocol"] == "17":

                dst_config.append("    set protocol TCP/UDP/SCTP")
                dst_config.append("    set udp-portrange " + attributes["port"])

            else:

                dst_config.append("    set protocol IP")
                dst_config.append("    set protocol-number " + attributes["protocol"])

        if attributes["type"] == "range":

            if attributes["protocol"] == "6":

                dst_config.append("    set protocol TCP/UDP/SCTP")
                dst_config.append(
                    "    set tcp-portrange "
                    + attributes["port_first"]
                    + "-"
                    + attributes["port_last"]
                )

            elif attributes["protocol"] == "17":

                dst_config.append("    set protocol TCP/UDP/SCTP")
                dst_config.append(
                    "    set udp-portrange "
                    + attributes["port_first"]
                    + "-"
                    + attributes["port_last"]
                )

        dst_config.append("  next")

    dst_config.append("end")

    # Generate service groups

    logger.log(2, __name__ + ": generate service groups")

    dst_config.append("config firewall service group")

    for group, attributes in parsed_data["service_groups"].items():

        grp_members = ""

        if attributes["type"] == "group":

            dst_config.append('  edit "' + group + '"')

            for member in attributes["members"]:
                grp_members = grp_members + ' "' + member + '"'

            if grp_members:
                dst_config.append("    set member" + grp_members)

            dst_config.append("  next")

    dst_config.append("end")

    # Generate policies

    logger.log(2, __name__ + ": generate policies - not yet supported")

    dst_config.append("config firewall policy")

    dst_config.append("end")

    # Generate NAT

    logger.log(2, __name__ + ": generate NAT - not yet supported")

    # Return generated config

    logger.log(2, __name__ + ": generator module finished")

    return dst_config
