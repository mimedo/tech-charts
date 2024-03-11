import yfinance as yf
import pandas as pd
import mplfinance as mpf

stock_data = yf.download('AYX', start='2021-12-10', end='2024-03-17', interval='1wk')

delta = stock_data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
RS = gain / loss
stock_data['RSI'] = 100 - (100 / (1 + RS))

stock_data.reset_index(inplace=True)
stock_data['Date'] = pd.to_datetime(stock_data['Date'])
stock_data.set_index('Date', inplace=True)

ap = mpf.make_addplot(stock_data[['RSI']], panel=1, ylabel='RSI', color='lightblue', width=1.2)

kwargs = dict(
    type='line',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figsize=(10, 5.3),
    xlim=('2023-01-12', '2024-01-10'),
    datetime_format='%b %d',
    addplot=[ap],
    panel_ratios=(3, 3)
)

fig, axlist = mpf.plot(
    stock_data,
    **kwargs,
    returnfig=True
)

axStock = axlist[0]
axStock.plot(stock_data.index, stock_data['Close'], label='Kurslinie', color='#1f77b4')
# line = axStock.lines[0]
# line.set_color('#ff7f0e')

ax = axlist[2]
ax.plot(stock_data.index, stock_data['RSI'], label='RSI', color='lightblue')
ax_pos = ax.get_position()
ax.set_position([ax_pos.x0, ax_pos.y0 - 0.02, ax_pos.width, ax_pos.height])
ax.legend()
ax.axhline(70, linestyle='--', color='orange')
ax.axhline(30, linestyle='--', color='orange')
ax.set_yticks([0, 30, 70, 100])

for ax in axlist:
    ax.tick_params(axis='both', labelsize=11)
    ax.set_xlabel(ax.get_xlabel(), fontsize=11)
    ax.set_ylabel(ax.get_ylabel(), fontsize=11)
    ax.legend(fontsize=11)

mpf.show()
