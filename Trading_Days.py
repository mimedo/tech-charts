import pandas as pd
from pandas_market_calendars import get_calendar

nasdaq_calendar = get_calendar('NASDAQ')

start_date = pd.Timestamp('2019-01-01')
end_date = pd.Timestamp('2024-04-09')

trading_days = nasdaq_calendar.schedule(start_date=start_date, end_date=end_date)

num_trading_days = len(trading_days)

print("Number of trading days between", start_date.date(), "and", end_date.date(), ":", num_trading_days)