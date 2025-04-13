import pandas as pd
import os

def load_trade_data(days, folder_path="."):
    dfs = []
    for day in days:
        file_path = (folder_path + f"day_{day}.csv")
        df = pd.read_csv(file_path, sep=';')
        df["day"] = day
        df["global_timestamp"] = df["timestamp"] + day * 1000
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# Example usage:
days = [-1, 0, 1]  # Extend this list as needed
df = load_trade_data(days, folder_path="trades_round_2_")  # adjust path if needed
print(df.head())
import matplotlib.pyplot as plt


def plot_price_timeseries(df, symbol):
    symbol_df = df[df["symbol"] == symbol].sort_values("global_timestamp")
    plt.plot(symbol_df["global_timestamp"], symbol_df["price"], marker='o')
    plt.title(f"Price Over Time for {symbol}")
    plt.xlabel("Global Timestamp")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(f"{symbol}_price_timeseries.png")
    plt.clf()  # Clear the figure for the next plot



g = ['CROISSANTS', 'DJEMBES', 'JAMS', 'KELP', 'PICNIC_BASKET1', 'PICNIC_BASKET2', 'RAINFOREST_RESIN', 'SQUID_INK', 'CROISSANTS', 'JAMS']
for symbol in g:
    plot_price_timeseries(df, symbol)
    print(f"Price timeseries for {symbol} saved.")

def calculate_cross_correlation(df, symbols):
    correlations = {}
    for i, symbol1 in enumerate(symbols):
        for symbol2 in symbols[i+1:]:
            symbol1_df = df[df["symbol"] == symbol1].sort_values("global_timestamp")
            symbol2_df = df[df["symbol"] == symbol2].sort_values("global_timestamp")
            
            # Align timestamps
            merged_df = pd.merge(symbol1_df, symbol2_df, on="global_timestamp", suffixes=('_1', '_2'))
            
            if not merged_df.empty:
                correlation = merged_df["price_1"].corr(merged_df["price_2"])
                correlations[(symbol1, symbol2)] = correlation
            else:
                correlations[(symbol1, symbol2)] = None  # No overlapping timestamps

    return correlations

# Calculate cross-correlations
cross_correlations = calculate_cross_correlation(df, g)
for (symbol1, symbol2), correlation in cross_correlations.items():
    print(f"Cross-correlation between {symbol1} and {symbol2}: {correlation}")


import numpy as np

def find_average_lag(df, symbol1, symbol2, max_lag=20):
    # Aggregate duplicate timestamps by mean price
    df1 = df[df["symbol"] == symbol1].groupby("global_timestamp")["price"].mean()
    df2 = df[df["symbol"] == symbol2].groupby("global_timestamp")["price"].mean()

    # Get full sorted union of timestamps
    all_timestamps = sorted(set(df1.index).union(df2.index))

    # Reindex with ffill to align on same timeline
    s1 = df1.reindex(all_timestamps).fillna(method='ffill')
    s2 = df2.reindex(all_timestamps).fillna(method='ffill')

    # Detrend (remove mean)
    s1 -= s1.mean()
    s2 -= s2.mean()

    # Compute correlation for different lags
    lags = range(-max_lag, max_lag + 1)
    correlations = [s1.corr(s2.shift(lag)) for lag in lags]

    # Best lag = one with max correlation
    best_lag = lags[np.nanargmax(correlations)]
    max_corr = np.nanmax(correlations)

    return best_lag, max_corr


for symbol1 in g:
    for symbol2 in g:
        if symbol1 != symbol2:
            lag, corr = find_average_lag(df, symbol1, symbol2)
            print(f"Average lag between {symbol1} and {symbol2}: {lag}, correlation: {corr}")


            # Find pairs with both high correlation and high time lag
threshold_corr = 0.3  # Adjust as needed
threshold_lag = 0   # Adjust as needed

high_corr_lag_pairs = []

for symbol1 in g:
    for symbol2 in g:
        if symbol1 != symbol2:
            lag, corr = find_average_lag(df, symbol1, symbol2)
            if abs(corr) >= threshold_corr and abs(lag) >= threshold_lag:
                high_corr_lag_pairs.append((symbol1, symbol2, lag, corr))

# Print results
for symbol1, symbol2, lag, corr in high_corr_lag_pairs:
    print(f"High correlation and lag: {symbol1} and {symbol2} -> Lag: {lag}, Correlation: {corr}")




