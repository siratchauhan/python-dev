import argparse
import os

from bot.client import BinanceFuturesClient, BinanceAPIError, BinanceFuturesClientError
from bot.logging_config import setup_logging
from bot.orders import format_order_response, place_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simplified Binance Futures Testnet trading bot."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, for example BTCUSDT")
    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--order-type",
        required=True,
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity", required=True, help="Order quantity, for example 0.001"
    )
    parser.add_argument(
        "--price",
        required=False,
        help="Limit order price. Required when order-type is LIMIT.",
    )
    parser.add_argument(
        "--api-key",
        required=False,
        default=os.environ.get("BINANCE_API_KEY"),
        help="Binance Futures API key. Can also be provided with BINANCE_API_KEY environment variable.",
    )
    parser.add_argument(
        "--api-secret",
        required=False,
        default=os.environ.get("BINANCE_API_SECRET"),
        help="Binance Futures API secret. Can also be provided with BINANCE_API_SECRET environment variable.",
    )
    parser.add_argument(
        "--base-url",
        required=False,
        default="https://testnet.binancefuture.com",
        help="Binance Futures Testnet base URL.",
    )
    parser.add_argument(
        "--log-file",
        required=False,
        default="trading_bot.log",
        help="Path to the log file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.log_file)

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price) if args.price else None

        if order_type == "LIMIT" and not price:
            raise ValueError("Price is required for LIMIT orders")

        if order_type == "MARKET" and price:
            print("Warning: price is ignored for MARKET orders")

        if not args.api_key or not args.api_secret:
            raise ValueError(
                "API key and secret are required. Set BINANCE_API_KEY and BINANCE_API_SECRET or pass --api-key and --api-secret."
            )

        client = BinanceFuturesClient(
            api_key=args.api_key,
            api_secret=args.api_secret,
            base_url=args.base_url,
        )

        print("Order request summary:")
        print(f"  symbol={symbol}")
        print(f"  side={side}")
        print(f"  order_type={order_type}")
        print(f"  quantity={quantity}")
        print(f"  price={price if price else 'N/A'}")

        order = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        print("\nOrder response details:")
        print(format_order_response(order))
        print("\nSuccess: order created successfully.")
        return 0

    except ValueError as exc:
        print(f"Input validation error: {exc}")
        return 1
    except BinanceAPIError as exc:
        print(f"Binance API error: {exc}")
        return 2
    except BinanceFuturesClientError as exc:
        print(f"Client error: {exc}")
        return 3
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
