#!/usr/bin/env python

# Title: OpenFireVert (Open Firewall Converter)
# Description: OpenFireVert is an open source firewall configuration conversion tool written in Python
# Author: Glenn Akester (@glennake)
# Version: 0.0.1
#
# OpenFireVert is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenFireVert is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# If you don't have a copy of the GNU General Public License,
# it is available here <http://www.gnu.org/licenses/>.


# Imports

try:
    import argparse
except:
    raise ImportError("Could not import module: argparse")

try:
    from colorama import Fore, Back, Style
except:
    raise ImportError("Could not import module: colorama")

try:
    import pprint
except:
    raise ImportError("Could not import module: pprint")


# Import common and settings

import OpenFireVert.common as common
from OpenFireVert.logging import logger
import OpenFireVert.settings as settings

# Get arguments

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-c", "--config", help="/full/path/to/config", required=True)

arg_parser.add_argument(
    "-o", "--output", choices=["config", "data"], help="output mode", required=True,
)

arg_parser.add_argument(
    "-s",
    "--source",
    choices=["ciscoasa_pre83", "fortigate", "watchguard"],
    help="source format",
    required=True,
)

arg_parser.add_argument(
    "-d", "--destination", choices=["ciscoasa", "fortigate"], help="destination format",
)

args = arg_parser.parse_args()

# Initiate logging

if args.output == "data":
    logger = logger(args.source, "data")
else:
    logger = logger(args.source, args.destination)

logger.log(2, "OpenFireVert.main: converter starting")
logger.log(2, "OpenFireVert.main: output mode is " + args.output)
logger.log(2, "OpenFireVert.main: source format is " + args.source)

# Check arguments

if args.output == "config":

    if args.destination is None:

        logger.log(
            3,
            "OpenFireVert.main: destination format is required when output mode is config",
        )

        print(
            f"{Fore.RED}Error: destination format is required when output mode is config.{Style.RESET_ALL}"
        )

        exit()

elif args.output == "data":

    if args.destination:

        logger.log(
            2,
            "OpenFireVert.main: destination format provided but not required when output mode is data",
        )


def parse(src_format, src_config):

    logger.log(2, "OpenFireVert.parse: loading parser module for " + src_format)

    if src_format == "ciscoasa_pre83":
        from OpenFireVert.parsers.ciscoasa_pre83 import parse

    elif src_format == "fortigate":
        from OpenFireVert.parsers.fortigate import parse

    elif src_format == "watchguard":
        from OpenFireVert.parsers.watchguard import parse

    logger.log(2, "OpenFireVert.parse: loaded parser module for " + src_format)

    logger.log(2, "OpenFireVert.parse: starting parse of source configuration")

    parsed_data = parse(logger, src_config)

    logger.log(2, "OpenFireVert.parse: completed parse of source configuration")

    return parsed_data


def generate(dst_format, parsed_data):

    logger.log(2, "OpenFireVert.generate: loading generator module for " + dst_format)

    if dst_format == "ciscoasa":
        from OpenFireVert.generators.ciscoasa import generate

    elif dst_format == "fortigate":
        from OpenFireVert.generators.fortigate import generate

    logger.log(2, "OpenFireVert.generate: loaded generator module for " + dst_format)

    logger.log(
        2, "OpenFireVert.generate: starting generation of destination configuration"
    )

    dst_config = generate(logger, parsed_data)

    logger.log(
        2, "OpenFireVert.generate: completed generation of destination configuration"
    )

    return dst_config


def main(src_format, dst_format):

    # Load source configuration file

    logger.log(2, "OpenFireVert.main: loading source configuration from " + args.config)

    try:

        with open(args.config) as config_file:
            src_config = config_file.read()

    except:

        logger.log(
            4,
            "OpenFireVert.main: source file either not found or not readable "
            + args.config,
        )

        print(
            f"{Fore.RED}Error: source file either not found or not readable.{Style.RESET_ALL}"
        )

        exit()

    # Run configuration parser

    logger.log(2, "OpenFireVert.main: running configuration parser")

    parsed_data = parse(src_format=src_format, src_config=src_config)

    logger.log(2, "OpenFireVert.main: configuration parser finished")

    # Output

    if args.output == "data":  # pretty print parsed data

        logger.log(2, "OpenFireVert.main: output parsed data as dictionary dump")

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(parsed_data)

    else:  # generate destination configuration

        logger.log(2, "OpenFireVert.main: running configuration generator")

        dst_config = generate(dst_format=dst_format, parsed_data=parsed_data)

        for line in dst_config:
            print(line)

        logger.log(2, "OpenFireVert.main: configuration generator finished")

    logger.log(2, "OpenFireVert.main: converter exiting")


if __name__ == "__main__":

    main(src_format=args.source, dst_format=args.destination)
