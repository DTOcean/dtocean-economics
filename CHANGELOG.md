# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added main function which takes three dataframes, one for CAPEX, OPEX, and
  energy and the discount rate and returns a dictionary of results
- Added a preprocessing module which provides functions for preparing the
  required dataframes and for calculating estimates to the inputs

### Changed

- Reorganised the functions module to undertake all dataframe manipulation
  work. The main function just collects any valid results.

## [1.0.0] - 2017-01-05

### Added

- Initial import of dtocean-economics from SETIS.
