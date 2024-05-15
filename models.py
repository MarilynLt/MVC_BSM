import logging
from random import randrange

import bs4 as bs
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from scipy.stats import norm

import config

logger = logging.getLogger(__name__)


class Options:
    """
    Valuation of options in Black-Scholes-Merton Model (include dividend)
    Attributes
    ==========
    strike: strike price
    spot: initial stock/index level
    t: time to maturity (in year fractions)
    r: constant risk-free short rate, assume flat term structure
    q: yield of the dividend
    sigma: volatility factor in diffusion term

    """

    def __init__(
        self,
        strike: float,
        spot: float,
        t: float,
        sigma: float,
        r: float = config.param["model"]["rf"],
        q: float = config.param["model"]["div"],
    ):
        self.strike = strike
        self.spot = spot
        self.r = r
        self.q = q
        self.t = t
        self.sigma = sigma

        # private
        self._d1 = self.d1()
        self._d2 = self.d2()

    @staticmethod
    def n(x):
        return norm.cdf(x)

    def d1(self) -> float:
        return (
            np.log(self.spot / self.strike)
            + (self.r - self.q + 0.5 * self.sigma**2) * self.t
        ) / (self.sigma * np.sqrt(self.t))

    def d2(self) -> float:
        return -(self.sigma * np.sqrt(self.t)) + self._d1

    def bsm(self, option_type: str) -> float:
        """
        :param option_type: whether it is a Call or a Put
        :return: price of the put or call
        """
        try:
            if option_type == "CALL":
                call = self.spot * np.exp(-self.q * self.t) * self.n(
                    self._d1
                ) - self.strike * np.exp(-self.r * self.t) * self.n(self._d2)
                return call.round(3)
            elif option_type == "PUT":
                put = self.strike * np.exp(-self.r * self.t) * self.n(
                    -self._d2
                ) - self.spot * np.exp(-self.q * self.t) * self.n(-self._d1)
                return put.round(3)
        except Exception as e:
            print(
                f"{e} \n"
                f"Please enter the option type in string. It should be either Call or Put"
            )

    def delta(self, option_type: str) -> float:
        """
        Delta measures the change in the option price for a $1 change in the stock price (sensitivity)
        :param option_type: whether it is a Call or a Put
        :return: delta of the option
        """
        try:
            if option_type == "CALL":
                delta = np.exp(-self.q * self.t) * self.n(self._d1)
            elif option_type == "PUT":
                delta = np.exp(-self.q * self.t) * (self.n(self._d1) - 1)
            return delta.round(4)
        except Exception as e:
            print(
                f"{e} \n"
                f"Option type missing, please enter the option type. It should be a string"
            )

    def gamma(self) -> float:
        """
        Gamma measure the change on delta when the stock price change (convexity)
        :return: gama of the option
        """
        gamma = (
            np.exp(-self.q * self.t)
            * norm.pdf(self._d1)
            / self.spot
            * self.sigma
            * np.sqrt(self.t)
        )
        return gamma.round(4)

    def vega(self) -> float:
        """
        Vega measures the change in the option price per percentage point change in the volatility
        :return: vega of the option
        """
        vega = (
            self.spot
            * np.exp(-self.q * self.t)
            * np.sqrt(self.t)
            * norm.pdf(self._d1)
            / 100
        )
        return vega.round(4)

    def theta(self, option_type: str) -> float:
        """
        Vega measures the change in the option price per one calendar day (or 1/365 of a year)
        :return: theta of the option
        """
        try:
            if option_type == "CALL":
                theta = (
                    self.q * self.spot * np.exp(-self.q * self.t) * self.n(self._d1)
                    - self.r * self.strike * np.exp(-self.r * self.t) * self.n(self._d2)
                    - norm.pdf(self._d1)
                    * self.spot
                    * self.sigma
                    * np.exp(-self.q * self.t)
                    / 2
                    * np.sqrt(self.t)
                ) / 365
            elif option_type == "PUT":
                theta = (
                    self.r * self.strike * np.exp(-self.r * self.t) * self.n(-self._d2)
                    - self.q * self.spot * np.exp(-self.q * self.t) * self.n(-self._d1)
                    - norm.pdf(self._d1)
                    * self.spot
                    * self.sigma
                    * np.exp(-self.q * self.t)
                    / 2
                    * np.sqrt(self.t)
                ) / 365
            return theta.round(4)
        except Exception as e:
            print(
                f"{e} \n"
                f"Option type missing, please enter the option type. It should be a string"
            )

    def intrinsic_value(self, option_type: str) -> list:
        """
        Give an approximate intrinsic value of the option and the status based on the intrinsic value
        :param option_type: type of option
        :returns: intrinsic value and status
        """
        value = self.strike - self.spot
        if (option_type == "CALL" and value < 0) | (option_type == "PUT" and value > 0):
            status = "In the Money"
        elif value == 0:
            status = "At the Money"
        else:
            status = "Out of the Money"

        return [status, round(value, 2)]

    @staticmethod
    def retrieve_ticker() -> list:
        """
        get sp100 stock ticker from wikipedia
        :return: list of stocks ticker
        """

        # logger.log(level=logging.DEBUG)

        # get the ticker from wikipedia ETF S&P 100 page
        r = requests.get(config.param["model"]["link"])
        soup = bs.BeautifulSoup(r.text, "lxml")
        table = soup.find("table", {"class": "wikitable", "id": "constituents"})
        tickers = []

        for i in table.findAll("tr")[1:]:
            for x in i.findAll("td"):
                ticker = x.get_text()
                tickers.append(ticker)
                break

        tickers = [i.replace("\n", "") for i in tickers]

        # get the spot of each stocks from yahoo finance
        spots = (
            yf.download(tickers, interval="1m")["Adj Close"].iloc[-1, :]
        ).reset_index()
        while spots.isnull().sum().sum() >= 5:
            print(f"{spots.isnull().sum().sum()} missing values")
            spots = (yf.download(tickers)["Adj Close"].iloc[-1, :]).reset_index()
        stock_price = list(spots.dropna().itertuples(index=False, name=None))

        return stock_price

    @staticmethod
    def get_spot(ticker_list: list) -> float:
        """
        get spot price of a stocks list
        :param ticker_list: list of stock ticker
        :return: dataframe with stocks and spots
        """
        spot = yf.download(ticker_list)["Adj Close"].iloc[-1]
        return spot.round(2)

    @staticmethod
    def get_option(stock_price) -> pd.DataFrame:
        """
        Get the option characteristics from yahoo finance (s, k, t, sigma)
        :param stock_price: list of tuple with stock's ticker and price
        :return: dataframe with the options data
        """
        option_data = []
        for t, s in stock_price:
            try:
                maturity = yf.Ticker(str(t)).options
                exp = maturity[randrange(len(maturity))]
            except ValueError:
                continue

            for option_type in ["calls", "puts"]:
                opt = getattr(yf.Ticker(str(t)).option_chain(exp), option_type)
                for row in opt.itertuples():
                    type_op = "call" if option_type == "calls" else "put"
                    option_data.append(
                        {
                            "Ticker": t,
                            "Spot": s,
                            "Maturity": exp,
                            "Type": type_op,
                            "Contract Symbol": row.contractSymbol,
                            "Strike": row.strike,
                            "Volatility": row.impliedVolatility,
                            "Volume": row.volume,
                            "Currency": row.currency,
                        }
                    )
                    break

        return pd.DataFrame(option_data)

    @staticmethod
    def generate_excel(data: pd.DataFrame):
        data.to_excel(
            excel_writer=config.param["chart"]["file"],
            sheet_name=config.param["chart"]["sheet_name"],
            index=False,
        )
