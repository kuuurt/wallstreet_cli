import os
import argparse
# import json

from wallstreet import Stock
from wallstreet_cli import xetra
from forex_python.converter import CurrencyRates

LOCAL_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "db.txt")


def _currency_conversion(source_v: float, source_currency: str, target_currency: str):
    """Convert source currency to target currency
    Args:
        source_v (float):
        source_currency (str): designation of source currency
        target_currency (str): [description]
    """
    c = CurrencyRates()
    return c.convert(source_currency, target_currency, source_v)


def _get_stock_price(stock_name: str):

    try:
        return xetra.pipeline([stock_name])
    except IndexError:
        print("Ticker not found!")
        return None
    # TODO (easy): handle other exceptions. try using "APPL" as arguement for --stock,
    # unknown error occured

def _get_all_fav_stock_prices(show_command):
    xetra.pipeline(_get_fav_tickers(), show_command)
    # for stock in _get_fav_tickers():
    #     xetra.get_stock_from_dataset(stock, csv_list)
        # show_stock(stock)

def _find_ticker(company_name):
    """give the company_name, finds the ticker name"""
    # TODO (harder) having a function to search for tickers by just giving a company name
    # probably need to make an api request to some search engine
    pass


def show_stock(stock_name: str):
    """show stock price of certain stock
    Args:
        stock_name (str): [description]
    """
    # TODO (easy): take currency as arguement and show stock prices in different currencies
    price_in_usd = _get_stock_price(stock_name)
    if not price_in_usd:
        return
    price_in_eur = _currency_conversion(price_in_usd, "USD", "EUR")

    print(f"{stock_name}: {round(price_in_eur, 2)} EUR")


def _append_fav_ticker(l_of_tickers: list, db_path: str=LOCAL_DB_PATH):
    """append a list of tickers to a json file
    Args:
        l_of_tickers (list): list of tickers to add to favorites
        db_path (str, optional): path to store the fav file. Defaults to LOCAL_DB_PATH.
    """
    # create the folder if not yet initialized
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # read the json file from local path
    # update the list
    l_of_tickers = l_of_tickers + _get_fav_tickers()
    file = open(db_path, "w")
    file.write("{}".format(l_of_tickers))
    file.close()

def _get_fav_tickers(db_path: str=LOCAL_DB_PATH):
    """read from the local json file, get all fav tickers
    Returns a list of strings
    """
    # return list of tickers from file
    if not os.path.exists(db_path):
        return []
    file = open(db_path, "r")
    content = file.read()
    file.close()
    output = content.strip("][").replace("'", "").split(", ")
    return output

def main():
    ## TODO clean tmp files

    parser = argparse.ArgumentParser(description="cli for wallstreet")

    parser.add_argument("--stock", help="show stock price of ticker")

    parser.add_argument("--currency", default="EUR", help="currency")
    parser.add_argument("-s", default=False, action="store_true")
    parser.add_argument("--add_fav", default=None, help="show stock price of ticker")
    parser.add_argument("--show_fav", default=False, action="store_true")
    args = parser.parse_args()

    if args.stock:
        show_stock(args.stock)
    elif args.show_fav:
        _get_all_fav_stock_prices(args.s)
    elif args.add_fav:
        _append_fav_ticker(args.add_fav.split(","))

if __name__ == "__main__":
    main()
