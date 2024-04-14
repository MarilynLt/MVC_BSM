import tkinter as tk
from datetime import datetime


class MinorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind()

    def _bind(self):
        self.view.btn_compute.config(command=self.computation)
        self.view.chk_ticker.config(command=self.fetch_spot)

    def computation(self):
        """
        Compute the option price.
        Use Options class - function bsm
        Return: float
        -------
        """

        try:
            op_type = str(self.view.ent_type.get().upper())
            if op_type == "":
                self.view.error_msg("Please enter Option type")
            strike_price = float(self.view.ent_strike.get())
            spot_price = float(self.view.ent_spot.get())
            try:
                maturity = (
                    datetime.strptime(self.view.ent_maturity.get(), "%d/%m/%Y")
                    - datetime.now()
                ).days / 365
            except Exception as e:
                print(e.args)
                self.view.error_msg("The maturity should be in DD/MM/YYYY")
            volatility = float(self.view.ent_vol.get())
        except Exception as e:
            print(e.args)
            self.view.error_msg("Attribute missing, please check your input")

        try:
            rf = float(self.view.ent_rf.get()) / 100
            div = float(self.view.ent_div.get()) / 100
        except ValueError:
            rf = 0.05
            div = 0.04

        op = self.model(strike_price, spot_price, maturity, volatility, rf, div)
        price = op.bsm(op_type)
        delta = op.delta(op_type)
        gamma = op.gamma()
        vega = op.vega()
        theta = op.theta(op_type)
        status = op.intrinsic_value(op_type)[0]
        value = str(op.intrinsic_value(op_type)[1])

        self.view.ent_price.delete(0, tk.END)
        self.view.ent_price.insert(0, str(price))

        self.view.ent_delta.delete(0, tk.END)
        self.view.ent_delta.insert(0, str(delta))

        self.view.ent_gamma.delete(0, tk.END)
        self.view.ent_gamma.insert(0, str(gamma))

        self.view.ent_vega.delete(0, tk.END)
        self.view.ent_vega.insert(0, str(vega))

        self.view.ent_theta.delete(0, tk.END)
        self.view.ent_theta.insert(0, str(theta))

        # delete label if already printed
        try:
            self.view.lbl_status.grid_forget()
            self.view.lbl_val.grid_forget()
        except Exception as e:
            print(e.args)
            pass

        self.view.update_status(status, value)

    def fetch_spot(self):
        """
        Get stock price from yahoo finance
        Returns
        -------
        """

        # get spot if the box is checked
        if self.view.var1.get():
            try:
                option_ticker = str(self.view.chk_ticker_ent.get().upper())
                spot = self.model.get_spot(option_ticker)

                self.view.ent_spot.delete(0, tk.END)
                self.view.ent_spot.insert(0, str(spot))
            except Exception as e:
                print(e.args)
                self.view.error_msg("You are using an incorrect  TICKER, please check")
        else:
            self.view.chk_ticker_ent.delete(0, tk.END)
            self.view.ent_spot.delete(0, tk.END)


class MajorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind()

    def _bind(self):
        self.view.btn_run.config(command=self.run_bsm_ptf)
        self.view.btn_chart.config(command=self.chart)

    def run_bsm_ptf(self):
        """
        Lunch BSM model computation of option price, delta, gamma and vega
        Returns: dataframe with all options infos
        -------
        """
        stock_price = self.model.retrieve_ticker()  # retrieve the ticker and spot
        df = self.model.get_option(
            stock_price
        )  # retrieve option data from yahoo finance

        df["Price"] = 0
        df["Delta"] = 0
        df["Gamma"] = 0
        df["Vega"] = 0
        df["Theta"] = 0
        df["Status"] = 0

        # Computing Option price, delta, gamma and vega
        for i in range(len(df)):
            #  Instantiation of Options class
            op = self.model(
                strike=df["Strike"].loc[i],
                spot=df["Spot"].loc[i],
                sigma=df["Volatility"].loc[i],
                t=(
                    datetime.strptime(df["Maturity"].loc[i], "%Y-%m-%d")
                    - datetime.now()
                ).days
                / 365,
            )

            df["Status"].loc[i] = op.intrinsic_value(
                option_type=df["Type"].loc[i].upper()
            )[0]
            df["Price"].loc[i] = op.bsm(option_type=df["Type"].loc[i].upper())
            df["Delta"].loc[i] = op.delta(option_type=df["Type"].loc[i].upper())
            df["Theta"].loc[i] = op.theta(option_type=df["Type"].loc[i].upper())
            df["Gamma"].loc[i] = op.gamma()
            df["Vega"].loc[i] = op.vega()

        # generate an excel with the data
        if self.view.var2.get():
            self.model.generate_excel(data=df)
            self.view.info_msg("Excel generated")

        # generate second window with the dataframe
        self.view.manage_pdtable(data=df)

    def chart(self):
        self.view.option_chart(self.model)
        self.view.info_msg("Chart generated")


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model
        self.min_controller = MinorController(model, self.view.minor_frame)
        self.major_controller = MajorController(model, self.view.major_frame)

    def start(self):
        self.view.mainloop()
