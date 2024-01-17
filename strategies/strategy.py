import inspect
import warnings
import importlib


class Strategy:
    """
    :description: This class is the main strategy class that will be used to run the strategy.

    :param prints: Print the strategy
    :type prints: bool
    :param strategy_name: The name of the strategy module to use
    :type strategy_name: str
    """
    def __init__(self, prints=False, strategy_name='example_strategy'):
        """
        :description: This class is the main strategy class that will be used to run the strategy.

        :return: None
        :rtype: None

        """
        self.prints = prints
        self.strategy_name = strategy_name

    def run_strategy(self):
        """
        :description: This function runs the strategy.

        :return: The strategy function
        :rtype: function
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            # Import the strategy function from the specified module
            strategy_module = importlib.import_module("strategies." + self.strategy_name)
            strategy_function = strategy_module.strategy

            num_parameters = len(inspect.signature(strategy_function).parameters)

            if num_parameters == 1:
                return strategy_function(self.prints)
            else:
                return strategy_function()
