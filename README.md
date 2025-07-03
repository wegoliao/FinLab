# FinLab

This repository contains a simple example of a FinLab QUAN strategy replicating
FinLab's high-return approach based on three financial indicators. The code
requires a FinLab API token. You can set it via the `FINLAB_API_TOKEN`
environment variable or place it inside a `.env` file.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your API token (do **not** commit the token). Either export it:
   ```bash
   export FINLAB_API_TOKEN=your_token_here
   ```
   Or create a `.env` file in this directory containing:
   ```bash
   FINLAB_API_TOKEN=your_token_here
   ```
3. Run the backtest:
   ```bash
   python quant_strategy.py
   ```

The script will log into the FinLab platform using your token, construct the
portfolio according to the strategy, and print backtest results.
