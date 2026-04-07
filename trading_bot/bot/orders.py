from decimal import Decimal
from typing import Any

from bot.client import BinanceFuturesClient


def place_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: Decimal,
    price: Decimal | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": _decimal_to_str(quantity),
        "newOrderRespType": "RESULT",
    }

    if order_type == "LIMIT":
        params["price"] = _decimal_to_str(price)
        params["timeInForce"] = "GTC"

    return client.place_order(params)


def format_order_response(order: dict[str, Any]) -> str:
    lines = [
        f"orderId={order.get('orderId', 'N/A')}",
        f"status={order.get('status', 'N/A')}",
        f"executedQty={order.get('executedQty', 'N/A')}",
        f"avgPrice={_extract_avg_price(order)}",
    ]
    return "\n".join(f"  {line}" for line in lines)


def _extract_avg_price(order: dict[str, Any]) -> str:
    for key in ("avgPrice", "priceAvg", "ap", "price"):
        value = order.get(key)
        if value not in (None, ""):
            return str(value)
    return "N/A"


def _decimal_to_str(value: Decimal | None) -> str:
    if value is None:
        return ""
    return format(value, "f")
