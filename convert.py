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
arg_parser.add_argument("input_file", help="/full/path/to/config")
arg_parser.add_argument("output_mode", help="output mode - [config|data]")
arg_parser.add_argument("src_format", help="source format - [watchguard]")
arg_parser.add_argument("dst_format", help="destination format - [fortigate]")
args = arg_parser.parse_args()

# Initiate logging

logger = logger(args.src_format, args.dst_format)

logger.log(2, "OpenFireVert.main: converter starting")
logger.log(2, "OpenFireVert.main: source format is " + args.src_format)
logger.log(2, "OpenFireVert.main: destination format is " + args.dst_format)
logger.log(2, "OpenFireVert.main: output mode is " + args.output_mode)

# Static variables

supported_src_formats = ["watchguard", "ciscoasa_pre83"]
supported_dst_formats = ["fortigate"]


def parse(src_format, src_config):

    logger.log(2, "OpenFireVert.parse: loading parser module for " + src_format)

    if src_format == "watchguard":
        from OpenFireVert.parsers.watchguard import parse

    elif src_format == "ciscoasa_pre83":
        from OpenFireVert.parsers.ciscoasa_pre83 import parse

    logger.log(2, "OpenFireVert.parse: loaded parser module for " + src_format)

    logger.log(2, "OpenFireVert.parse: starting parse of source configuration")

    parsed_data = parse(logger, src_config)

    logger.log(2, "OpenFireVert.parse: completed parse of source configuration")

    return parsed_data


def generate(dst_format, parsed_data):

    if dst_format == "fortigate":

        logger.log(
            2, "OpenFireVert.generate: loading generator module for " + dst_format
        )

        from OpenFireVert.generators.fortigate import generate

        logger.log(
            2, "OpenFireVert.generate: loaded generator module for " + dst_format
        )

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

    logger.log(
        2, "OpenFireVert.main: loading source configuration file " + args.input_file
    )

    if src_format in supported_src_formats:

        try:

            with open(args.input_file) as input_file:
                src_config = input_file.read()

        except:

            logger.log(
                4,
                "OpenFireVert.main: source file either not found or not readable "
                + args.input_file,
            )

            print(
                f"{Fore.RED}Error: source file either not found or not readable.{Style.RESET_ALL}"
            )

            exit()

    else:

        logger.log(
            4,
            "OpenFireVert.main: source firewall type not supported " + args.src_format,
        )

        print(f"{Fore.RED}Error: source firewall type not supported.{Style.RESET_ALL}")

        exit()

    # Run configuration parser

    logger.log(2, "OpenFireVert.main: running configuration parser")

    parsed_data = parse(src_format=src_format, src_config=src_config)

    logger.log(2, "OpenFireVert.main: configuration parser finished")

    # Output

    if args.output_mode == "data":  # pretty print parsed data

        logger.log(2, "OpenFireVert.main: output parsed data as dictionary dump")

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(parsed_data)

    else:  # generate destination configuration

        if dst_format in supported_dst_formats:

            logger.log(2, "OpenFireVert.main: running configuration generator")

            dst_config = generate(dst_format=dst_format, parsed_data=parsed_data)

            for line in dst_config:
                print(line)

            logger.log(2, "OpenFireVert.main: configuration generator finished")

        else:

            logger.log(
                4,
                "OpenFireVert.main: destination firewall type not currently supported "
                + args.src_format,
            )

            print(
                f"{Fore.RED}Error: destination firewall type not currently supported.{Style.RESET_ALL}"
            )

            exit()

    logger.log(2, "OpenFireVert.main: converter exiting")


if __name__ == "__main__":

    main(src_format=args.src_format, dst_format=args.dst_format)
