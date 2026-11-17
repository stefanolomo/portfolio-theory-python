import yfinance as yf
import numpy as np

assets = ["AAPL", "XOM", "JPM", "TLT", "GLD"]
# Apple, Exxon Mobile, JP Morgan, ETF USA Treasury Bonds, ETF Gold

# Download data
print('Downloading data...')
raw_data = yf.download(assets, start='2010-01-01', end='2026-01-01')
prices = raw_data['Close']
prices = prices.dropna()

returns = prices.pct_change()
returns = returns.dropna()

# Covariance matrix

cov_matrix = returns.cov() * 252

# Single stock portfolios (ssp) (anti hipotesis)

expected_returns = returns.mean() * 252 # 252 operating days in a year

ssp_weights = np.eye(len(assets))

for i in range(len(assets)):
	weight = ssp_weights[i]
	asset = assets[i]
	expected_return = np.dot(weight, expected_returns)
	variance = weight.T @ cov_matrix @ weight
	risk = np.sqrt(variance)
	sharpe_ratio = (expected_return - 0.0512 / risk) if risk != 0 else 0
	print(f'{asset} ssp ex. returns: {expected_return * 100:.2f}% anual - risk: {risk * 100:.2f}% - Sharpe Ratio: {sharpe_ratio:.2f}')

print(f'Single stock portfolios: {len(assets)}')
