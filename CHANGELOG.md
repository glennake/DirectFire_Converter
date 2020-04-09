# Changelog

All notable changes to this project will be documented in this file.

## [0.0.1] - 2020-03-29

### Added

- Initial conversion engine with modular design
- Initial support for parsing WatchGuard
- Initial support for generating Fortinet FortiGate

## [0.0.2] - 2020-03-31

### Added

- Module template for parsers
- Module template for generators
- Initial support for parsing Cisco ASA pre-8.3

## [0.0.3] - 2020-04-01

### Added

- Initial support for generating Cisco ASA post-8.3

## [0.0.4] - 2020-04-06

### Changed

- Standardised comments and logging to use common terminology

## [0.0.5] - 2020-04-06

### Added

- Requirements file to install Python modules using Pip

### Changed

- Argument parser and logging to use named arguments
- Documentation to provide new installation and usage details

## [0.0.6] - 2020-04-06

### Added

- Initial support for parsing Fortinet FortiGate

## [0.0.7] - 2020-04-07

### Added

- Initial support for parsing Juniper SRX (JunOS)
- Missing logging for interfaces and zones across parsers
- Improved logging for unsupported features when parsing

### Changed

- Bug fixes in Fortinet FortiGate parser

## [0.0.8] - 2020-04-09

### Added

- Support for parsing Juniper SRX (JunOS) interfaces
- Enhancements for parsing Juniper SRX (JunOS) routes

### Changed

- Bug fixes in parsers - Cisco ASA (pre and post 8.3), Fortinet FortiGate, WatchGuard
