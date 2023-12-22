class HardToBorrowException(Exception):
    def __init__(self, ticker):
        self.ticker = ticker
        super().__init__(f'Ticker {ticker} is hard to borrow.')
