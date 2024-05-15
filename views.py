import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from pandastable import Table

import config


class Root(tk.Tk):
    """
    Black and Scholes model GUI
    """

    def __init__(self):
        # main setup
        super().__init__()
        self.title(config.param["view"]["title"])
        self.iconbitmap(config.param["view"]["logo"])
        self.geometry("525x505")
        self.minsize(525, 505)

        # widgets
        self.minor_frame = Minor(self)
        self.major_frame = Major(self)


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.focus_force()  # put the focus on the new window
        self.title("BSM-Portfolio")
        self.iconbitmap(config.param["view"]["logo"])


class Minor(ttk.Frame):
    """
    Minor frame Class - For a chosen Option
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(relief="ridge")
        self.grid(row=0, column=0, sticky="nsew")

        # Option status
        self.lbl_val = None
        self.lbl_status = None

        # Widgets

        self.label_title = ttk.Label(self, text=config.param["view"]["minor_title"])
        self.label_title.grid(row=0, column=1, padx=5, pady=25, columnspan=2)

        self.lbl_type = ttk.Label(self, text="Type")
        self.lbl_type.grid(row=1, column=0, padx=1, pady=1)
        self.ent_type = ttk.Entry(self, width=8)
        self.ent_type.grid(row=1, column=1, padx=1, pady=3)

        self.lbl_strike = ttk.Label(self, text="Strike")
        self.lbl_strike.grid(row=2, column=0, padx=1, pady=1)
        self.ent_strike = ttk.Entry(self, width=8)
        self.ent_strike.grid(row=2, column=1, padx=1, pady=3)

        self.lbl_spot = ttk.Label(self, text="Spot:")
        self.lbl_spot.grid(row=3, column=0, padx=1, pady=1)
        self.ent_spot = ttk.Entry(self, width=8)
        self.ent_spot.grid(row=3, column=1, padx=1, pady=3)

        self.lbl_maturity = ttk.Label(self, text="maturity date:")
        self.lbl_maturity.grid(row=4, column=0, padx=1, pady=1)
        self.ent_maturity = ttk.Entry(self, width=10)
        self.ent_maturity.grid(row=4, column=1, padx=1, pady=3)

        self.lbl_vol = ttk.Label(self, text="volatility:")
        self.lbl_vol.grid(row=5, column=0, padx=1, pady=1)
        self.ent_vol = ttk.Entry(self, width=8)
        self.ent_vol.grid(row=5, column=1, padx=1, pady=3)

        self.lbl = ttk.Label(self, text="Optional (in %)")
        self.lbl.grid(row=6, column=0, columnspan=2, pady=18)

        self.lbl_rf = ttk.Label(self, text="risk free rate:")
        self.lbl_rf.grid(row=7, column=0, padx=1, pady=1)
        self.ent_rf = ttk.Entry(self, width=8)
        self.ent_rf.grid(row=7, column=1, padx=1, pady=3)

        self.lbl_div = ttk.Label(self, text="dividend yield:")
        self.lbl_div.grid(row=8, column=0, padx=2, pady=1)
        self.ent_div = ttk.Entry(self, width=8)
        self.ent_div.grid(row=8, column=1, padx=1, pady=3)

        self.btn_compute = ttk.Button(self, text="Compute")
        self.btn_compute.grid(row=9, column=0, columnspan=2, padx=7, pady=22)

        self.label_result = ttk.Label(self, text="Result:")
        self.label_result.grid(row=10, column=0, columnspan=2)

        self.label_price = ttk.Label(self, text="Price:")
        self.label_price.grid(row=12, column=0)
        self.ent_price = ttk.Entry(self, width=8)
        self.ent_price.grid(row=12, column=1, pady=2)

        self.label_delta = ttk.Label(self, text="Delta:")
        self.label_delta.grid(row=11, column=2)
        self.ent_delta = ttk.Entry(self, width=8)
        self.ent_delta.grid(row=11, column=3, pady=2)

        self.label_gamma = ttk.Label(self, text="Gamma:")
        self.label_gamma.grid(row=12, column=2)
        self.ent_gamma = ttk.Entry(self, width=8)
        self.ent_gamma.grid(row=12, column=3, pady=2)

        self.label_vega = ttk.Label(self, text="Vega:")
        self.label_vega.grid(row=13, column=2)
        self.ent_vega = ttk.Entry(self, width=8)
        self.ent_vega.grid(row=13, column=3, pady=2)

        self.label_theta = ttk.Label(self, text="Theta:")
        self.label_theta.grid(row=14, column=2)
        self.ent_theta = ttk.Entry(self, width=8)
        self.ent_theta.grid(row=14, column=3, pady=2)

        self.var1 = tk.BooleanVar()
        self.chk_ticker_ent = ttk.Entry(self, width=7)
        self.chk_ticker_ent.grid(row=3, column=3)
        self.chk_ticker_lbl = ttk.Label(self, text="Ticker:")
        self.chk_ticker_lbl.grid(row=3, column=2)
        self.chk_ticker = ttk.Checkbutton(
            self, text="Download spot", variable=self.var1, onvalue=True, offvalue=False
        )
        self.chk_ticker.grid(row=2, column=2, columnspan=2, padx=40, sticky="nsew")

    @staticmethod
    def error_msg(text: str):
        messagebox.showerror("showerror", str(text))

    def update_status(self, status: str, value):
        self.lbl_status = ttk.Label(
            self, text=status, foreground=("red" if len(status) > 12 else "green")
        )
        self.lbl_val = ttk.Label(
            self,
            text=f"Intrinsic value: {value}",
            foreground=(
                config.param["view"]["foreground_2"]
                if len(status) > 12
                else config.param["view"]["foreground_1"]
            ),
        )
        self.lbl_status.grid(row=5, column=2, columnspan=2, pady=2)
        self.lbl_val.grid(row=4, column=2, columnspan=2, pady=2)


class Major(ttk.Frame):
    """
    Manage Main frame - Random Portfolio
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(relief="ridge")
        self.grid(row=0, column=1, sticky="nsew")

        # Widgets
        self.lbl_title = ttk.Label(self, text=config.param["view"]["major_title"])
        self.lbl_title.grid(row=0, column=1, padx=5, pady=25, columnspan=3)

        self.btn_run = ttk.Button(self, text="Run")
        self.btn_run.grid(row=5, column=1, columnspan=2, padx=7, pady=22)

        self.var2 = tk.BooleanVar()
        self.chk_report = ttk.Checkbutton(
            self,
            text="Export to Excel",
            variable=self.var2,
            onvalue=True,
            offvalue=False,
        )
        self.chk_report.grid(
            row=6, column=1, columnspan=2, padx=7, pady=20, sticky="nsew"
        )

        self.btn_chart = ttk.Button(self, text="Generate Options' chart")
        self.btn_chart.grid(row=7, column=1, columnspan=2, padx=7, pady=20)

    @staticmethod
    def info_msg(msg: str):
        messagebox.showinfo("Info", msg)

    @staticmethod
    def option_chart(model):
        with PdfPages(config.param["chart"]["pdf"]) as pdf:
            with plt.style.context(config.param["chart"]["style"]):
                spot = np.arange(1, 150)

                # Greek plot

                fig, axes = plt.subplots(5, 1, figsize=(10, 25))
                fig.suptitle("Greeks", ha="center", fontweight="bold", fontsize=15)
                fig.tight_layout(pad=7.0)
                strike = [63, 87, 124]

                for s in strike:
                    del_call = [
                        model(float(s), float(x), 5.0, 0.1).delta("CALL") for x in spot
                    ]
                    del_put = [
                        model(float(s), float(x), 5.0, 0.1).delta("PUT") for x in spot
                    ]
                    axes[0].plot(
                        del_call, linestyle="--", label=("Delta Call K=%s" % s)
                    )
                    axes[0].plot(del_put, label=("Delta Put K=%s" % s))

                axes[0].set_ylabel("Delta")
                axes[0].legend()

                for s in strike:
                    gam = [model(float(s), float(x), 5.0, 0.1).gamma() for x in spot]
                    axes[1].plot(gam, linestyle="--", label=("Options Gamma K=%s" % s))

                axes[1].set_ylabel("Gamma")
                axes[1].legend()

                for s in strike:
                    veg = [model(float(s), float(x), 5.0, 0.1).vega() for x in spot]
                    axes[2].plot(veg, label=("Options Vega K=%s" % s))

                axes[2].set_ylabel("Vega")
                axes[2].set_title("Volatility = 0.1 ")
                axes[2].legend()

                for s in strike:
                    theta_call = [
                        model(float(s), float(x), 5.0, 0.1).theta("CALL") for x in spot
                    ]
                    theta_put = [
                        model(float(s), float(x), 5.0, 0.1).theta("PUT") for x in spot
                    ]
                    axes[3].plot(
                        theta_call, linestyle="--", label=("Theta Call K=%s" % s)
                    )
                    axes[3].plot(theta_put, label=("Theta Put K=%s" % s))

                axes[3].set_ylabel("Theta")
                axes[3].set_title("Maturity = 5 years")
                axes[3].legend()

                # Option plot

                call_val = [model(87.0, float(x), 1.0, 0.5).bsm("CALL") for x in spot]
                put_val = [model(87.0, float(x), 1.0, 0.5).bsm("PUT") for x in spot]

                axes[4].set_title(
                    f"Change in option value with stock price"
                    f"\n \n Strike: 87, t: 1 an, sigma: 0.5, r: 5%, q: 4%",
                    fontweight="bold",
                )
                axes[4].set_xlabel("Stock Price")
                axes[4].set_ylabel("Option price")
                axes[4].plot(
                    spot,
                    call_val,
                    color=config.param["chart"]["call_color"],
                    label="Call",
                )
                axes[4].plot(
                    spot, put_val, color=config.param["chart"]["put_color"], label="Put"
                )
                axes[4].legend()

            pdf.savefig()
            plt.close()

    def manage_pdtable(self, data: pd.DataFrame):
        """
        Create a new window and display data in an Excel way , plot are feasible by using the plot button on the new
        interface

        Parameters
        ----------
        data : Dataframe the need to be displayed in the new window
        -------
        """
        window = Window(self)

        frame = tk.Frame(master=window)
        frame.pack(fill="both", expand=True)

        pt = Table(frame, showtoolbar=True, showstatusbar=True)
        pt.show()

        pt.model.df = data
