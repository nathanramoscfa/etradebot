import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

mock_accounts_response = {
    'AccountListResponse': {
        'Accounts': {
            'Account': [
                {
                    'accountId': '82314598',
                    'accountIdKey': 'dBZOKt9xDrtRSAOl4MSiiA',
                    'accountMode': 'IRA',
                    'accountDesc': 'Brokerage',
                    'accountName': 'NickName-1',
                    'accountType': 'MARGIN',
                    'institutionType': 'BROKERAGE',
                    'accountStatus': 'ACTIVE',
                    'closedDate': 0,
                    'shareWorksAccount': False},
                {
                    'accountId': '58315636',
                    'accountIdKey': 'vQMsebA1H5WltUfDkJP48g',
                    'accountMode': 'CASH',
                    'accountDesc': 'LLC C Corporation',
                    'accountName': '',
                    'accountType': 'LLC_C_CORPORATION',
                    'institutionType': 'BROKERAGE',
                    'accountStatus': 'ACTIVE',
                    'closedDate': 0,
                    'shareWorksAccount': False},
                {
                    'accountId': '70700418',
                    'accountIdKey': '6_Dpy0rmuQ9cu9IbTfvF2A',
                    'accountMode': 'CASH',
                    'accountDesc': 'INDIVIDUAL',
                    'accountName': 'NickName-3',
                    'accountType': 'INDIVIDUAL',
                    'institutionType': 'BROKERAGE',
                    'accountStatus': 'ACTIVE',
                    'closedDate': 0,
                    'shareWorksAccount': False},
                {
                    'accountId': '83515143',
                    'accountIdKey': 'xj1Dc18FTqWPqkEEVUr5rw',
                    'accountMode': 'CASH',
                    'accountDesc': 'INDIVIDUAL',
                    'accountName': '',
                    'accountType': 'CASH',
                    'institutionType': 'BROKERAGE',
                    'accountStatus': 'CLOSED',
                    'closedDate': 1521027780,
                    'shareWorksAccount': False
                }
            ]
        }
    }
}

mock_balance_response = {
    'BalanceResponse': {
        'accountId': '58315636',
        'accountType': 'MARGIN',
        'optionLevel': 'LEVEL_4',
        'accountDescription': 'JOHN DOE',
        'quoteMode': 1,
        'dayTraderStatus': 'NO_PDT',
        'accountMode': 'MARGIN',
        'Cash': {
            'fundsForOpenOrdersCash': 0, 'moneyMktBalance': 0
        },
        'Computed': {
            'cashAvailableForInvestment': 0,
            'cashAvailableForWithdrawal': 0,
            'totalAvailableForWithdrawal': 2155,
            'netCash': 2155,
            'cashBalance': 0,
            'settledCashForInvestment': 0,
            'unSettledCashForInvestment': 0,
            'fundsWithheldFromPurchasePower': 0,
            'fundsWithheldFromWithdrawal': 0,
            'marginBuyingPower': 4310,
            'cashBuyingPower': 2155,
            'dtMarginBuyingPower': 0,
            'dtCashBuyingPower': 0,
            'marginBalance': -2977.14,
            'shortAdjustBalance': 2913.88,
            'regtEquity': 10205.6084,
            'regtEquityPercent': 63.402149483676965,
            'accountBalance': -63.26,
            'OpenCalls': {
                'minEquityCall': 0,
                'fedCall': 0,
                'cashCall': 0,
                'houseCall': 0
            },
            'RealTimeValues': {
                'totalAccountValue': 10201.5284,
                'netMv': 10264.7884,
                'netMvLong': 13178.6684,
                'netMvShort': -2913.88
            }
        }
    }
}

mock_orders_list_response = {
    'OrdersResponse': {
        'Order': [
            {
                'orderId': 19,
                'details': 'https://api.etrade.com/v1/accounts/vQMsebA1H5WltUfDkJP48g/orders/19.json',
                'orderType': 'EQ',
                'OrderDetail': [
                    {
                        'placedTime': 1676490079653,
                        'executedTime': 1676490080854,
                        'orderValue': 324.2424,
                        'status': 'EXECUTED',
                        'orderTerm': 'GOOD_FOR_DAY',
                        'priceType': 'MARKET',
                        'limitPrice': 0,
                        'stopPrice': 0,
                        'marketSession': 'REGULAR',
                        'allOrNone': False,
                        'netPrice': 0,
                        'netBid': 0,
                        'netAsk': 0,
                        'gcd': 0,
                        'ratio': '',
                        'Instrument': [
                            {
                                'symbolDescription': 'VANECK OIL SERVICES ETF',
                                'orderAction': 'SELL_SHORT',
                                'quantityType': 'QUANTITY',
                                'orderedQuantity': 1,
                                'filledQuantity': 1.0,
                                'averageExecutionPrice': 324.26,
                                'estimatedCommission': 0.0001,
                                'estimatedFees': 0.0074,
                                'Product': {
                                    'symbol': 'OIH',
                                    'securityType': 'EQ'
                                }
                            }
                        ]
                    }
                ]
            },
            {
                'orderId': 18,
                'details': 'https://api.etrade.com/v1/accounts/vQMsebA1H5WltUfDkJP48g/orders/18.json',
                'orderType': 'EQ',
                'OrderDetail': [
                    {
                        'placedTime': 1676490078940,
                        'executedTime': 1676490079399,
                        'orderValue': 203.39,
                        'status': 'EXECUTED',
                        'orderTerm': 'GOOD_FOR_DAY',
                        'priceType': 'MARKET',
                        'limitPrice': 0,
                        'stopPrice': 0,
                        'marketSession': 'REGULAR',
                        'allOrNone': False,
                        'netPrice': 0,
                        'netBid': 0,
                        'netAsk': 0,
                        'gcd': 0,
                        'ratio': '',
                        'Instrument': [
                            {
                                'symbolDescription': 'VANGUARD ADMIRAL FDS INC S&P SMALLCAP 600 GROWTH INDEX ETF SHS',
                                'orderAction': 'BUY',
                                'quantityType': 'QUANTITY',
                                'orderedQuantity': 1,
                                'filledQuantity': 1.0,
                                'averageExecutionPrice': 203.285,
                                'estimatedCommission': 0.0,
                                'estimatedFees': 0.0,
                                'Product': {
                                    'symbol': 'VIOG',
                                    'securityType': 'EQ'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

mock_quote_response = {
    'QuoteResponse': {
        'QuoteData': [
            {
                'dateTime': '19:59:57 EST 02-17-2023',
                'dateTimeUTC': 1676681997,
                'quoteStatus': 'CLOSING',
                'ahFlag': 'true',
                'hasMiniOptions': False,
                'All': {
                    'adjustedFlag': False,
                    'ask': 152.64,
                    'askSize': 600,
                    'askTime': '19:59:57 EST 02-17-2023',
                    'bid': 152.56,
                    'bidExchange': '',
                    'bidSize': 100,
                    'bidTime': '19:59:57 EST 02-17-2023',
                    'changeClose': -1.16,
                    'changeClosePercentage': -0.75,
                    'companyName': 'APPLE INC COM',
                    'daysToExpiration': 0,
                    'dirLast': '1',
                    'dividend': 0.23,
                    'eps': 5.89,
                    'estEarnings': 5.972,
                    'exDividendDate': 1676085660,
                    'high': 153.0,
                    'high52': 179.61,
                    'lastTrade': 152.55,
                    'low': 150.85,
                    'low52': 124.17,
                    'open': 152.35,
                    'openInterest': 0,
                    'optionStyle': '',
                    'optionUnderlier': '',
                    'previousClose': 153.71,
                    'previousDayVolume': 65602013,
                    'primaryExchange': 'NSDQ',
                    'symbolDescription': 'APPLE INC COM',
                    'totalVolume': 59144118,
                    'upc': 0,
                    'cashDeliverable': 0,
                    'marketCap': 2413637862300.0,
                    'sharesOutstanding': 15821946000,
                    'nextEarningDate': '',
                    'beta': 1.32,
                    'yield': 0.5985,
                    'declaredDividend': 0.23,
                    'dividendPayableDate': 1676604060,
                    'pe': 26.0661,
                    'week52LowDate': 1672802460,
                    'week52HiDate': 1648693260,
                    'intrinsicValue': 0.0,
                    'timePremium': 0.0,
                    'optionMultiplier': 0.0,
                    'contractSize': 0.0,
                    'expirationDate': 0,
                    'timeOfLastTrade': 1676667600,
                    'averageVolume': 74285990,
                    'ExtendedHourQuoteDetail': {
                        'lastPrice': 152.64,
                        'change': -1.07,
                        'percentChange': -0.7,
                        'bid': 152.56,
                        'bidSize': 100,
                        'ask': 152.64,
                        'askSize': 600,
                        'volume': 59144118,
                        'timeOfLastTrade': 1676681997,
                        'timeZone': 'EST',
                        'quoteStatus': 'EH_CLOSED'
                    }
                },
                'Product': {
                    'symbol': 'AAPL', 'securityType': 'EQ'
                }
            },
            {
                'dateTime': '19:59:57 EST 02-17-2023',
                'dateTimeUTC': 1676681997,
                'quoteStatus': 'CLOSING',
                'ahFlag': 'true',
                'hasMiniOptions': False,
                'All': {
                    'adjustedFlag': False,
                    'ask': 94.6,
                    'askSize': 200,
                    'askTime': '19:59:57 EST 02-17-2023',
                    'bid': 94.5,
                    'bidExchange': '',
                    'bidSize': 500,
                    'bidTime': '19:59:57 EST 02-17-2023',
                    'changeClose': -1.19,
                    'changeClosePercentage': -1.24,
                    'companyName': 'ALPHABET INC CAP STK CL C',
                    'daysToExpiration': 0,
                    'dirLast': '1',
                    'dividend': 0.0,
                    'eps': 4.56,
                    'estEarnings': 5.067,
                    'exDividendDate': 0,
                    'high': 95.75,
                    'high52': 144.1625,
                    'lastTrade': 94.59,
                    'low': 93.45,
                    'low52': 83.45,
                    'open': 95.07,
                    'openInterest': 0,
                    'optionStyle': '',
                    'optionUnderlier': '',
                    'previousClose': 95.78,
                    'previousDayVolume': 36992919,
                    'primaryExchange': 'NSDQ',
                    'symbolDescription': 'ALPHABET INC CAP STK CL C',
                    'totalVolume': 31095067,
                    'upc': 0,
                    'cashDeliverable': 0,
                    'marketCap': 1211414130000.0,
                    'sharesOutstanding': 12807000000,
                    'nextEarningDate': '',
                    'beta': 1.41,
                    'yield': 0.0,
                    'declaredDividend': 0.0,
                    'dividendPayableDate': 0,
                    'pe': 21.0429,
                    'week52LowDate': 1667528460,
                    'week52HiDate': 1648606860,
                    'intrinsicValue': 0.0,
                    'timePremium': 0.0,
                    'optionMultiplier': 0.0,
                    'contractSize': 0.0,
                    'expirationDate': 0,
                    'timeOfLastTrade': 1676667600,
                    'averageVolume': 47510680,
                    'ExtendedHourQuoteDetail': {
                        'lastPrice': 94.54,
                        'change': -1.24,
                        'percentChange': -1.29,
                        'bid': 94.5,
                        'bidSize': 500,
                        'ask': 94.6,
                        'askSize': 200,
                        'volume': 31095067,
                        'timeOfLastTrade': 1676681997,
                        'timeZone': 'EST',
                        'quoteStatus': 'EH_CLOSED'
                    }
                },
                'Product': {
                    'symbol': 'GOOG', 'securityType': 'EQ'
                }
            }
        ]
    }
}

mock_get_portfolio_data = {
    'PortfolioResponse': {
        'AccountPortfolio': {
            'accountId': '58315636',
            'Position': [
                {
                    'positionId': '301369347900',
                    'Product': {
                        'expiryDay': '0',
                        'expiryMonth': '0',
                        'expiryYear': '0',
                        'productId': {
                            'symbol': 'FYX',
                            'typeCode': 'EQUITY'
                        },
                        'securitySubType': 'ETF',
                        'securityType': 'EQ',
                        'strikePrice': '0',
                        'symbol': 'FYX'
                    },
                    'symbolDescription': 'FYX',
                    'dateAcquired': '1676350800000',
                    'pricePaid': '86.90',
                    'commissions': '0',
                    'otherFees': '0',
                    'quantity': '11',
                    'positionIndicator': 'TYPE2',
                    'positionType': 'LONG',
                    'daysGain': '11.3871',
                    'daysGainPct': '1.216',
                    'marketValue': '947.8171',
                    'totalCost': '955.8999',
                    'totalGain': '-8.0828',
                    'totalGainPct': '-0.8455',
                    'pctOfPortfolio': '9.4585',
                    'costPerShare': '86.9',
                    'todayCommissions': '0',
                    'todayFees': '0',
                    'todayPricePaid': '0',
                    'todayQuantity': '0',
                    'adjPrevClose': '85.130000',
                    'Quick': {
                        'change': '1.0352',
                        'changePct': '1.216',
                        'lastTrade': '86.1652',
                        'lastTradeTime': '1677184587',
                        'quoteStatus': 'DELAYED',
                        'volume': '14449'
                    },
                    'lotsDetails': 'https://api.etrade.com/v1/accounts/vQMsebA1H5WltUfDkJP48g/portfolio/301369347900',
                    'quoteDetails': 'https://api.etrade.com/v1/market/quote/FYX'
                },
                {
                    'positionId': '301385125900',
                    'Product': {
                        'expiryDay': '0',
                        'expiryMonth': '0',
                        'expiryYear': '0',
                        'productId': {
                            'symbol': 'VIOG',
                            'typeCode': 'EQUITY'
                        },
                        'securitySubType': 'ETF',
                        'securityType': 'EQ',
                        'strikePrice': '0',
                        'symbol': 'VIOG'
                    },
                    'symbolDescription': 'VIOG',
                    'dateAcquired': '1676350800000',
                    'pricePaid': '200.4115',
                    'commissions': '0',
                    'otherFees': '0',
                    'quantity': '16',
                    'positionIndicator': 'TYPE2',
                    'positionType': 'LONG',
                    'daysGain': '19.4704',
                    'daysGainPct': '0.6167',
                    'marketValue': '3176.5599',
                    'totalCost': '3206.5849',
                    'totalGain': '-30.0249',
                    'totalGainPct': '-0.9363',
                    'pctOfPortfolio': '31.6997',
                    'costPerShare': '200.4115',
                    'todayCommissions': '0',
                    'todayFees': '0',
                    'todayPricePaid': '0',
                    'todayQuantity': '0',
                    'adjPrevClose': '197.318100',
                    'Quick': {
                        'change': '1.2169',
                        'changePct': '0.6167',
                        'lastTrade': '198.535',
                        'lastTradeTime': '1677182074',
                        'quoteStatus': 'DELAYED',
                        'volume': '3429'
                    },
                    'lotsDetails': 'https://api.etrade.com/v1/accounts/vQMsebA1H5WltUfDkJP48g/portfolio'
                                   '/301385125900',
                    'quoteDetails': 'https://api.etrade.com/v1/market/quote/VIOG'
                }
            ]
        }
    }
}

mock_preview_order = '<?xml version="1.0" encoding="UTF-8" ' \
                     'standalone="yes"?><PreviewOrderResponse><orderType>EQ</orderType><totalOrderValue>146.13' \
                     '</totalOrderValue><Order><orderTerm>GOOD_FOR_DAY</orderTerm><priceType>MARKET</priceType' \
                     '><limitPrice>0</limitPrice><stopPrice>0</stopPrice><marketSession>REGULAR</marketSession' \
                     '><allOrNone>false</allOrNone><Instrument><Product><symbol>AAPL</symbol><securityType>EQ' \
                     '</securityType></Product><symbolDescription>APPLE INC ' \
                     'COM</symbolDescription><orderAction>BUY</orderAction><quantityType>QUANTITY</quantityType' \
                     '><quantity>3</quantity><cancelQuantity>0.0</cancelQuantity><reserveOrder>true</reserveOrder' \
                     '><reserveQuantity>0.0</reserveQuantity></Instrument><egQual>EG_QUAL_NOT_IN_FORCE</egQual' \
                     '><estimatedCommission>0</estimatedCommission><estimatedTotalAmount>146.13</estimatedTotalAmount' \
                     '><netPrice>0</netPrice><netBid>0</netBid><netAsk>0</netAsk><gcd>0</gcd><ratio></ratio></Order' \
                     '><PreviewIds><previewId>{client_order_id}</previewId></PreviewIds><previewTime>1677267025597' \
                     '</previewTime><dstFlag>false</dstFlag><accountId>58315636</accountId><optionLevelCd>2' \
                     '</optionLevelCd><marginLevelCd>MARGIN_TRADING_ALLOWED</marginLevelCd><Disclosure' \
                     '><ahDisclosureFlag>false</ahDisclosureFlag><aoDisclosureFlag>true</aoDisclosureFlag' \
                     '><conditionalDisclosureFlag>true</conditionalDisclosureFlag><ehDisclosureFlag>false' \
                     '</ehDisclosureFlag></Disclosure><marginBpDetails><marginable><currentBp>4310.00</currentBp' \
                     '><currentNetBp>4310.00</currentNetBp><currentOor>0.00</currentOor><currentOrderImpact>146.13' \
                     '</currentOrderImpact><netBp>4163.87</netBp></marginable><nonMarginable><currentBp>2155.00' \
                     '</currentBp></nonMarginable></marginBpDetails></PreviewOrderResponse>'

mock_place_order = '<?xml version="1.0" encoding="UTF-8" ' \
                   'standalone="yes"?><PreviewOrderResponse><orderType>EQ</orderType><totalOrderValue>446.75' \
                   '</totalOrderValue><Order><orderTerm>GOOD_FOR_DAY</orderTerm><priceType>MARKET</priceType' \
                   '><limitPrice>0</limitPrice><stopPrice>0</stopPrice><marketSession>REGULAR</marketSession' \
                   '><allOrNone>false</allOrNone><Instrument><Product><symbol>GOOG</symbol><securityType>EQ' \
                   '</securityType></Product><symbolDescription>ALPHABET INC CAP STK CL ' \
                   'C</symbolDescription><orderAction>BUY</orderAction><quantityType>QUANTITY</quantityType><quantity' \
                   '>5</quantity><cancelQuantity>0.0</cancelQuantity><reserveOrder>true</reserveOrder' \
                   '><reserveQuantity>0.0</reserveQuantity></Instrument><egQual>EG_QUAL_NOT_IN_FORCE</egQual' \
                   '><estimatedCommission>0</estimatedCommission><estimatedTotalAmount>446.75</estimatedTotalAmount' \
                   '><netPrice>0</netPrice><netBid>0</netBid><netAsk>0</netAsk><gcd>0</gcd><ratio></ratio></Order' \
                   '><PreviewIds><previewId>{client_order_id}</previewId></PreviewIds><previewTime>1677282512846' \
                   '</previewTime><dstFlag>false</dstFlag><accountId>58315636</accountId><optionLevelCd>2' \
                   '</optionLevelCd><marginLevelCd>MARGIN_TRADING_ALLOWED</marginLevelCd><Disclosure' \
                   '><ahDisclosureFlag>false</ahDisclosureFlag><aoDisclosureFlag>true</aoDisclosureFlag' \
                   '><conditionalDisclosureFlag>true</conditionalDisclosureFlag><ehDisclosureFlag>false' \
                   '</ehDisclosureFlag></Disclosure><marginBpDetails><marginable><currentBp>4310.00</currentBp' \
                   '><currentNetBp>4310.00</currentNetBp><currentOor>0.00</currentOor><currentOrderImpact>500.89' \
                   '</currentOrderImpact><netBp>3809.12</netBp></marginable><nonMarginable><currentBp>2155.00' \
                   '</currentBp></nonMarginable></marginBpDetails></PreviewOrderResponse>'

mock_current_portfolio = current_portfolio = pd.Series(
    data=[17, 16, 19, 39, 11, 2, -6, -24],
    index=['QQQ', 'VIOG', 'PSCD', 'SPSM', 'FYX', 'VIOV', 'OIH', 'SPYV'],
    name='Shares'
)

mock_new_portfolio = new_portfolio = pd.DataFrame(
    data={
        'positionType': ['SHORT', 'SHORT', 'LONG', 'LONG', 'LONG', 'LONG', 'LONG', 'LONG'],
        'quantity': [-6, -25, 16, 39, 11, 2, 20, 17],
        'costPerShare': ['$328.46', '$41.66', '$200.41', '$40.54', '$86.90', '$176.25', '$93.30', '$302.33'],
        'marketValue': [
            '$-1,859.70', '$-1,009.00', '$3,162.17', '$1,555.71', '$939.84', '$345.88', '$1,828.20', '$4,961.45'
        ],
        'totalCost': [
            '$-1,970.76', '$-1,041.47', '$3,206.58', '$1,581.06', '$955.90', '$352.51', '$1,865.91', '$5,139.61'
        ],
        'daysGain': ['$-37.98', '$8.75', '$-18.36', '$-13.26', '$-9.57', '$-3.34', '$-21.24', '$-84.49'],
        'daysGainPct': ['-2.08%', '0.86%', '-0.58%', '-0.85%', '-1.01%', '-0.96%', '-1.15%', '-1.67%'],
        'totalGain': ['$111.06', '$32.47', '$-44.42', '$-25.35', '$-16.06', '$-6.63', '$-37.71', '$-178.16'],
        'totalGainPct': ['5.64%', '3.12%', '-1.39%', '-1.60%', '-1.68%', '-1.88%', '-2.02%', '-3.47%'],
        'pctOfPortfolio': ['-18.86%', '-10.23%', '32.07%', '15.78%', '9.53%', '3.51%', '18.54%', '50.31%']
    },
    index=['OIH', 'SPYV', 'VIOG', 'SPSM', 'FYX', 'VIOV', 'PSCD', 'QQQ'],
    columns=[
        'positionType', 'quantity', 'costPerShare', 'marketValue', 'totalCost', 'daysGain', 'daysGainPct',
        'totalGain', 'totalGainPct', 'pctOfPortfolio'
        ]
)
mock_new_portfolio.index.name = 'symbolDescription'

mock_summary_detail = {
    'QQQ': {
        'totalAssets': 156738928640,
    },
    'VIOG': {
        'totalAssets': 132355722.24000001,
    },
    'PSCD': {
        'totalAssets': 18090595.520000003,
    },
    'SPSM': {
        'totalAssets': 144030271.36,
    },
    'FYX': {
        'totalAssets': 141469231.36,
    }
}

np.random.seed(1)
last_business_days = pd.date_range(end='03/14/2023', periods=5, freq=BDay())
last_business_days_str = last_business_days.strftime('%Y-%m-%d')
mock_prices = pd.DataFrame(
    np.random.randn(5, 5) * 2 + 100, columns=['QQQ', 'VIOG', 'PSCD', 'SPSM', 'FYX'], index=last_business_days).round(2)
new_index = pd.date_range(start=mock_prices.index[0], end=mock_prices.index[-1], freq=BDay())
mock_prices.index = new_index

mock_market_caps = pd.Series({
    'QQQ': 156738928640,
    'VIOG': 132355722.24000001,
    'PSCD': 18090595.520000003,
    'SPSM': 144030271.36,
    'FYX': 141469231.36
    }, name='CUR_MKT_CAP'
)

mock_market_prices = pd.Series(
    data=[398.92, 391.56, 385.91, 385.36, 391.73],
    index=pd.date_range(start='2023-03-08', end='2023-03-14', freq='B'),
    name='SPDR S&P 500 ETF Trust'
)
mock_market_prices.index.name = 'SPY'
