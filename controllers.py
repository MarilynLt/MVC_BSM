from datetime import datetime
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_value_view(self, widget, value):


    def computation(self, t, k, s, m, vol, rf, div):
        op_type = str(t)
        strike_price = float(k)
        spot_price = float(s)
        maturity = (datetime.strptime(m, '%d/%m/%Y') - datetime.now()).days / 365
        volatility = float(vol)

        try:
            rf = float(rf) / 100
            div = float(div) / 100
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



    def download(self):
        pass
