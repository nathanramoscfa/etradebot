# ETradeBot

ETradeBot is an automated trading software written in Python for E-Trade accounts that allows users to execute trades 
based on custom trading strategies. ETradeBot is strategy-agnostic and will execute any strategy given to it. Schedule 
a [FREE Consultation](https://calendly.com/nrcapitalmanagement/etradebot) to learn more about how ETradeBot can fit into 
your trading strategy. 

<b><span style="color:red">Warning: ETradeBot is experimental software and is in early development. Test on small dollar 
accounts only. This project is not affiliated with E-Trade or any other financial institution. By using ETradeBot, you 
agree to the [disclaimer](https://etradebot.readthedocs.io/en/latest/disclaimer.html). The developer is not responsible for any 
losses incurred from the use of ETradeBot. Use at your own risk. </span></b>
<span></b>

## Features

-   Fetches real-time market data from E-Trade API
-   Accesses market data from the Bloomberg API or Yahoo Finance API
-   Executes trade types: buy, sell, sell short, and short cover
-   Submits price type: market orders to E-Trade API
-   Manages portfolio: tracks positions, balance, and performance
-   Trades: common stocks and ETFs

## Getting Started

Refer to the [ETradeBot documentation](https://etradebot.readthedocs.io/en/latest/index.html) for instructions on installing, configuring, and using the software. 

1. [Create](https://etradebot.readthedocs.io/en/latest/environment.html) your Python environment and install ETradeBot.
2. [Obtain](https://etradebot.readthedocs.io/en/latest/credentials.html) and securely store your E-Trade credentials.
3. [Insert](https://etradebot.readthedocs.io/en/latest/strategies.html) your strategy into the strategies directory as a .py file.
4. [Configure](https://etradebot.readthedocs.io/en/latest/batch.html) a batch file to run ETradeBot.
5. [Run](https://etradebot.readthedocs.io/en/latest/running.html) ETradeBot in either preview or live trading mode.
6. [Schedule](https://etradebot.readthedocs.io/en/latest/scheduling.html) ETradeBot to run automatically.

If you are using the Bloomberg API, you will need to [Install](https://etradebot.readthedocs.io/en/latest/data.html) the Bloomberg SDK and C++ Build Tools. 
Otherwise, ETradeBot will automatically use the Yahoo Finance API.

## Example

The following example shows ETradeBot being run in Anaconda Prompt:

![Execute Trades](https://github.com/nathanramoscfa/etradebot/blob/main/docs/source/_static/execute_trades.gif)

Also see this example of ETradeBot being run within a [jupyter notebook](https://github.com/nathanramoscfa/etradebot/blob/main/dev/test_etradebot.ipynb).

## Troubleshooting

Refer to the [troubleshooting](https://etradebot.readthedocs.io/en/latest/scheduling.html) section of the documentation if you encounter any issues.

## Roadmap

Future releases will include the following features:

-   More price types: limit, stop, and other order types
-   More security types: options, mutual funds, and other security types

## Important Links

-   [ETradeBot Documentation](https://etradebot.readthedocs.io/en/latest/)
-   [E-Trade Developer Website](https://developer.etrade.com/home)
-   [Keyring Documentation](https://keyring.readthedocs.io/en/latest/)
-   [Anaconda Distribution](https://www.anaconda.com/products/individual)
-   [Windows Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)

## Contributing

Contributions to ETradeBot are welcome! Please see the [contributing guidelines](https://github.com/nathanramoscfa/etradebot/blob/main/CONTRIBUTING.md) for more information.

## Disclaimer

You must fully read, understand, and agree to the full disclaimer [here](https://etradebot.readthedocs.io/en/latest/disclaimer.html) before using ETradeBot. Please note that while the developer has taken care to ensure the quality and functionality of ETradeBot, there is no guarantee that the software is free from errors or bugs. The developer does not assume responsibility or liability for any damages or losses incurred as a result of using ETradeBot. Users of ETradeBot should use the software at their own risk and verify the accuracy and correctness of its output before making any investment decisions. By using ETradeBot, users agree to release the developer from any and all liability related to their use of the software. Users should read and understand all documentation and instructions provided before using ETradeBot. If you do not agree with any part of this disclaimer, do not use ETradeBot.

## License

ETradeBot is licensed under the [MIT License](https://github.com/nathanramoscfa/etradebot/blob/main/LICENSE).
