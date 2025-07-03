import os
from dotenv import load_dotenv
from finlab import data, backtest, login


def load_api_key(env_var="FINLAB_API_TOKEN"):
    """Retrieve API token from environment variable or .env file."""
    load_dotenv()
    token = os.getenv(env_var)
    if token:
        login(token)
    else:
        raise EnvironmentError(
            f"Missing API token. Please set {env_var} environment variable.")


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


def run_backtest(start='2020'):
    rebalance = data.get('fundamental_features:淨值除資產').deadline().index
    position = build_position(rebalance)
    return backtest.sim(position.loc[start:], resample=rebalance)


if __name__ == "__main__":
    load_api_key()
    result = run_backtest()
    print(result.display())
