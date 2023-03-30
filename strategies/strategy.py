import warnings
import importlib


class Strategy:
    def __init__(self, prints=False, strategy_name='example_strategy'):
        """
        This class is the main strategy class that will be used to run the strategy.

        :param prints: Print the strategy
        :type prints: bool
        :param strategy_name: The name of the strategy module to use
        :type strategy_name: str
        """
        self.prints = prints
        self.strategy_name = strategy_name

    def run_strategy(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            # Import the strategy function from the specified module
            strategy_module = importlib.import_module("strategies." + self.strategy_name)
            strategy_function = strategy_module.strategy

            return strategy_function(self.prints)
