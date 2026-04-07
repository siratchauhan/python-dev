import hashlib
import hmac
import logging
import time
from typing import Any
from urllib.parse import urlencode

import requests


LOGGER = logging.getLogger(__name__)


class BinanceFuturesClientError(Exception):
    """Base client exception."""


class BinanceAPIError(BinanceFuturesClientError):
    """Raised when Binance returns a non-success response."""

    def __init__(self, status_code: int, message: str, payload: dict[str, Any] | None = None):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.payload = payload or {}


class BinanceFuturesClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: int = 10,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def place_order(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._signed_request("POST", "/fapi/v1/order", params)

    def _signed_request(self, method: str, path: str, params: dict[str, Any]) -> dict[str, Any]:
        payload = {key: value for key, value in params.items() if value is not None}
        payload["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(payload, doseq=True)
        signature = hmac.new(
            self.api_secret,
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_payload = dict(payload)
        signed_payload["signature"] = signature
        url = f"{self.base_url}{path}"

        LOGGER.info(
            "binance_request method=%s url=%s payload=%s",
            method,
            url,
            signed_payload,
        )

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=signed_payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            LOGGER.exception("binance_network_error method=%s url=%s", method, url)
            raise BinanceFuturesClientError(f"Network error while calling Binance: {exc}") from exc

        raw_text = response.text.strip()
        LOGGER.info(
            "binance_response status_code=%s body=%s",
            response.status_code,
            raw_text,
        )

        try:
            data = response.json()
        except ValueError as exc:
            raise BinanceFuturesClientError(
                f"Unable to parse Binance response as JSON: {raw_text}"
            ) from exc

        if not response.ok:
            message = data.get("msg", "Unknown Binance API error")
            raise BinanceAPIError(response.status_code, message, data)

        return data
