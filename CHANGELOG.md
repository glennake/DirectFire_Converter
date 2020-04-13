# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2020-03-29

### Added

- Initial conversion engine with modular design
- Initial support for parsing WatchGuard
- Initial support for generating Fortinet FortiGate

## [0.2.0] - 2020-03-31

### Added

- Module template for parsers
- Module template for generators
- Initial support for parsing Cisco ASA pre-8.3

## [0.3.0] - 2020-04-01

### Added

- Initial support for generating Cisco ASA post-8.3

## [0.3.1] - 2020-04-06

### Changed

- Standardised comments and logging to use common terminology

## [0.3.2] - 2020-04-06

### Added

- Requirements file to install Python modules using Pip

### Changed

- Argument parser and logging to use named arguments
- Documentation to provide new installation and usage details

## [0.4.0] - 2020-04-06

### Added

- Initial support for parsing Fortinet FortiGate

## [0.5.0] - 2020-04-07

### Added

- Initial support for parsing Juniper SRX (JunOS)
- Missing logging for interfaces and zones across parsers
- Improved logging for unsupported features when parsing

### Changed

- Bug fixes in Fortinet FortiGate parser

## [0.5.1] - 2020-04-09

### Added

- Support for parsing Juniper SRX (JunOS) interfaces
- Enhancements for parsing Juniper SRX (JunOS) routes

### Changed

- Bug fixes in parsers - Cisco ASA (pre and post 8.3), Fortinet FortiGate, WatchGuard

## [0.5.2] - 2020-04-12

### Added

- Support for parsing WatchGuard interfaces
- Enhancements for parsing WatchGuard routes

### Changed

- Moved data output method to a generator module
- Changed data output method to JSON formatting

## [0.5.3] - 2020-04-13

### Added

- Support for parsing Fortinet FortiGate interfaces

### Changed

- Standardisation of Fortinet FortiGate parser indentation levels
- Move firewall policy data structure to nested lists for addresses, interfaces and services
