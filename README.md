# Binance Futures Testnet Trading Bot

Small Python CLI application for placing USDT-M futures orders on Binance Futures Testnet.

## Features

- Places `MARKET` and `LIMIT` orders
- Supports both `BUY` and `SELL`
- Uses a separate CLI layer, validation layer, and API client layer
- Logs request payloads, responses, and failures to a file
- Handles invalid input, Binance API errors, and network failures

## Project structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    logging_config.py
    orders.py
    validators.py
  cli.py
README.md
requirements.txt
```

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Set Binance Futures Testnet credentials:

```powershell
setx BINANCE_API_KEY "your_api_key"
setx BINANCE_API_SECRET "your_api_secret"
```

4. Open a new terminal so the environment variables are available.

## Run examples

Market order:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001 --log-file logs\market_order.log
```

Limit order:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 65000 --log-file logs\limit_order.log
```

Explicit credentials:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001 --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET
```

## CLI arguments

- `--symbol` required, example `BTCUSDT`
- `--side` required, `BUY` or `SELL`
- `--order-type` required, `MARKET` or `LIMIT`
- `--quantity` required, positive decimal
- `--price` required for `LIMIT`
- `--api-key` optional if `BINANCE_API_KEY` is set
- `--api-secret` optional if `BINANCE_API_SECRET` is set
- `--base-url` optional, defaults to `https://testnet.binancefuture.com`
- `--log-file` optional, defaults to `trading_bot.log`

## Output

The CLI prints:

- order request summary
- order response details including `orderId`, `status`, `executedQty`, and `avgPrice` when present
- a clear success or failure message

## Assumptions

- The app targets Binance Futures Testnet USDT-M endpoints only.
- `LIMIT` orders are sent with `timeInForce=GTC`.
- The default response mode is `RESULT` so order details are returned immediately when Binance provides them.
- Real market and limit log files can only be generated after valid testnet credentials are supplied.
