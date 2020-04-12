<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import
use \ccxt\ExchangeError;
use \ccxt\ArgumentsRequired;

class biki extends Exchange {

    public function describe() {
        return $this->deep_extend(parent::describe (), array(
            'id' => 'biki',
            'name' => 'Biki',
            'countries' => array( 'CN' ),
            'version' => 'v1',
            'rateLimit' => 10,
            'has' => array(
                'CORS' => false,
                'createMarketOrder' => false,
                'fetchTickers' => false,
                'withdraw' => false,
                'fetchDeposits' => false,
                'fetchWithdrawals' => false,
                'fetchTransactions' => false,
                'createDepositAddress' => false,
                'fetchDepositAddress' => false,
                'fetchClosedOrders' => false,
                'fetchOHLCV' => true,
                'fetchOpenOrders' => false,
                'fetchOrderTrades' => false,
                'fetchOrders' => true,
                'fetchOrder' => true,
                'fetchMyTrades' => false,
            ),
            'timeframes' => array(
                '1m' => '60',
                '5m' => '300',
                '15m' => '900',
                '30m' => '1800',
                '60m' => '3600',
                '1h' => '3600',
                '2h' => '7200',
                '4h' => '14400',
                '6h' => '21600',
                '12h' => '43200',
                '1d' => '86400',
                '1w' => '604800',
            ),
            'urls' => array(
                'logo' => '',
                'api' => array(
                    'public' => 'https://openapi.biki.com/open/api/',
                    'private' => 'https://openapi.biki.com/open/api/',
                ),
                'www' => 'https://biki.com/',
                'doc' => 'https://github.com/code-biki/open-api',
                'fees' => array(
                    'https://bikiuser.zendesk.com/hc/zh-cn/articles/360019543671-BiKi%E8%B4%B9%E7%8E%87%E8%AF%B4%E6%98%8E',
                ),
                'referral' => '',
            ),
            'api' => array(
                'public' => array(
                    'get' => array(
                        'common/symbols',
                        'market_dept',
                        'get_trades',
                        'get_ticker',
                        'get_records',
                    ),
                ),
                'private' => array(
                    'get' => array(
                        'user/account',
                        'v2/all_order',
                        'order_info',
                    ),
                    'post' => array(
                        'create_order',
                        'mass_replaceV2',
                        'cancel_order',
                    ),
                ),
            ),
            'fees' => array(
                'trading' => array(
                    'tierBased' => true,
                    'percentage' => true,
                    'maker' => 0.0015,
                    'taker' => 0.0015,
                ),
            ),
            'exceptions' => array(
                '1' => '\\ccxt\\BadResponse',
            ),
            'errorCodeNames' => array(
            ),
            'options' => array(
                'limits' => array(
                    'cost' => array(
                        'min' => array(
                        ),
                    ),
                ),
            ),
        ));
    }

    public function fetch_markets($params = array ()) {
        $response = $this->publicGetCommonSymbols ($params);
        $markets = $this->safe_value($response, 'data');
        if (!$markets) {
            throw new ExchangeError($this->id . ' fetchMarkets got an unrecognized response');
        }
        $result = array();
        for ($i = 0; $i < count($markets); $i++) {
            $market = $markets[$i];
            $id = $market['symbol'];
            $baseId = $market['base_coin'];
            $quoteId = $market['count_coin'];
            $base = $this->safe_currency_code($baseId);
            $quote = $this->safe_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
            $precision = array(
                'amount' => $this->safe_integer($market, 'amount_precision'),
                'price' => $this->safe_integer($market, 'price_precision'),
            );
            $amountLimits = array(
                'min' => pow(10, -$market['amount_precision']),
                'max' => null,
            );
            $priceLimits = array(
                'min' => pow(10, -$market['price_precision']),
                'max' => null,
            );
            $defaultCost = $amountLimits['min'] * $priceLimits['min'];
            $minCost = $this->safe_float($this->options['limits']['cost']['min'], $quote, $defaultCost);
            $costLimits = array(
                'min' => $minCost,
                'max' => null,
            );
            $limits = array(
                'amount' => $amountLimits,
                'price' => $priceLimits,
                'cost' => $costLimits,
            );
            $active = true;
            $result[] = array(
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'info' => $market,
                'active' => $active,
                'precision' => $precision,
                'limits' => $limits,
            );
        }
        return $result;
    }

    public function fetch_balance($params = array ()) {
        $this->load_markets();
        $request = array(
            'api_key' => $this->apiKey,
            'time' => $this->milliseconds(),
        );
        $response = $this->privateGetUserAccount (array_merge($request, $params));
        $respData = $this->safe_value($response, 'data');
        $result = array( 'info' => $respData );
        $coins = $this->safe_value($respData, 'coin_list');
        for ($i = 0; $i < count($coins); $i++) {
            $coin = $coins[$i];
            $currencyId = $this->safe_value($coin, 'coin');
            $code = $this->safe_currency_code($currencyId);
            $account = $this->account();
            $account['free'] = $this->safe_float($coin, 'normal');
            $account['used'] = $this->safe_float($coin, 'locked');
            $result[$code] = $account;
        }
        return $this->parse_balance($result);
    }

    public function fetch_order_book($symbol, $limit = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            'type' => 'step0',
            'symbol' => $this->market_id($symbol),
        );
        $response = $this->publicGetMarketDept (array_merge($request, $params));
        $data = $this->safe_value($response, 'data');
        $orderbook = $this->safe_value($data, 'tick');
        return $this->parse_order_book($orderbook);
    }

    public function parse_ohlcv($ohlcv, $market = null, $timeframe = '1m', $since = null, $limit = null) {
        // they return array( Timestamp, Volume, Close, High, Low, Open )
        return [
            intval ($ohlcv[0]),   // t
            floatval ($ohlcv[1]), // o
            floatval ($ohlcv[2]), // c
            floatval ($ohlcv[3]), // h
            floatval ($ohlcv[4]), // l
            floatval ($ohlcv[5]), // v
        ];
    }

    public function fetch_ohlcv($symbol, $timeframe = '1m', $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $periodDurationInSeconds = $this->parse_timeframe($timeframe);
        $request = array(
            'symbol' => $this->market_id($symbol),
            'period' => $periodDurationInSeconds / 60,  // in minute
        );
        // max $limit = 1001
        // $since & $limit not supported
        $response = $this->publicGetGetRecords (array_merge($request, $params));
        //        ordering => Ts, O, C, H, L, V
        //     {
        //         "code" => 200,
        //         "$data" => array(
        //             array( "TS", "o", "c", "h", "l", "v" ),
        //         )
        //     }
        //
        $data = $this->safe_value($response, 'data', array());
        return $this->parse_ohlcvs($data, $market, $timeframe, $since, $limit);
    }

    public function parse_ticker($ticker, $market = null) {
        $timestamp = $this->milliseconds();
        $symbol = null;
        if ($market) {
            $symbol = $market['symbol'];
        }
        $last = $this->safe_float($ticker, 'last');
        $percentage = $this->safe_float($ticker, 'rose');
        $open = $this->safe_float($ticker, 'open');
        $change = null;
        $average = null;
        if (($last !== null) && ($percentage !== null)) {
            $change = $last - $open;
            $average = $this->sum($last, $open) / 2;
        }
        return array(
            'symbol' => $symbol,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'high' => $this->safe_float($ticker, 'high'),
            'low' => $this->safe_float($ticker, 'low'),
            'bid' => $this->safe_float($ticker, 'buy'),
            'bidVolume' => null,
            'ask' => $this->safe_float($ticker, 'sell'),
            'askVolume' => null,
            'vwap' => null,
            'open' => $open,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => $change,
            'percentage' => $percentage,
            'average' => $average,
            'baseVolume' => $this->safe_float($ticker, 'vol'),
            'quoteVolume' => null,
            'info' => $ticker,
        );
    }

    public function fetch_ticker($symbol, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $ticker = $this->publicGetGetTicker (array_merge(array(
            'symbol' => $this->market_id($symbol),
        ), $params));
        return $this->parse_ticker($ticker, $market);
    }

    public function parse_trade($trade, $market = null) {
        // API doc says 'ts', but in fact it is 'ctime'
        $timestamp = $this->safe_timestamp($trade, 'ctime') / 1000;
        // take either of orderid or orderId
        $price = $this->safe_float($trade, 'price');
        $amount = $this->safe_float($trade, 'amount');
        $type = $this->safe_string($trade, 'type');
        $cost = null;
        if ($price !== null) {
            if ($amount !== null) {
                $cost = $price * $amount;
            }
        }
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        return array(
            'id' => null,
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601($timestamp),
            'symbol' => $symbol,
            'order' => null,
            'type' => null,
            'side' => $type === '1' ? 'buy' : 'sell',
            'takerOrMaker' => null,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'fee' => null,
        );
    }

    public function fetch_trades($symbol, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'symbol' => $this->market_id($symbol),
        );
        $response = $this->publicGetGetTrades (array_merge($request, $params));
        $data = $this->safe_value($response, 'data');
        if (!$data) {
            throw new ExchangeError($this->id . ' fetchTrades got an unrecognized response');
        }
        return $this->parse_trades($data, $market, $since, $limit);
    }

    public function fetch_orders($symbol = null, $since = null, $limit = null, $params = array ()) {
        $request = array(
            'api_key' => $this->apiKey,
            'time' => $this->milliseconds(),
        );
        $response = $this->privateGetCurrentOrders (array_merge($request, $params));
        return $this->parse_orders($response['data'], null, $since, $limit);
    }

    public function fetch_order($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            'order_id' => $id,
            'symbol' => $this->market_id($symbol),
            'api_key' => $this->apiKey,
            'time' => $this->milliseconds(),
        );
        $response = $this->privateGetOrderInfo (array_merge($request, $params));
        return $this->parse_order($response['data']['order_info']);
    }

    public function parse_order_side($side) {
        $sides = array(
            '1' => 'buy',
            '2' => 'sell',
            'BUY' => 'buy',
            'SELL' => 'sell',
        );
        return $this->safe_string($sides, $side, $side);
    }

    public function parse_order_status($status) {
        $statuses = array(
            '0' => 'open',
            '1' => 'open',
            '2' => 'closed',
            '3' => 'open', // partial closed
            '4' => 'canceled', // partial closed
            '5' => 'canceled', // partial canceled
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order($order, $market = null) {
        // Different API endpoints returns $order info in different format...
        // with different fields $filled->
        $id = $this->safe_string($order, 'id');
        if ($id === null) {
            $id = $this->safe_string($order, 'order_id');
        }
        $symbol = null;
        $marketId = null;
        if ((is_array($order) && array_key_exists('baseCoin', $order)) && (is_array($order) && array_key_exists('countCoin', $order))) {
            $marketId = $this->safe_string_lower($order, 'baseCoin') . $this->safe_string_lower($order, 'countCoin');
            if (is_array($this->markets_by_id) && array_key_exists($marketId, $this->markets_by_id)) {
                $market = $this->markets_by_id[$marketId];
            }
            if ($market !== null) {
                $symbol = $market['symbol'];
            }
        }
        if (is_array($order) && array_key_exists('symbol', $order)) {
            $symbol = $this->safe_string($order, 'symbol');
        }
        $timestamp = null;
        $datetime = null;
        if (is_array($order) && array_key_exists('created_at', $order)) {
            $timestamp = $this->safe_timestamp($order, 'created_at') / 1000;
            $datetime = $this->iso8601($timestamp);
        }
        $status = $this->parse_order_status($this->safe_string($order, 'status'));
        $side = $this->parse_order_side($this->safe_string($order, 'type'));
        $price = $this->safe_float($order, 'price');
        $amount = $this->safe_float($order, 'volume');
        $filled = $this->safe_float($order, 'deal_volume');
        $average = $this->safe_float($order, 'avg_price');
        $remaining = $this->safe_float($order, 'remain_volume');
        return array(
            'id' => $id,
            'datetime' => $datetime,
            'timestamp' => $timestamp,
            'status' => $status,
            'symbol' => $symbol,
            'type' => 'limit',
            'side' => $side,
            'price' => $price,
            'cost' => null,
            'amount' => $amount,
            'filled' => $filled,
            'remaining' => $remaining,
            'average' => $average,
            'trades' => null,
            'fee' => array(
                'cost' => null,
                'currency' => null,
                'rate' => null,
            ),
            'info' => $order,
        );
    }

    public function create_order($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        if ($type === 'market') {
            // https://github.com/code-biki/open-api#%E5%88%9B%E5%BB%BA%E8%AE%A2%E5%8D%95
            // their API for $market order is crap, not supporting $market orders for now
            throw new ExchangeError($this->id . ' allows limit orders only');
        }
        $this->load_markets();
        $market = $this->market($symbol);
        $request = array(
            'api_key' => $this->apiKey,
            'time' => $this->milliseconds(),
            'symbol' => $this->market_id($symbol),
            'price' => $price,
            'volume' => $amount,
            'side' => strtoupper($side),
            'type' => '1', // limit order
        );
        $response = $this->privatePostCreateOrder (array_merge($request, $params));
        return $this->parse_order(array_merge(array(
            'status' => 'open',
            'side' => $side,
            'amount' => $amount,
            'type' => $type,
            'symbol' => $symbol,
        ), $this->safe_value($response, 'data')), $market);
    }

    public function cancel_order($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' cancelOrder requires $symbol argument');
        }
        $this->load_markets();
        $request = array(
            'api_key' => $this->apiKey,
            'time' => $this->milliseconds(),
            'symbol' => $this->market_id($symbol),
            'order_id' => $id,
        );
        return $this->privatePostCancelOrder (array_merge($request, $params));
    }

    public function sign($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $url = $this->urls['api'][$api] . $this->implode_params($path, $params);
        $query = $this->omit($params, $this->extract_params($path));
        if ($api === 'public') {
            if ($query) {
                $url .= '?' . $this->urlencode($query);
            }
        } else {
            $this->check_required_credentials();
            $auth = $this->rawencode($this->keysort($query));
            $to_sign = str_replace('&', '', $auth->replace ('=', ''));
            $signature = $this->hash($this->encode($to_sign . $this->secret), 'md5');
            $suffix = 'sign=' . $signature;
            $url .= '?' . $auth . '&' . $suffix;
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function handle_errors($code, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if ($response === null) {
            return;
        }
        // use $response $code for error
        $errorCode = $this->safe_string($response, 'code');
        $message = $this->safe_string($response, 'msg', $body);
        if ($errorCode !== null && $errorCode !== '0') {
            $feedback = $this->safe_string($this->errorCodeNames, $errorCode, $message);
            // XXX => just throwing generic error when API call went wrong
            $this->throw_exactly_matched_exception($this->exceptions, '1', $feedback);
        }
    }
}
