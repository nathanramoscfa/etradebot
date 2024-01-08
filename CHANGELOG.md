# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- No pending changes. 

## [3.0.3] - 2024-01-08
### Added
- Traceback functionality to `is_market_open()` function for better error diagnosis.

### Changed
- Updated `pandas-market_calendars` from version 4.1.4 to 4.3.3 for enhanced features and bug fixes.

### Fixed
- Resolved an error related to 'Timestamp' object handling in `is_market_open()`.

### Security
- Addressed security vulnerability in `setuptools` by downgrading to a safer version (67.6.0).

## [Initial Release] - 2023-03-31
