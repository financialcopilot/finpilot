import numpy as np
import pandas as pd
import json
import datetime

def generate_gbm_with_events(
    start_date,
    end_date,
    initial_value,
    mu,
    sigma,
    crash_date=None,
    crash_severity=-0.35,
    crash_duration_days=30,
    volatility_event_date=None,
    volatility_increase=0.5,
    volatility_duration_days=90,
):
    """
    Generates a Geometric Brownian Motion series with optional crash and volatility events.
    """
    dates = pd.date_range(start_date, end_date, freq='B')
    n_days = len(dates)
    dt = 1 / 252

    returns = np.random.normal(loc=(mu * dt), scale=(sigma * np.sqrt(dt)), size=n_days)
    
    if crash_date:
        # CORRECTED: Use index.get_indexer for modern pandas versions
        crash_datetime = pd.to_datetime(crash_date)
        crash_start_idx = dates.get_indexer([crash_datetime], method='nearest')[0]
        crash_end_idx = min(crash_start_idx + crash_duration_days, n_days)
        
        crash_returns = np.linspace(0, crash_severity, crash_duration_days)
        crash_noise = np.random.normal(0, sigma * 0.5, crash_duration_days)
        
        if crash_end_idx - crash_start_idx == crash_duration_days:
            returns[crash_start_idx:crash_end_idx] = (crash_returns / crash_duration_days) + crash_noise

    if volatility_event_date:
        # CORRECTED: Use index.get_indexer for modern pandas versions
        vol_datetime = pd.to_datetime(volatility_event_date)
        vol_start_idx = dates.get_indexer([vol_datetime], method='nearest')[0]
        vol_end_idx = min(vol_start_idx + volatility_duration_days, n_days)
        
        high_vol_returns = np.random.normal(
            loc=(mu * dt),
            scale=(sigma * (1 + volatility_increase) * np.sqrt(dt)),
            size=(vol_end_idx - vol_start_idx)
        )
        returns[vol_start_idx:vol_end_idx] = high_vol_returns

    price_path = initial_value * np.exp(np.cumsum(returns))
    series = pd.Series(price_path, index=dates)
    return [{"date": date.strftime('%Y-%m-%d'), "value": round(val, 2)} for date, val in series.items()]

def main():
    """
    Main function to define asset classes and generate the final JSON file.
    """
    print("Generating sophisticated market trend data...")
    start_date = datetime.date.today() - datetime.timedelta(days=10 * 365)
    end_date = datetime.date.today()
    
    asset_params = {
        "equities": {"mu": 0.12, "sigma": 0.22, "initial": 100},
        "bonds": {"mu": 0.07, "sigma": 0.08, "initial": 100},
        "crypto": {"mu": 0.35, "sigma": 0.80, "initial": 100},
        "commodities": {"mu": 0.05, "sigma": 0.15, "initial": 100}
    }
    
    market_trends = {}
    for asset, params in asset_params.items():
        print(f"  -> Simulating for {asset}...")
        market_trends[asset] = generate_gbm_with_events(
            start_date=start_date,
            end_date=end_date,
            initial_value=params["initial"],
            mu=params["mu"],
            sigma=params["sigma"],
            crash_date="2020-03-01",
            volatility_event_date="2025-01-01"
        )

    output = {"market_trends": market_trends}
    
    with open("market_trends.json", "w") as f:
        json.dump(output, f, indent=2)
        
    print("\nSuccessfully created market_trends.json with realistic events.")

if __name__ == "__main__":
    main()