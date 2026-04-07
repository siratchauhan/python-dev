from decimal import Decimal, InvalidOperation


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(value: str) -> str:
    symbol = value.strip().upper()
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    if not symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric")
    return symbol


def validate_side(value: str) -> str:
    side = value.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Side must be one of: {', '.join(sorted(VALID_SIDES))}")
    return side


def validate_order_type(value: str) -> str:
    order_type = value.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Order type must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}"
        )
    return order_type


def validate_quantity(value: str) -> Decimal:
    quantity = _parse_positive_decimal(value, "Quantity")
    return quantity


def validate_price(value: str) -> Decimal:
    price = _parse_positive_decimal(value, "Price")
    return price


def _parse_positive_decimal(value: str, field_name: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field_name} must be a valid decimal number") from exc

    if parsed <= 0:
        raise ValueError(f"{field_name} must be greater than zero")

    return parsed
