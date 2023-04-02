---
description: Configuring your trading strategy
---

# Strategies

The `strategies` directory is where the user should place their own strategy file, written in Python. Here are the steps to create and use your own strategy:

1. Create your strategy file:
   * In the `strategies` directory, create a new Python file for your strategy.
   * Write your strategy in the form of a function which returns a pd.Series where the index is the ticker symbols and the values are the percent decimal portfolio weightings of each ticker.
   *   Your strategy must return a pd.Series like below:

       ```ruby
       def my_strategy():
           # Your trading strategy logic goes here. 
           return pd.Series({
               'AAPL': 0.5,
               'GOOG': 0.3,
               'AMZN': 0.2
           })
       ```
   * An example strategy is provided [here](../strategies/example\_strategy.py) purely for demonstration purposes only. The example strategy included in the `strategies` directory is not intended to be used as a trading strategy.&#x20;
2. Set the strategy name in `main.py`:
   * In the `main.py` file, set the `strategy_name` variable to the name of your strategy file (without the .py extension).
   *   Example code:

       ```python
       strategy_name = 'my_strategy'
       ```
   * By default, `strategy_name` is set to `example_strategy` which is only intended as a demonstration.&#x20;

That's it! You should now have your strategy ready to use with ETradeBot.
