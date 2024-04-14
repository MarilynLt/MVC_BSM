#University python project on the black and Scholes model with dividend included
This is a Black and Scholes Merton Pricer with a Tkinter interface and MVC model 

#used libraries (must be installed before runing the code) : 
-random
-numpy as np
-scipy.stats
-bs4
-pandas
-requests
-yfinance
-tkinter
-datetime
-pandastable

Structure : 4 files (models, view, controller, main)
-View : Class Root, Window, Major , Minor 
-Model: Class Options (all functions and attribute on the option class)
-Controller: Class Controller (intermediary between the views and models. The controller routes data between the views and models)
-Main

How to use the interface (2 Frame):
*Main frame, for launching the BSM model on a random option portfolio. Open a tkinter window with the portfolio and the result (price, delta, gamma, vega)
*Minor frame, allow to compute an option price based on BSM model (no Grecks in this one)
** maturity should be in following format: DD/MM/YYYY (for the pricer)