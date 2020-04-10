# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadResponse


class biki(Exchange):

    def describe(self):
        return self.deep_extend(super(biki, self).describe(), {
            'id': 'biki',
            'name': 'Biki',
            'countries': ['CN'],
            'version': 'v1',
            'rateLimit': 10,
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': False,
                'withdraw': False,
                'fetchDeposits': False,
                'fetchWithdrawals': False,
                'fetchTransactions': False,
                'createDepositAddress': False,
                'fetchDepositAddress': False,
                'fetchClosedOrders': False,
                'fetchOHLCV': True,
                'fetchOpenOrders': False,
                'fetchOrderTrades': False,
                'fetchOrders': True,
                'fetchOrder': True,
                'fetchMyTrades': False,
            },
            'timeframes': {
                '1m': '60',
                '5m': '300',
                '15m': '900',
                '30m': '1800',
                '60m': '3600',
                '1h': '3600',
                '2h': '7200',
                '4h': '14400',
                '6h': '21600',
                '12h': '43200',
                '1d': '86400',
                '1w': '604800',
            },
            'urls': {
                'logo': '',
                'api': {
                    'public': 'https://openapi.biki.com/open/api/',
                    'private': 'https://openapi.biki.com/open/api/',
                },
                'www': 'https://biki.com/',
                'doc': 'https://github.com/code-biki/open-api',
                'fees': [
                    'https://bikiuser.zendesk.com/hc/zh-cn/articles/360019543671-BiKi%E8%B4%B9%E7%8E%87%E8%AF%B4%E6%98%8E',
                ],
                'referral': '',
            },
            'api': {
                'public': {
                    'get': [
                        'common/symbols',
                        'market_dept',
                        'get_trades',
                        'get_ticker',
                        'get_records',
                    ],
                },
                'private': {
                    'get': [
                        'user/account',
                        'v2/all_order',
                        'order_info',
                    ],
                    'post': [
                        'create_order',
                        'mass_replaceV2',
                        'cancel_order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'maker': 0.0015,
                    'taker': 0.0015,
                },
            },
            'exceptions': {
                '1': BadResponse,
            },
            'errorCodeNames': {
            },
            'options': {
                'limits': {
                    'cost': {
                        'min': {
                        },
                    },
                },
            },
        })

    async def fetch_markets(self, params={}):
        response = await self.publicGetCommonSymbols(params)
        markets = self.safe_value(response, 'data')
        if not markets:
            raise ExchangeError(self.id + ' fetchMarkets got an unrecognized response')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['symbol']
            baseId = market['base_coin']
            quoteId = market['count_coin']
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': self.safe_integer(market, 'amount_precision'),
                'price': self.safe_integer(market, 'price_precision'),
            }
            amountLimits = {
                'min': math.pow(10, -market['amount_precision']),
                'max': None,
            }
            priceLimits = {
                'min': math.pow(10, -market['price_precision']),
                'max': None,
            }
            defaultCost = amountLimits['min'] * priceLimits['min']
            minCost = self.safe_float(self.options['limits']['cost']['min'], quote, defaultCost)
            costLimits = {
                'min': minCost,
                'max': None,
            }
            limits = {
                'amount': amountLimits,
                'price': priceLimits,
                'cost': costLimits,
            }
            active = True
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': limits,
            })
        return result

    async def fetch_balance(self, params={}):
        await self.load_markets()
        request = {
            'api_key': self.apiKey,
            'time': self.milliseconds(),
        }
        response = await self.privateGetUserAccount(self.extend(request, params))
        respData = self.safe_value(response, 'data')
        result = {'info': respData}
        coins = self.safe_value(respData, 'coin_list')
        for i in range(0, len(coins)):
            coin = coins[i]
            currencyId = self.safe_value(coin, 'coin')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(coin, 'normal')
            account['used'] = self.safe_float(coin, 'locked')
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'type': 'step0',
            'symbol': self.market_id(symbol),
        }
        response = await self.publicGetMarketDept(self.extend(request, params))
        data = self.safe_value(response, 'data')
        orderbook = self.safe_value(data, 'tick')
        return self.parse_order_book(orderbook)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        # they return [Timestamp, Volume, Close, High, Low, Open]
        return [
            int(ohlcv[0]),   # t
            float(ohlcv[1]),  # o
            float(ohlcv[2]),  # c
            float(ohlcv[3]),  # h
            float(ohlcv[4]),  # l
            float(ohlcv[5]),  # v
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        periodDurationInSeconds = self.parse_timeframe(timeframe)
        request = {
            'symbol': self.market_id(symbol),
            'period': periodDurationInSeconds / 60,  # in minute
        }
        # max limit = 1001
        # since & limit not supported
        response = await self.publicGetGetRecords(self.extend(request, params))
        #        ordering: Ts, O, C, H, L, V
        #     {
        #         "code": 200,
        #         "data": [
        #             ["TS", "o", "c", "h", "l", "v"],
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        percentage = self.safe_float(ticker, 'rose')
        open = self.safe_float(ticker, 'open')
        change = None
        average = None
        if (last is not None) and (percentage is not None):
            change = last - open
            average = self.sum(last, open) / 2
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        ticker = await self.publicGetGetTicker(self.extend({
            'symbol': self.market_id(symbol),
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        # API doc says 'ts', but in fact it is 'ctime'
        timestamp = self.safe_timestamp(trade, 'ctime') / 1000
        # take either of orderid or orderId
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        type = self.safe_string(trade, 'type')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'id': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
            'side': type == 'buy' if '1' else 'sell',
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': self.market_id(symbol),
        }
        response = await self.publicGetGetTrades(self.extend(request, params))
        data = self.safe_value(response, 'data')
        if not data:
            raise ExchangeError(self.id + ' fetchTrades got an unrecognized response')
        return self.parse_trades(data, market, since, limit)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'api_key': self.apiKey,
            'time': self.milliseconds(),
        }
        response = await self.privateGetCurrentOrders(self.extend(request, params))
        return self.parse_orders(response['data'], None, since, limit)

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        request = {
            'order_id': id,
            'symbol': self.market_id(symbol),
            'api_key': self.apiKey,
            'time': self.milliseconds(),
        }
        response = await self.privateGetOrderInfo(self.extend(request, params))
        return self.parse_order(response['data']['order_info'])

    def parse_order_side(self, side):
        sides = {
            '1': 'buy',
            '2': 'sell',
        }
        return self.safe_string(sides, side, side)

    def parse_order_status(self, status):
        statuses = {
            '0': 'open',
            '1': 'open',
            '2': 'closed',
            '3': 'open',  # partial closed
            '4': 'canceled',  # partial closed
            '5': 'canceled',  # partial canceled
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        # Different API endpoints returns order info in different format...
        # with different fields filled.
        id = self.safe_string(order, 'id')
        if id is None:
            id = self.safe_string(order, 'order_id')
        symbol = None
        marketId = None
        if ('baseCoin' in order) and ('countCoin' in order):
            marketId = self.safe_string_lower(order, 'baseCoin') + self.safe_string_lower(order, 'countCoin')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            if market is not None:
                symbol = market['symbol']
        if 'symbol' in order:
            symbol = self.safe_string(order, 'symbol')
        timestamp = None
        datetime = None
        if 'created_at' in order:
            timestamp = self.safe_timestamp(order, 'created_at') / 1000
            datetime = self.iso8601(timestamp)
        status = self.parse_order_status(self.safe_string(order, 'status'))
        side = self.parse_order_side(self.safe_string(order, 'type'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'volume')
        filled = self.safe_float(order, 'deal_volume')
        average = self.safe_float(order, 'avg_price')
        remaining = self.safe_float(order, 'remain_volume')
        return {
            'id': id,
            'datetime': datetime,
            'timestamp': timestamp,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'average': average,
            'trades': None,
            'fee': {
                'cost': None,
                'currency': None,
                'rate': None,
            },
            'info': order,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type == 'market':
            # https://github.com/code-biki/open-api#%E5%88%9B%E5%BB%BA%E8%AE%A2%E5%8D%95
            # their API for market order is crap, not supporting market orders for now
            raise ExchangeError(self.id + ' allows limit orders only')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'api_key': self.apiKey,
            'time': self.milliseconds(),
            'symbol': self.market_id(symbol),
            'price': price,
            'volume': amount,
            'side': side.upper(),
            'type': '1',  # limit order
        }
        response = await self.privatePostCreateOrder(self.extend(request, params))
        return self.parse_order(self.extend({
            'status': 'open',
            'side': side,
            'amount': amount,
            'type': type,
            'symbol': symbol,
        }, self.safe_value(response, 'data')), market)

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires symbol argument')
        await self.load_markets()
        request = {
            'api_key': self.apiKey,
            'time': self.milliseconds(),
            'symbol': self.market_id(symbol),
            'order_id': id,
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            auth = self.rawencode(self.keysort(query))
            to_sign = auth.replace('=', '').replace('&', '')
            signature = self.hash(self.encode(to_sign + self.secret), 'md5')
            suffix = 'sign=' + signature
            url += '?' + auth + '&' + suffix
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        # use response code for error
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg', body)
        if errorCode is not None and errorCode != '0':
            feedback = self.safe_string(self.errorCodeNames, errorCode, message)
            # XXX: just throwing generic error when API call went wrong
            self.throw_exactly_matched_exception(self.exceptions, '1', feedback)
