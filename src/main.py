import pandas as pd
from backtest import Backtest

df = pd.read_csv("../data/GOOGL.csv", index_col="Date", parse_dates=True)
bt = Backtest(df)
bt.run()
