
# ETradeBot

ETradeBot is an automated trading software for E-Trade accounts that allows users to execute trades based on custom trading strategies. This project is not affiliated with E-Trade or any other financial institution.

## Features

-   Fetches real-time market data from E-Trade API
-   Executes trades (buy/sell) based on user-defined strategies
-   Manages portfolio: tracks positions, balance, and performance

## Documentation

Please refer to the [ETradeBot documentation](https://nr-capital-management.gitbook.io/etradebot/) for instructions on installing, configuring, and using the software.

## Installation

1.  Clone this repository:
    
    `git clone https://github.com/nathanramoscfa/etradebot.git` 
    
2.  Install the required packages:
    
    `pip install -r requirements.txt`

## Getting Started

1.  Obtain your E-Trade API credentials and store them securely using the `keyring` library. Refer to the documentation for instructions on obtaining and storing your credentials.
    
2.  Create a new Python file for your trading strategy in the `strategies` directory. Refer to the documentation for instructions on creating a custom trading strategy.
    
3.  In `main.py`, set the `strategy_name` variable to the name of your trading strategy file (without the .py extension).
    
4.  Run `main.py` to execute trades based on your trading strategy. Refer to the documentation for instructions on running the software in preview or production mode.

## Contributing

Contributions to ETradeBot are welcome! Please see the [contributing guidelines](https://chat.openai.com/CONTRIBUTING.md) for more information.

## Disclaimer

Please note that while the developer has taken care to ensure the quality and functionality of ETradeBot, there is no guarantee that the software is free from errors or bugs. The developer does not assume responsibility or liability for any damages or losses incurred as a result of using ETradeBot. Users of ETradeBot should use the software at their own risk and verify the accuracy and correctness of its output before making any investment decisions.

## License

ETradeBot is licensed under the [MIT License](https://chat.openai.com/LICENSE).