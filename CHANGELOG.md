# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Option trading functionality.
- Limit and stop order functionality.
- Support for trading option spreads.
- Support for macOS compatibility.

## [3.0.5] - 2024-01-17

### Fixed
- Updated `README.md` to fix typo in keyring parameters example from "cookie" to "etrade_cookie".
- Edited `bot.py` to fix console output print statements' formatting.
- Fixed issues with the `pyetrade` forked repository's `setup.py` file.

## Updated
- Updated `authentication.py` Exception handling to remove unnecessary print statements.

## [3.0.4] - 2024-01-15
### Updated
- Updated driver management to `webdriver_manager` library to handle webdriver management.

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
