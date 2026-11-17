import yfinance as yf
import numpy as np
import time
from scipy.optimize import minimize

assets = ["AAPL", "XOM", "JPM", "TLT", "GLD"]
rfr = 0.0512  # Risk-free rate (5.12% annualized)
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
	sharpe_ratio = (expected_return - rfr) / risk if risk != 0 else 0
	print(f'{asset} ssp ex. returns: {expected_return * 100:.2f}% anual - risk: {risk * 100:.2f}% - Sharpe Ratio: {sharpe_ratio:.2f}')

print(f'Single stock portfolios: {len(assets)}')

returns_ssp = np.dot(ssp_weights, expected_returns)

# Montecarlo simulation for random portfolios

resolution = 100
n = resolution**(len(assets)-1)
batch_size = n//100
batches = n // batch_size

# Generate n random portfolios

print(f'Generating {n} random portfolios...')

best_sharpe_ratio = -np.inf
best_portfolio = None
best_expected_return = None
best_risk = None

start_time = time.time()

for i in range(batches):
	weights_mc = np.random.dirichlet(np.ones(len(assets)), size=batch_size)
	returns_mc = np.dot(weights_mc, returns_ssp)
	variances_mc = np.einsum('ij,jk,ik->i', weights_mc, cov_matrix, weights_mc)
	volatilities_mc = np.sqrt(variances_mc)
	sharpe_ratios_mc = (returns_mc - rfr) / volatilities_mc

	max_index = np.argmax(sharpe_ratios_mc) # Index of winner of batch
	max_sharpe_ratio = sharpe_ratios_mc[max_index] 
	max_weights = weights_mc[max_index]
	max_expected_return = returns_mc[max_index]
	max_risk = volatilities_mc[max_index]
	
	if max_sharpe_ratio > best_sharpe_ratio:
		best_sharpe_ratio = max_sharpe_ratio
		best_portfolio = max_weights
		best_expected_return = max_expected_return
		best_risk = max_risk

	print(f'Batch {i+1}/{batches} completed. Best Sharpe Ratio so far: {best_sharpe_ratio:.4f}')

end_time = time.time()

# Results	

print(f'\nBest portfolio found:')
print(f'Expected return: {best_expected_return * 100:.2f}% anual')
print(f'Risk (volatility): {best_risk * 100:.2f}%')
print(f'Sharpe Ratio: {best_sharpe_ratio:.2f}')
print('\nBest portfolio weights:')

for asset, weight in zip(assets, best_portfolio):
	print(f'{asset}: {weight * 100:.2f}%')
print(f'Time taken: {end_time - start_time:.2f} seconds')

# Gradient ascent method

# Objective function

def negative_sharpe_ratio(weights, expected_returns, cov_matrix, rfr):
	portfolio_return = np.dot(weights, expected_returns)
	portfolio_variance = weights.T @ cov_matrix @ weights
	portfolio_risk = np.sqrt(portfolio_variance)
	return -(portfolio_return - rfr) / portfolio_risk  # Negative for minimization

# Restrictions: weights must sum to 1 and be non-negative

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

start_time = time.time()

# lower bounds for weights (no short selling)
bounds = tuple((0, 1) for _ in range(len(assets)))

# Initial guess for weights (equal distribution)

initial_weights = np.array([1/len(assets)] * len(assets))

print('\nOptimizing portfolio using gradient ascent method...')

result = minimize(negative_sharpe_ratio, initial_weights, args=(expected_returns, cov_matrix, rfr), method='SLSQP', bounds=bounds, constraints=constraints)

end_time = time.time()

# Results

weights_optimal = result.x
returns_optimal = np.dot(weights_optimal, expected_returns)
variance_optimal = weights_optimal.T @ cov_matrix @ weights_optimal
risk_optimal = np.sqrt(variance_optimal)
sharpe_ratio_optimal = (returns_optimal - rfr) / risk_optimal

print(f'\nOptimal portfolio found using gradient ascent method:')
print(f'Expected return: {returns_optimal * 100:.2f}% anual')
print(f'Risk (volatility): {risk_optimal * 100:.2f}%')
print(f'Sharpe Ratio: {sharpe_ratio_optimal:.2f}')

print('\nOptimal portfolio weights:')
for asset, weight in zip(assets, weights_optimal):
	print(f'{asset}: {weight * 100:.2f}%')

print(f'Time taken for optimization: {result.nit} iterations, {result.nfev} function evaluations, {end_time - start_time:.2f} seconds')