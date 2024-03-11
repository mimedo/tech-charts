import yfinance as yf
import mplfinance as mpf

ticker = 'AAPL'
data = yf.download(ticker, start='2023-12-25', end='2024-03-10', interval='1d')

kwargs = dict(
    type='candle',
    style='yahoo',
    xrotation=90,
    ylabel='Aktienpreis',
    xlabel='Zeitraum',
    figscale=1,
    xlim=('2024-01-10', '2024-03-10'),
    datetime_format='%b %d'
)

mpf.plot(data, **kwargs, mav=9)
