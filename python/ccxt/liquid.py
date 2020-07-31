# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce


class liquid(Exchange):

    def describe(self):
        return self.deep_extend(super(liquid, self).describe(), {
            'id': 'liquid',
            'name': 'Liquid',
            'countries': ['JP', 'CN', 'TW'],
            'version': '2',
            'rateLimit': 1000,
            'has': {
                'CORS': False,
                'fetchCurrencies': True,
                'fetchTickers': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/45798859-1a872600-bcb4-11e8-8746-69291ce87b04.jpg',
                'api': 'https://api.liquid.com',
                'www': 'https://www.liquid.com',
                'doc': [
                    'https://developers.liquid.com',
                ],
                'fees': 'https://help.liquid.com/getting-started-with-liquid/the-platform/fee-structure',
                'referral': 'https://www.liquid.com?affiliate=SbzC62lt30976',
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'products',
                        'products/{id}',
                        'products/{id}/price_levels',
                        'executions',
                        'ir_ladders/{currency}',
                        'fees',  # add fetchFees, fetchTradingFees, fetchFundingFees
                    ],
                },
                'private': {
                    'get': [
                        'accounts/balance',
                        'accounts/main_asset',
                        'accounts/{id}',
                        'accounts/{currency}/reserved_balance_details',
                        'crypto_accounts',  # add fetchAccounts
                        'crypto_withdrawals',  # add fetchWithdrawals
                        'executions/me',
                        'fiat_accounts',  # add fetchAccounts
                        'fund_infos',  # add fetchDeposits
                        'loan_bids',
                        'loans',
                        'orders',
                        'orders/{id}',
                        'orders/{id}/trades',  # add fetchOrderTrades
                        'trades',
                        'trades/{id}/loans',
                        'trading_accounts',
                        'trading_accounts/{id}',
                        'transactions',
                        'withdrawals',  # add fetchWithdrawals
                    ],
                    'post': [
                        'crypto_withdrawals',
                        'fund_infos',
                        'fiat_accounts',
                        'loan_bids',
                        'orders',
                        'withdrawals',
                    ],
                    'put': [
                        'crypto_withdrawal/{id}/cancel',
                        'loan_bids/{id}/close',
                        'loans/{id}',
                        'orders/{id}',  # add editOrder
                        'orders/{id}/cancel',
                        'trades/{id}',
                        'trades/{id}/adjust_margin',
                        'trades/{id}/close',
                        'trades/close_all',
                        'trading_accounts/{id}',
                        'withdrawals/{id}/cancel',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': 0.0015,
                    'maker': 0.0000,
                    'tiers': {
                        'perpetual': {
                            'maker': [
                                [0, 0.0000],
                                [25000, 0.0000],
                                [50000, -0.00025],
                                [100000, -0.00025],
                                [1000000, -0.00025],
                                [10000000, -0.00025],
                                [25000000, -0.00025],
                                [50000000, -0.00025],
                                [75000000, -0.00025],
                                [100000000, -0.00025],
                                [200000000, -0.00025],
                                [300000000, -0.00025],
                            ],
                            'taker': [
                                [0, 0.000600],
                                [25000, 0.000575],
                                [50000, 0.000550],
                                [100000, 0.000525],
                                [1000000, 0.000500],
                                [10000000, 0.000475],
                                [25000000, 0.000450],
                                [50000000, 0.000425],
                                [75000000, 0.000400],
                                [100000000, 0.000375],
                                [200000000, 0.000350],
                                [300000000, 0.000325],
                            ],
                        },
                        'spot': {
                            'taker': [
                                [0, 0.0015],
                                [10000, 0.0015],
                                [20000, 0.0014],
                                [50000, 0.0013],
                                [100000, 0.0010],
                                [1000000, 0.0008],
                                [5000000, 0.0006],
                                [10000000, 0.0005],
                                [25000000, 0.0005],
                                [50000000, 0.00045],
                                [100000000, 0.0004],
                                [200000000, 0.0003],
                            ],
                            'maker': [
                                [0, 0.0000],
                                [10000, 0.0015],
                                [20000, 0.1400],
                                [50000, 0.1300],
                                [100000, 0.0800],
                                [1000000, 0.0004],
                                [5000000, 0.00035],
                                [10000000, 0.00025],
                                [25000000, 0.0000],
                                [50000000, 0.0000],
                                [100000000, 0.0000],
                                [200000000, 0.0000],
                            ],
                        },
                    },
                },
            },
            'exceptions': {
                'API rate limit exceeded. Please retry after 300s': DDoSProtection,
                'API Authentication failed': AuthenticationError,
                'Nonce is too small': InvalidNonce,
                'Order not found': OrderNotFound,
                'Can not update partially filled order': InvalidOrder,
                'Can not update non-live order': OrderNotFound,
                'not_enough_free_balance': InsufficientFunds,
                'must_be_positive': InvalidOrder,
                'less_than_order_size': InvalidOrder,
                'price_too_high': InvalidOrder,
            },
            'commonCurrencies': {
                'WIN': 'WCOIN',
                'HOT': 'HOT Token',
            },
            'options': {
                'cancelOrderException': True,
            },
        })

    def fetch_currencies(self, params={}):
        response = self.publicGetCurrencies(params)
        #
        #     [
        #         {
        #             currency_type: 'fiat',
        #             currency: 'USD',
        #             symbol: '$',
        #             assets_precision: 2,
        #             quoting_precision: 5,
        #             minimum_withdrawal: '15.0',
        #             withdrawal_fee: 5,
        #             minimum_fee: null,
        #             minimum_order_quantity: null,
        #             display_precision: 2,
        #             depositable: True,
        #             withdrawable: True,
        #             discount_fee: 0.5,
        #         },
        #     ]
        #
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'currency')
            code = self.safe_currency_code(id)
            active = currency['depositable'] and currency['withdrawable']
            amountPrecision = self.safe_integer(currency, 'display_precision')
            pricePrecision = self.safe_integer(currency, 'quoting_precision')
            precision = max(amountPrecision, pricePrecision)
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': code,
                'active': active,
                'fee': self.safe_float(currency, 'withdrawal_fee'),
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -amountPrecision),
                        'max': math.pow(10, amountPrecision),
                    },
                    'price': {
                        'min': math.pow(10, -pricePrecision),
                        'max': math.pow(10, pricePrecision),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.safe_float(currency, 'minimum_withdrawal'),
                        'max': None,
                    },
                },
            }
        return result

    def fetch_markets(self, params={}):
        spot = self.publicGetProducts(params)
        #
        #     [
        #         {
        #             id: '7',
        #             product_type: 'CurrencyPair',
        #             code: 'CASH',
        #             name: ' CASH Trading',
        #             market_ask: 8865.79147,
        #             market_bid: 8853.95988,
        #             indicator: 1,
        #             currency: 'SGD',
        #             currency_pair_code: 'BTCSGD',
        #             symbol: 'S$',
        #             btc_minimum_withdraw: null,
        #             fiat_minimum_withdraw: null,
        #             pusher_channel: 'product_cash_btcsgd_7',
        #             taker_fee: 0,
        #             maker_fee: 0,
        #             low_market_bid: '8803.25579',
        #             high_market_ask: '8905.0',
        #             volume_24h: '15.85443468',
        #             last_price_24h: '8807.54625',
        #             last_traded_price: '8857.77206',
        #             last_traded_quantity: '0.00590974',
        #             quoted_currency: 'SGD',
        #             base_currency: 'BTC',
        #             disabled: False,
        #         },
        #     ]
        #
        perpetual = self.publicGetProducts({'perpetual': '1'})
        #
        #     [
        #         {
        #             "id": "603",
        #             "product_type": "Perpetual",
        #             "code": "CASH",
        #             "name": null,
        #             "market_ask": "1143900",
        #             "market_bid": "1143250",
        #             "currency": "JPY",
        #             "currency_pair_code": "P-BTCJPY",
        #             "pusher_channel": "product_cash_p-btcjpy_603",
        #             "taker_fee": "0.0",
        #             "maker_fee": "0.0",
        #             "low_market_bid": "1124450.0",
        #             "high_market_ask": "1151750.0",
        #             "volume_24h": "0.1756",
        #             "last_price_24h": "1129850.0",
        #             "last_traded_price": "1144700.0",
        #             "last_traded_quantity": "0.014",
        #             "quoted_currency": "JPY",
        #             "base_currency": "P-BTC",
        #             "tick_size": "50.0",
        #             "perpetual_enabled": True,
        #             "index_price": "1142636.03935",
        #             "mark_price": "1143522.18417",
        #             "funding_rate": "0.00033",
        #             "fair_price": "1143609.31009",
        #             "timestamp": "1581558659.195353100",
        #         },
        #     ]
        #
        currencies = self.fetch_currencies()
        currenciesByCode = self.index_by(currencies, 'code')
        result = []
        markets = self.array_concat(spot, perpetual)
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'id')
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'quoted_currency')
            productType = self.safe_string(market, 'product_type')
            type = 'spot'
            spot = True
            swap = False
            if productType == 'Perpetual':
                spot = False
                swap = True
                type = 'swap'
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = None
            if swap:
                symbol = self.safe_string(market, 'currency_pair_code')
            else:
                symbol = base + '/' + quote
            maker = self.fees['trading']['maker']
            taker = self.fees['trading']['taker']
            if type == 'swap':
                maker = self.safe_float(market, 'maker_fee', self.fees['trading']['maker'])
                taker = self.safe_float(market, 'taker_fee', self.fees['trading']['taker'])
            disabled = self.safe_value(market, 'disabled', False)
            active = not disabled
            baseCurrency = self.safe_value(currenciesByCode, base)
            quoteCurrency = self.safe_value(currenciesByCode, quote)
            precision = {
                'amount': 8,
                'price': 8,
            }
            minAmount = None
            if baseCurrency is not None:
                minAmount = self.safe_float(baseCurrency['info'], 'minimum_order_quantity')
                # precision['amount'] = self.safe_integer(baseCurrency['info'], 'quoting_precision')
            minPrice = None
            if quoteCurrency is not None:
                precision['price'] = self.safe_integer(quoteCurrency['info'], 'quoting_precision')
                minPrice = math.pow(10, -precision['price'])
            minCost = None
            if minPrice is not None:
                if minAmount is not None:
                    minCost = minPrice * minAmount
            limits = {
                'amount': {
                    'min': minAmount,
                    'max': None,
                },
                'price': {
                    'min': minPrice,
                    'max': None,
                },
                'cost': {
                    'min': minCost,
                    'max': None,
                },
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'type': type,
                'spot': spot,
                'swap': swap,
                'maker': maker,
                'taker': taker,
                'limits': limits,
                'precision': precision,
                'active': active,
                'info': market,
            })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccountsBalance(params)
        #
        #     [
        #         {"currency":"USD","balance":"0.0"},
        #         {"currency":"BTC","balance":"0.0"},
        #         {"currency":"ETH","balance":"0.1651354"}
        #     ]
        #
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['total'] = self.safe_float(balance, 'balance')
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        response = self.publicGetProductsIdPriceLevels(self.extend(request, params))
        return self.parse_order_book(response, None, 'buy_price_levels', 'sell_price_levels')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        last = None
        if 'last_traded_price' in ticker:
            if ticker['last_traded_price']:
                length = len(ticker['last_traded_price'])
                if length > 0:
                    last = self.safe_float(ticker, 'last_traded_price')
        symbol = None
        if market is None:
            marketId = self.safe_string(ticker, 'id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId = self.safe_string(ticker, 'base_currency')
                quoteId = self.safe_string(ticker, 'quoted_currency')
                if symbol in self.markets:
                    market = self.markets[symbol]
                else:
                    symbol = self.safe_currency_code(baseId) + '/' + self.safe_currency_code(quoteId)
        if market is not None:
            symbol = market['symbol']
        change = None
        percentage = None
        average = None
        open = self.safe_float(ticker, 'last_price_24h')
        if open is not None and last is not None:
            change = last - open
            average = self.sum(last, open) / 2
            if open > 0:
                percentage = change / open * 100
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high_market_ask'),
            'low': self.safe_float(ticker, 'low_market_bid'),
            'bid': self.safe_float(ticker, 'market_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'market_ask'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'volume_24h'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetProducts(params)
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.publicGetProductsId(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        # {            id:  12345,
        #         quantity: "6.789",
        #            price: "98765.4321",
        #       taker_side: "sell",
        #       created_at:  1512345678,
        #          my_side: "buy"           }
        timestamp = self.safe_timestamp(trade, 'created_at')
        orderId = self.safe_string(trade, 'order_id')
        # 'taker_side' gets filled for both fetchTrades and fetchMyTrades
        takerSide = self.safe_string(trade, 'taker_side')
        # 'my_side' gets filled for fetchMyTrades only and may differ from 'taker_side'
        mySide = self.safe_string(trade, 'my_side')
        side = mySide if (mySide is not None) else takerSide
        takerOrMaker = None
        if mySide is not None:
            takerOrMaker = 'taker' if (takerSide == mySide) else 'maker'
        cost = None
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'quantity')
        if price is not None:
            if amount is not None:
                cost = price * amount
        id = self.safe_string(trade, 'id')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': side,
            'takerOrMaker': takerOrMaker,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'product_id': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        if since is not None:
            # timestamp should be in seconds, whereas we use milliseconds in since and everywhere
            request['timestamp'] = int(since / 1000)
        response = self.publicGetExecutions(self.extend(request, params))
        result = response if (since is not None) else response['models']
        return self.parse_trades(result, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        # the `with_details` param is undocumented - it adds the order_id to the results
        request = {
            'product_id': market['id'],
            'with_details': True,
        }
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetExecutionsMe(self.extend(request, params))
        return self.parse_trades(response['models'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        clientOrderId = self.safe_string_2(params, 'clientOrderId', 'client_order_id')
        params = self.omit(params, ['clientOrderId', 'client_order_id'])
        request = {
            'order_type': type,
            'product_id': self.market_id(symbol),
            'side': side,
            'quantity': self.amount_to_precision(symbol, amount),
        }
        if clientOrderId is not None:
            request['client_order_id'] = clientOrderId
        if (type == 'limit') or (type == 'limit_post_only') or (type == 'market_with_range') or (type == 'stop'):
            request['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #         "id": 2157474,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.0",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "live",
        #         "leverage_level": 1,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0",
        #         "client_order_id": null,
        #     }
        #
        return self.parse_order(response)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privatePutOrdersIdCancel(self.extend(request, params))
        order = self.parse_order(response)
        if order['status'] == 'closed':
            if self.options['cancelOrderException']:
                raise OrderNotFound(self.id + ' order closed already: ' + self.json(response))
        return order

    def edit_order(self, id, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if price is None:
            raise ArgumentsRequired(self.id + ' editOrder requires the price argument')
        request = {
            'order': {
                'quantity': self.amount_to_precision(symbol, amount),
                'price': self.price_to_precision(symbol, price),
            },
            'id': id,
        }
        response = self.privatePutOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def parse_order_status(self, status):
        statuses = {
            'live': 'open',
            'filled': 'closed',
            'cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        # createOrder
        #
        #     {
        #         "id": 2157474,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.0",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "live",
        #         "leverage_level": 1,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0"
        #         "client_order_id": null,
        #     }
        #
        # fetchOrder, fetchOrders, fetchOpenOrders, fetchClosedOrders
        #
        #     {
        #         "id": 2157479,
        #         "order_type": "limit",
        #         "quantity": "0.01",
        #         "disc_quantity": "0.0",
        #         "iceberg_total_quantity": "0.0",
        #         "side": "sell",
        #         "filled_quantity": "0.01",
        #         "price": "500.0",
        #         "created_at": 1462123639,
        #         "updated_at": 1462123639,
        #         "status": "filled",
        #         "leverage_level": 2,
        #         "source_exchange": "QUOINE",
        #         "product_id": 1,
        #         "product_code": "CASH",
        #         "funding_currency": "USD",
        #         "currency_pair_code": "BTCUSD",
        #         "order_fee": "0.0",
        #         "executions": [
        #             {
        #                 "id": 4566133,
        #                 "quantity": "0.01",
        #                 "price": "500.0",
        #                 "taker_side": "buy",
        #                 "my_side": "sell",
        #                 "created_at": 1465396785
        #             }
        #         ]
        #     }
        #
        orderId = self.safe_string(order, 'id')
        timestamp = self.safe_timestamp(order, 'created_at')
        marketId = self.safe_string(order, 'product_id')
        market = self.safe_value(self.markets_by_id, marketId)
        status = self.parse_order_status(self.safe_string(order, 'status'))
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'filled_quantity')
        price = self.safe_float(order, 'price')
        symbol = None
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        type = self.safe_string(order, 'order_type')
        tradeCost = 0
        tradeFilled = 0
        average = self.safe_float(order, 'average_price')
        trades = self.parse_trades(self.safe_value(order, 'executions', []), market, None, None, {
            'order': orderId,
            'type': type,
        })
        numTrades = len(trades)
        for i in range(0, numTrades):
            # php copies values upon assignment, but not references them
            # todo rewrite self(shortly)
            trade = trades[i]
            trade['order'] = orderId
            trade['type'] = type
            tradeFilled = self.sum(tradeFilled, trade['amount'])
            tradeCost = self.sum(tradeCost, trade['cost'])
        cost = None
        lastTradeTimestamp = None
        if numTrades > 0:
            lastTradeTimestamp = trades[numTrades - 1]['timestamp']
            if not average and (tradeFilled > 0):
                average = tradeCost / tradeFilled
            if cost is None:
                cost = tradeCost
            if filled is None:
                filled = tradeFilled
        remaining = None
        if amount is not None and filled is not None:
            remaining = amount - filled
        side = self.safe_string(order, 'side')
        clientOrderId = self.safe_string(order, 'client_order_id')
        return {
            'id': orderId,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'type': type,
            'status': status,
            'symbol': symbol,
            'side': side,
            'price': price,
            'amount': amount,
            'filled': filled,
            'cost': cost,
            'remaining': remaining,
            'average': average,
            'trades': trades,
            'fee': {
                'currency': feeCurrency,
                'cost': self.safe_float(order, 'order_fee'),
            },
            'info': order,
        }

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privateGetOrdersId(self.extend(request, params))
        return self.parse_order(response)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {
            # 'funding_currency': market['quoteId'],  # filter orders based on "funding" currency(quote currency)
            # 'product_id': market['id'],
            # 'status': 'live',  # 'filled', 'cancelled'
            # 'trading_type': 'spot',  # 'margin', 'cfd'
            'with_details': 1,  # return full order details including executions
        }
        if symbol is not None:
            market = self.market(symbol)
            request['product_id'] = market['id']
        if limit is not None:
            request['limit'] = limit
        response = self.privateGetOrders(self.extend(request, params))
        #
        #     {
        #         "models": [
        #             {
        #                 "id": 2157474,
        #                 "order_type": "limit",
        #                 "quantity": "0.01",
        #                 "disc_quantity": "0.0",
        #                 "iceberg_total_quantity": "0.0",
        #                 "side": "sell",
        #                 "filled_quantity": "0.0",
        #                 "price": "500.0",
        #                 "created_at": 1462123639,
        #                 "updated_at": 1462123639,
        #                 "status": "live",
        #                 "leverage_level": 1,
        #                 "source_exchange": "QUOINE",
        #                 "product_id": 1,
        #                 "product_code": "CASH",
        #                 "funding_currency": "USD",
        #                 "currency_pair_code": "BTCUSD",
        #                 "order_fee": "0.0",
        #                 "executions": [],  # optional
        #             }
        #         ],
        #         "current_page": 1,
        #         "total_pages": 1
        #     }
        #
        orders = self.safe_value(response, 'models', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'live'}
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': 'filled'}
        return self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            # 'auth_code': '',  # optional 2fa code
            'currency': currency['id'],
            'address': address,
            'amount': self.currency_to_precision(code, amount),
            # 'payment_id': tag,  # for XRP only
            # 'memo_type': 'text',  # 'text', 'id' or 'hash', for XLM only
            # 'memo_value': tag,  # for XLM only
        }
        if tag is not None:
            if code == 'XRP':
                request['payment_id'] = tag
            elif code == 'XLM':
                request['memo_type'] = 'text'  # overrideable via params
                request['memo_value'] = tag
            else:
                raise NotSupported(self.id + ' withdraw() only supports a tag along the address for XRP or XLM')
        response = self.privatePostCryptoWithdrawals(self.extend(request, params))
        #
        #     {
        #         "id": 1353,
        #         "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        #         "amount": 1.0,
        #         "state": "pending",
        #         "currency": "BTC",
        #         "withdrawal_fee": 0.0,
        #         "created_at": 1568016450,
        #         "updated_at": 1568016450,
        #         "payment_id": null
        #     }
        #
        return self.parse_transaction(response, currency)

    def parse_transaction_status(self, status):
        statuses = {
            'pending': 'pending',
            'cancelled': 'canceled',
            'approved': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # withdraw
        #
        #     {
        #         "id": 1353,
        #         "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
        #         "amount": 1.0,
        #         "state": "pending",
        #         "currency": "BTC",
        #         "withdrawal_fee": 0.0,
        #         "created_at": 1568016450,
        #         "updated_at": 1568016450,
        #         "payment_id": null
        #     }
        #
        # fetchDeposits, fetchWithdrawals
        #
        #     ...
        #
        id = self.safe_string(transaction, 'id')
        address = self.safe_string(transaction, 'address')
        tag = self.safe_string_2(transaction, 'payment_id', 'memo_value')
        txid = None
        currencyId = self.safe_string(transaction, 'asset')
        code = self.safe_currency_code(currencyId, currency)
        timestamp = self.safe_timestamp(transaction, 'created_at')
        updated = self.safe_timestamp(transaction, 'updated_at')
        type = 'withdrawal'
        status = self.parse_transaction_status(self.safe_string(transaction, 'state'))
        amount = self.safe_float(transaction, 'amount')
        return {
            'info': transaction,
            'id': id,
            'txid': txid,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,
            'type': type,
            'amount': amount,
            'currency': code,
            'status': status,
            'updated': updated,
            'fee': None,
        }

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        headers = {
            'X-Quoine-API-Version': self.version,
            'Content-Type': 'application/json',
        }
        if api == 'private':
            self.check_required_credentials()
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            elif query:
                body = self.json(query)
            nonce = self.nonce()
            request = {
                'path': url,
                'token_id': self.apiKey,
                'iat': int(math.floor(nonce / 1000)),  # issued at
            }
            if not ('client_order_id' in query):
                request['nonce'] = nonce
            headers['X-Quoine-Auth'] = self.jwt(request, self.encode(self.secret))
        else:
            if query:
                url += '?' + self.urlencode(query)
        url = self.urls['api'] + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if code >= 200 and code < 300:
            return
        if code == 401:
            # expected non-json response
            self.throw_exactly_matched_exception(self.exceptions, body, body)
            return
        if code == 429:
            raise DDoSProtection(self.id + ' ' + body)
        if response is None:
            return
        feedback = self.id + ' ' + body
        message = self.safe_string(response, 'message')
        errors = self.safe_value(response, 'errors')
        if message is not None:
            #
            #  {"message": "Order not found"}
            #
            self.throw_exactly_matched_exception(self.exceptions, message, feedback)
        elif errors is not None:
            #
            #  {"errors": {"user": ["not_enough_free_balance"]}}
            #  {"errors": {"quantity": ["less_than_order_size"]}}
            #  {"errors": {"order": ["Can not update partially filled order"]}}
            #
            types = list(errors.keys())
            for i in range(0, len(types)):
                type = types[i]
                errorMessages = errors[type]
                for j in range(0, len(errorMessages)):
                    message = errorMessages[j]
                    self.throw_exactly_matched_exception(self.exceptions, message, feedback)
        else:
            raise ExchangeError(feedback)
