# OpenFireVert (Open Firewall Converter)

OpenFireVert is a firewall configuration conversion tool written in Python.
Support for any firewall type will be added based on request, demand and resource availability.

This tool generates configuration for supported elements only, that must be input through CLI or "merged" with a full or running configuration, not full configuration files. See the documentation for supported elements for each vendor.

## Usage

python3 openfirevert.py <source_config> <source_type> <destination_type>

## Requirements

 * Python 3.6+

#### Python Module Dependencies

 * netaddr

## Changelog

#### Version 0.1 (Initial Release)

 * Support for conversion from WatchGuard to FortiGate
