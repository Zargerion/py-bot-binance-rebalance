from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

api = "RSFAr6KdylB47hPMjdWcW2j41DftwDY61cd1JmJSAQ6S8Aq4lXskcf8DOXtlmmRY"
secret = "BqqBzo3DpkQYZ5awmkm5VY1HXp3oqXuCgTdYwn3e2e7j6Pqnx7C5PVvLnWt1ZtrS"

client = Client(api, secret)

import time

btc = 0.02
eth = 0.3

def buy_or_sell_funk(buy, sell, eth):

    value_to_sell_or_buy = 0.0
    if buy > sell:
        value_to_sell_or_buy = buy
    if buy < sell:
        value_to_sell_or_buy = sell
    else:
        return value_to_sell_or_buy, "wait" 

    if eth < 49.5:
        return value_to_sell_or_buy, "buy" 
    if eth > 50.5:
        return value_to_sell_or_buy, "sell"
    else:
        return value_to_sell_or_buy, "wait" 

def rebalance_funk(d_btc, d_eth, signal):
    global btc
    global eth
    if signal == "buy":
        btc = round(btc - d_btc, 8)
        eth = round(eth + d_eth, 4)
    if signal == "sell":
        btc = round(btc + d_btc, 8)
        eth = round(eth - d_eth, 4)
    else:
        return

import time

while True:
    
    spot_eth_usdt = client.get_ticker(symbol='ETHUSDT')
    spot_eth_usdt['lastPrice']
    spot_btc_usdt = client.get_ticker(symbol='BTCUSDT')
    spot_btc_usdt['lastPrice'] 
    
    #old_spot_btc_usdt = spot_btc_usdt['lastPrice']
    #old_spot_eth_usdt = spot_eth_usdt['lastPrice']

    btc_usd = round(btc * float(spot_btc_usdt['lastPrice']), 2)
    eth_usd = round(eth * float(spot_eth_usdt['lastPrice']), 2)

    all_value_percernt_btc = btc_usd / ((btc_usd + eth_usd) / 100)
    all_value_percernt_eth = eth_usd / ((btc_usd + eth_usd) / 100)
    print('Проценты бтк и ефира:', all_value_percernt_btc, all_value_percernt_eth)

    how_much_buy_eth = round((eth / all_value_percernt_btc) * (all_value_percernt_btc - 50), 4)
    how_much_sell_eth = round((eth / all_value_percernt_eth) * (all_value_percernt_eth - 50), 4)
    print('Как много купить эфира:', how_much_buy_eth)
    print('Как много продать эфира:', how_much_sell_eth)

    value_bs, buy_or_sell = buy_or_sell_funk(round(how_much_buy_eth, 4), round(how_much_sell_eth, 4), all_value_percernt_eth)
    print('Купить или продать ETH:', value_bs, buy_or_sell)

    spot_eth_btc = float(client.get_ticker(symbol='ETHBTC')['lastPrice'])
    eth_to_btc = round(value_bs * spot_eth_btc, 8)
    print('Купить или продать BTC:', eth_to_btc)

    print('BTC и ETH:', btc, eth)
    rebalance_funk(eth_to_btc, value_bs, buy_or_sell)
    print('BTC и ETH:', btc, eth)

    time.sleep(10)


