---
description: Tools for automated trading on E*Trade
---

# Introduction

ETradeBot is a Python-based project that automates trading on the E-Trade platform. The bot can fetch market data, execute trades, and manage your portfolio. This project aims to help traders execute rules-based trading strategies and minimize manual intervention in the trading process.

## Features

* Fetches real-time market data from E-Trade API
* Executes trades (buy/sell) based on user-defined strategies
* Manages portfolio: tracks positions, balance, and performance

## Getting Started

1. [Configure ](broken-reference)your Python environment and install ETradeBot.
2. [Obtain](configuration/credentials.md) and securely store your E-Trade credentials.
3. [Insert](configuration/strategies.md) your strategy into the `strategies` directory as a `.py` file.&#x20;
4. [Run ](usage/running.md)`main.py` from the root directory.&#x20;

## Purpose

ETradeBot provides tools for automated trading on the E-Trade platform. ETradeBot is strategy-agnostic. This means that you must come up with your own strategy for ETradeBot to execute. ETradeBot is nothing more than a tool to automate trading.&#x20;
