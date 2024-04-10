import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk


class App(tk.Tk):
    """
    Black and Scholes model GUI
    """

    def __init__(self):
        # main setup
        super().__init__()
        self.title("Black-Scholes-Merton pricer")
        self.iconbitmap('logo.ico')
        self.geometry("525x505")
        self.minsize(525, 505)

        # widgets
        self.minor_frame = Minor(self)
        self.main_frame = Major(self)


class Minor(ttk.Frame):
    """
    Minor frame Class - For a chosen Option
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(relief='ridge')
        self.grid(row=0, column=0, sticky="nsew")

        # controller
        self.controller = None

        # Widgets

        self.label_title = ttk.Label(self, text="BSM Model on selected option")
        self.label_title.grid(row=0, column=1, padx=5, pady=25, columnspan=2)

        self.lbl_type = ttk.Label(self, text="Type")
        self.lbl_type.grid(row=1, column=0, padx=1, pady=1)
        self.ent_type = ttk.Entry(self, width=8)
        self.ent_type.grid(row=1, column=1, padx=1, pady=3)

        self.lbl_strike = ttk.Label(self, text="Strike")
        self.lbl_strike.grid(row=2, column=0, padx=1, pady=1)
        self.ent_strike = ttk.Entry(self, width=8)
        self.ent_strike.grid(row=2, column=1, padx=1, pady=3)

        self.lbl_spot = ttk.Label(self, text='Spot:')
        self.lbl_spot.grid(row=3, column=0, padx=1, pady=1)
        self.ent_spot = ttk.Entry(self, width=8)
        self.ent_spot.grid(row=3, column=1, padx=1, pady=3)

        self.lbl_maturity = ttk.Label(self, text='maturity date:')
        self.lbl_maturity.grid(row=4, column=0, padx=1, pady=1)
        self.ent_maturity = ttk.Entry(self, width=10)
        self.ent_maturity.grid(row=4, column=1, padx=1, pady=3)

        self.lbl_vol = ttk.Label(self, text='volatility:')
        self.lbl_vol.grid(row=5, column=0, padx=1, pady=1)
        self.ent_vol = ttk.Entry(self, width=8)
        self.ent_vol.grid(row=5, column=1, padx=1, pady=3)

        self.lbl = ttk.Label(self, text='Optional (in %)')
        self.lbl.grid(row=6, column=0, columnspan=2, pady=18)

        self.lbl_rf = ttk.Label(self, text='risk free rate:')
        self.lbl_rf.grid(row=7, column=0, padx=1, pady=1)
        self.ent_rf = ttk.Entry(self, width=8)
        self.ent_rf.grid(row=7, column=1, padx=1, pady=3)

        self.lbl_div = ttk.Label(self, text='dividend yield:')
        self.lbl_div.grid(row=8, column=0, padx=2, pady=1)
        self.ent_div = ttk.Entry(self, width=8)
        self.ent_div.grid(row=8, column=1, padx=1, pady=3)

        self.btn_compute = ttk.Button(self, text='Compute')
        self.btn_compute.grid(row=9, column=0, columnspan=2, padx=7, pady=22)

        self.label_result = ttk.Label(self, text='Result:')
        self.label_result.grid(row=10, column=0, columnspan=2)

        self.label_price = ttk.Label(self, text='Price:')
        self.label_price.grid(row=12, column=0)
        self.ent_price = ttk.Entry(self, width=8)
        self.ent_price.grid(row=12, column=1, pady=2)

        self.label_delta = ttk.Label(self, text='Delta:')
        self.label_delta.grid(row=11, column=2)
        self.ent_delta = ttk.Entry(self, width=8)
        self.ent_delta.grid(row=11, column=3, pady=2)

        self.label_gamma = ttk.Label(self, text='Gamma:')
        self.label_gamma.grid(row=12, column=2)
        self.ent_gamma = ttk.Entry(self, width=8)
        self.ent_gamma.grid(row=12, column=3, pady=2)

        self.label_vega = ttk.Label(self, text='Vega:')
        self.label_vega.grid(row=13, column=2)
        self.ent_vega = ttk.Entry(self, width=8)
        self.ent_vega.grid(row=13, column=3, pady=2)

        self.label_theta = ttk.Label(self, text='Theta:')
        self.label_theta.grid(row=14, column=2)
        self.ent_theta = ttk.Entry(self, width=8)
        self.ent_theta.grid(row=14, column=3, pady=2)

        self.var1 = tk.IntVar()
        self.chk_ticker_ent = ttk.Entry(self, width=7)
        self.chk_ticker_ent.grid(row=3, column=3)
        self.chk_ticker_lbl = ttk.Label(self, text='Ticker:')
        self.chk_ticker_lbl.grid(row=3, column=2)
        self.chk_ticker = ttk.Checkbutton(self, text='Download spot', variable=self.var1,
                                          onvalue=1, offvalue=0)
        self.chk_ticker.grid(row=2, column=2, columnspan=2, padx=40, sticky="nsew")

        # Option status
        self.lbl_status = ttk.Label(self, text="")
        self.lbl_val = ttk.Label(self, text="")
        self.lbl_status.grid(row=5, column=2, columnspan=2, pady=2)
        self.lbl_val.grid(row=4, column=2, columnspan=2, pady=2)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    @staticmethod
    def error_msg(text: str):
        messagebox.showerror("showerror", str(text))

    # @staticmethod
    # def update_view(param, value):
    #     param.delete(0, tk.END)
    #     param.insert(0, str(value))

    def compute_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            self.controller.computation(self.ent_type.get().upper(), self.ent_strike.get(), self.ent_spot.get(),
                                        self.ent_maturity.get(), self.ent_vol.get(), self.ent_rf.get(),
                                        self.ent_div.get())

    def update_option(self, value):
        self.ent_price.delete(0, tk.END)
        self.ent_price.insert(0, str(value))

        self.ent_delta.delete(0, tk.END)
        self.ent_delta.insert(0, str(delta))

        self.ent_gamma.delete(0, tk.END)
        self.ent_gamma.insert(0, str(gamma))

        self.ent_vega.delete(0, tk.END)
        self.ent_vega.insert(0, str(vega))

        self.ent_theta.delete(0, tk.END)
        self.ent_theta.insert(0, str(theta))

    def download_box_checked(self):
        """
        Handle download click event
        :return:
        """
        if self.controller:
            self.controller.download()


class Major(ttk.Frame):
    """
    Manage Main frame - Random Portfolio
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(relief='ridge')
        self.grid(row=0, column=1, sticky="nsew")

        # controller
        self.controller = None

        # Widgets
        self.lbl_title = ttk.Label(self, text="BSM model on random Portfolio")
        self.lbl_title.grid(row=0, column=1, padx=5, pady=25, columnspan=3)

        self.btn_run = ttk.Button(self, text='Run')
        self.btn_run.grid(row=5, column=1, columnspan=2, padx=7, pady=22)

        self.var2 = tk.IntVar()
        self.chk_report = ttk.Checkbutton(self, text="Export to Excel", variable=self.var2,
                                          onvalue=1, offvalue=0)
        self.chk_report.grid(row=6, column=1, columnspan=2, padx=7, pady=20, sticky='nsew')

        self.btn_chart = ttk.Button(self, text="Generate Options' chart")
        self.btn_chart.grid(row=7, column=1, columnspan=2, padx=7, pady=20)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
