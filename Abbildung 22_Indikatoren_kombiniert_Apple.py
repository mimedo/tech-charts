import yfinance as yf
import mplfinance as mpf
import pandas as pd

# Kursdaten von Yahoo-Finance importieren
data = yf.download('AAPL', start='2019-01-01', end='2024-04-09', interval='1d')

# MACD
data['EMA12'] = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
data['EMA26'] = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
data['MACD'] = data['EMA12'] - data['EMA26']
data['Signal Line'] = data['MACD'].ewm(span=9, min_periods=0, adjust=False).mean()

# RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
RS = gain / loss
data['RSI'] = 100 - (100 / (1 + RS))

data.reset_index(inplace=True)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

ap1 = mpf.make_addplot(data[['MACD']], panel=1, ylabel='MACD', color='#1f77b4', width=1.2, ylim=(-4.5, 1.5))
ap2 = mpf.make_addplot(data[['Signal Line']], panel=1, color='#ff7f0e', width=1.2, ylim=(-4.5, 1.5))
ap3 = mpf.make_addplot(data[['RSI']], panel=2, ylabel='RSI', color='lightblue')

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figsize=(10, 6.1),
    xlim=('2024-01-01', '2024-04-09'),
    ylim=(165, 198),
    datetime_format='%b %d',
    addplot=[ap1, ap2, ap3],
    panel_ratios=(4, 2),
    mav=50,
    ema=100
)

fig, axlist = mpf.plot(
    data,
    **kwargs,
    returnfig=True
)

axStock = axlist[0]
axStock.plot(data.index, data['Close'], label='SMA', color='#1f77b4')
axStock.plot(data.index, data['Close'], label='EMA', color='#ff7f0e')

axMacd = axlist[3]
axMacd.plot(data.index, data['MACD'], label='MACD', color='#1f77b4')
axMacd.plot(data.index, data['Signal Line'], label='Signallinie', color='#ff7f0e')
axMacd_pos = axMacd.get_position()
axMacd.set_position([axMacd_pos.x0, axMacd_pos.y0 - 0.02, axMacd_pos.width, axMacd_pos.height])

axRsi = axlist[4]
axRsi.plot(data.index, data['RSI'], label='RSI', color='lightblue')
axRsiPos = axRsi.get_position()
axRsi.set_position([axRsiPos.x0, axRsiPos.y0 - 0.04, axRsiPos.width, axRsiPos.height])
axRsi.axhline(70, linestyle='--', color='#ff7f0e')
axRsi.axhline(30, linestyle='--', color='#ff7f0e')
axRsi.set_yticks([0, 30, 70, 100])

for ax in axlist:
    ax.tick_params(axis='both', labelsize=11)
    ax.set_xlabel(ax.get_xlabel(), fontsize=11)
    ax.set_ylabel(ax.get_ylabel(), fontsize=11)
    ax.legend(fontsize=11)

axlist[2].get_legend().remove()
axlist[3].legend(loc='upper right')
axlist[4].legend(loc='upper right')

mpf.show()
