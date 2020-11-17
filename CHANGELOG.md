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

## [0.6.0] - 2020-04-14

### Added

- Resolve interfaces of objects by static routing information

### Changed

- Rewrite parser module for Cisco ASA pre 8.3

## [0.6.1] - 2020-04-18

### Added

- Support for parsing Cisco ASA pre 8.3 service objects

### Changed

- Bug fixes in Cisco ASA pre 8.3 parser
- Bug fixes in interface lookup function

## [0.6.2] - 2020-04-18

### Changed

- Migrate all parser and generator modules to new data structure
- Bug fixes and stardisation across parser and generator modules

## [0.7.0] - 2020-04-23

### Added

- Initial support for parsing Cisco ASA post 8.3

### Changed

- Bug fixes in Cisco ASA pre 8.3 parser module
- Bug fixes in Fortinet FortiGate generator module

## [0.7.1] - 2020-11-16

### Added

- Improved logging in Watchguard parser module

## [0.7.2] - 2020-11-17

### Added

- Added traceback-with-variables to requirements

### Changed

- Overhaul logging across all modules and improve exception logging
- Improved logging in Watchguard parser module
- Improved logging in FortiGate generator module

## [0.7.3] - 2020-11-17

### Added

- Added more default interface exclusions in Watchguard parser module
- Source appliance context logging in Watchguard parser module

### Changed

- Fixed enhanced exception logging across several modules
- Improved logging in Watchguard parser module
