#!/usr/bin/env python

# Import modules

import ipaddress
import re
import unidecode


def cleanse_names(name):

    name = name.replace("+ ", "plus_")
    name = name.replace(" -", "_")
    name = name.replace("  ", "_")
    name = name.replace(" ", "_")
    name = name.replace("/", "_")
    name = name.replace(".", "_")
    name = unidecode.unidecode(name)
    valid_chars = re.compile(r"[^A-Za-z0-9!@#$%^&()-_{}]")
    name = valid_chars.sub("", name)

    return name


def common_regex():

    common_regex.country_code = "(?:[A-Z]{2})"
    common_regex.fqdn = "(.*?)"
    # common_regex.ipv4 = "(?:[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})"
    common_regex.ipv4_address = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    common_regex.ipv4_prefix = "(?:\/(?:[0-9]|[1-2][0-9]|3[0-2]))"
    common_regex.ipv4_mask = "(?:(?:255\.){3}(?:255|254|252|248|240|224|192|128|0+))|(?:(?:255\.){2}(?:255|254|252|248|240|224|192|128|0+)\.0)|(?:(255\.)(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){2})|(?:(?:255|254|252|248|240|224|192|128|0+)(?:\.0+){3})"
    common_regex.ipv6_address = "(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    common_regex.ipv6_mask = "(?:\/(?:12[0-8]|1[0-1][0-9]|[1-9][0-9]|[0-9]))"
    common_regex.mac_address = "(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})"


def interface_lookup(ip_address, interfaces, routes):

    ip_address = ipaddress.ip_address(ip_address)

    interface_networks = {}
    matching_interfaces = {}
    selected_interface = ""

    route_networks = {}
    matching_routes = {}
    selected_route = ""

    # lookup interface subnets

    ## build dictionary of all interface networks

    for interface, attributes in interfaces.items():

        if attributes["ipv4_config"]:

            for ipv4_config in attributes["ipv4_config"]:

                interface_networks[interface] = ipaddress.IPv4Interface(
                    ipv4_config["ip_address"] + "/" + ipv4_config["mask"]
                )

    ## check if ip address matches any interface networks

    for interface, network in interface_networks.items():

        if ip_address in network.network:

            matching_interfaces[interface] = network

    ## if multiple matching interfaces find the most specific

    if len(matching_interfaces) == 1:

        selected_interface = list(matching_interfaces)[0]

    elif len(matching_interfaces) > 1:

        for interface, network in matching_interfaces.items():

            if selected_interface:

                if network.network.netmask > selected_interface_network.network.netmask:

                    selected_interface = interface
                    selected_interface_network = network
            else:

                selected_interface = interface
                selected_interface_network = network

    else:

        selected_interface = ""

    ## return if an interface selected

    if selected_interface:
        return selected_interface

    # lookup routes if no interface found

    ## build dictionary of all routes

    for id, route in enumerate(routes):

        route_networks[id] = ipaddress.IPv4Network(
            route["network"] + "/" + route["mask"]
        )

    ## check if ip address matches any routes

    for id, route in route_networks.items():

        if ip_address in route:

            matching_routes[id] = route

    ## if multiple matching routes find the most specific

    if len(matching_routes) == 1:

        selected_route = list(matching_routes)[0]

    elif len(matching_routes) > 1:

        for id, route in matching_routes.items():

            if selected_route:

                if route.netmask > selected_route_network.netmask:

                    selected_route = id
                    selected_route_network = route
            else:

                selected_route = id
                selected_route_network = route

    else:

        selected_route = ""

    if selected_route:
        selected_interface = routes[selected_route]["interface"]

    ## return if an interface selected

    if selected_interface:
        return selected_interface

    else:
        return ""

    ### need to add lookup against supplemental routing info csv


def ipv4_prefix_to_mask(prefix):

    if "/32" in prefix:
        mask = "255.255.255.255"

    elif "/31" in prefix:
        mask = "255.255.255.254"

    elif "/30" in prefix:
        mask = "255.255.255.252"

    elif "/29" in prefix:
        mask = "255.255.255.248"

    elif "/28" in prefix:
        mask = "255.255.255.240"

    elif "/27" in prefix:
        mask = "255.255.255.224"

    elif "/26" in prefix:
        mask = "255.255.255.192"

    elif "/25" in prefix:
        mask = "255.255.255.128"

    elif "/24" in prefix:
        mask = "255.255.255.0"

    elif "/23" in prefix:
        mask = "255.255.254.0"

    elif "/22" in prefix:
        mask = "255.255.252.0"

    elif "/21" in prefix:
        mask = "255.255.248.0"

    elif "/20" in prefix:
        mask = "255.255.240.0"

    elif "/19" in prefix:
        mask = "255.255.224.0"

    elif "/18" in prefix:
        mask = "255.255.192.0"

    elif "/17" in prefix:
        mask = "255.255.128.0"

    elif "/16" in prefix:
        mask = "255.255.0.0"

    elif "/15" in prefix:
        mask = "255.254.0.0"

    elif "/14" in prefix:
        mask = "255.252.0.0"

    elif "/13" in prefix:
        mask = "255.248.0.0"

    elif "/12" in prefix:
        mask = "255.240.0.0"

    elif "/11" in prefix:
        mask = "255.224.0.0"

    elif "/10" in prefix:
        mask = "255.192.0.0"

    elif "/9" in prefix:
        mask = "255.128.0.0"

    elif "/8" in prefix:
        mask = "255.0.0.0"

    elif "/7" in prefix:
        mask = "254.0.0.0"

    elif "/6" in prefix:
        mask = "252.0.0.0"

    elif "/5" in prefix:
        mask = "248.0.0.0"

    elif "/4" in prefix:
        mask = "240.0.0.0"

    elif "/3" in prefix:
        mask = "224.0.0.0"

    elif "/2" in prefix:
        mask = "192.0.0.0"

    elif "/1" in prefix:
        mask = "128.0.0.0"

    elif "/0" in prefix:
        mask = "0.0.0.0"

    else:
        mask = ""

    return mask
