#!/usr/bin/env python3
# data_preprocessor.py
# Reads market_trends.json and produces market_stats.json with per-asset metrics and correlation matrix

import argparse
import json
import os
from pathlib import Path
import sys
import traceback
import numpy as np
import pandas as pd
import math
from datetime import datetime

BUSINESS_DAYS_PER_YEAR = 252

def safe_series_from_list(list_of_dicts):
    if not list_of_dicts:
        return pd.Series(dtype=float)
    df = pd.DataFrame(list_of_dicts)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
    return df['value']

def max_drawdown(series):
    if series.empty:
        return None, None
    roll_max = series.cummax()
    drawdown = series / roll_max - 1.0
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    return float(round(max_dd, 4)), max_dd_date.strftime('%Y-%m-%d')

def analyze_series(series):
    if series.empty or len(series) < 2:
        return {}
    daily_ret = series.pct_change().dropna()
    mean_daily = float(daily_ret.mean())
    vol_daily = float(daily_ret.std())
    annualized_return = (1 + mean_daily) ** BUSINESS_DAYS_PER_YEAR - 1
    annual_vol = vol_daily * math.sqrt(BUSINESS_DAYS_PER_YEAR)
    # CAGR
    days = (series.index[-1] - series.index[0]).days
    years = max(days / 365.25, 1/365.25)
    cagr = (series.iloc[-1] / series.iloc[0]) ** (1.0 / years) - 1.0
    # Sharpe (rf default 3.5%)
    rf = 0.035
    sharpe = (annualized_return - rf) / annual_vol if annual_vol > 0 else None
    best_worst_year = series.resample('Y').last().pct_change().dropna()
    best_year = float(round(best_worst_year.max(), 4)) if not best_worst_year.empty else None
    worst_year = float(round(best_worst_year.min(), 4)) if not best_worst_year.empty else None
    max_dd, max_dd_date = max_drawdown(series)
    stats = {
        "first_date": series.index[0].strftime('%Y-%m-%d'),
        "last_date": series.index[-1].strftime('%Y-%m-%d'),
        "last_price": float(round(series.iloc[-1], 2)),
        "num_observations": int(series.shape[0]),
        "cagr_percent": round(cagr * 100, 2),
        "avg_annual_return_percent": round(annualized_return * 100, 2),
        "annual_volatility_percent": round(annual_vol * 100, 2),
        "sharpe_ratio": round(sharpe, 3) if sharpe is not None else None,
        "max_drawdown_percent": round(max_dd * 100, 2) if max_dd is not None else None,
        "max_drawdown_date": max_dd_date,
        "best_year_return_percent": round(best_year * 100, 2) if best_year is not None else None,
        "worst_year_return_percent": round(worst_year * 100, 2) if worst_year is not None else None
    }
    return stats

def build_correlations(series_map):
    # series_map: name -> pd.Series (value indexed by date)
    if not series_map:
        return {}
    df = pd.concat(series_map, axis=1)
    df = df.sort_index()
    daily_returns = df.pct_change().dropna(how='all')
    corr = daily_returns.corr()
    return corr.round(4).to_dict()

def main(argv=None):
    parser = argparse.ArgumentParser(description='Preprocess market_trends.json into market_stats.json')
    parser.add_argument('--infile', '-i', default='market_trends.json', help='Input JSON file (market_trends.json)')
    parser.add_argument('--outfile', '-o', default='market_stats.json', help='Output JSON file (market_stats.json)')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args(argv)

    try:
        infile = Path(args.infile)
        if not infile.exists():
            print(f"Error: input file {infile} not found. Run generate_market_data.py first.")
            return

        with open(infile, 'r', encoding='utf-8') as f:
            raw = json.load(f)

        market_trends = raw.get('market_trends', {})
        if args.verbose:
            print("Loaded assets:", list(market_trends.keys()))

        series_map = {}
        stats_map = {}
        for asset, series in market_trends.items():
            s = safe_series_from_list(series)
            series_map[asset] = s
            stats_map[asset] = analyze_series(s)
            if args.verbose:
                print(f"Analyzed {asset}: {stats_map[asset]}")

        correlations = build_correlations(series_map)
        output = {
            "metadata": {
                "generated_on": datetime.utcnow().isoformat() + "Z",
                "source_file": str(infile)
            },
            "asset_stats": stats_map,
            "correlations": correlations
        }

        with open(args.outfile, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
            f.flush()
            try:
                os.fsync(f.fileno())
            except Exception:
                pass

        print(f"Wrote {args.outfile} (assets: {len(stats_map)}).")
        if args.verbose:
            print("Correlation matrix keys:", list(correlations.keys()))
    except Exception:
        print("Error: data_preprocessor.py failed with exception:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()