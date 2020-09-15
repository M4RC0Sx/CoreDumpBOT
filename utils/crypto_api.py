from pycoingecko import CoinGeckoAPI


def get_crypto_prices():

    return CoinGeckoAPI().get_price(ids='bitcoin,litecoin,ethereum', vs_currencies='usd,eur')
