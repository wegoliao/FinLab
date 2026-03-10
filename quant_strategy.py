import os
import argparse
from dotenv import load_dotenv
from finlab import data, backtest, login


def load_api_key(env_file: str, env_var: str) -> None:
    """Retrieve API token from environment variable or .env file."""
    load_dotenv(env_file)
    token = os.getenv(env_var)
    if not token:
        raise EnvironmentError(
            f"Missing API token. Please set {env_var} or provide {env_file}"
        )
    login(token)


def parse_args():
    parser = argparse.ArgumentParser(description="Run FinLab QUAN backtest")
    parser.add_argument(
        "--start",
        default="2020",
        help="Backtest start date (YYYY or YYYY-MM-DD)",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file containing the API token",
    )
    parser.add_argument(
        "--token-var",
        default="FINLAB_API_TOKEN",
        help="Environment variable name for the API token",
    )
    return parser.parse_args()


def build_position(rebalance_dates):
    """Construct portfolio positions using financial indicators."""
    close = data.get('price:收盤價')
    volume = data.get('price:成交股數')

    rd_ratio = data.get('fundamental_features:研究發展費用率')
    pm_ratio = data.get('fundamental_features:管理費用率')
    eq_ratio = data.get('fundamental_features:淨值除資產').deadline()

    rd_pm = rd_ratio / pm_ratio
    eq_price = eq_ratio / close.reindex(eq_ratio.index, method='ffill')

    base_filter = (
        (close > close.average(60)) &
        (volume > 200_000) &
        (volume.average(10) > volume.average(60)) &
        (rd_pm.deadline().rank(axis=1, pct=True) > 0.5)
    )

    return eq_price[base_filter].reindex(rebalance_dates).is_largest(20)


def run_backtest(start="2020"):
    rebalance = data.get("fundamental_features:淨值除資產").deadline().index
    position = build_position(rebalance)
    return backtest.sim(position.loc[start:], resample=rebalance)


if __name__ == "__main__":
    args = parse_args()
    load_api_key(args.env_file, args.token_var)
    result = run_backtest(args.start)
    print(result.display())
