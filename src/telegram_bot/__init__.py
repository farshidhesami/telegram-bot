"""
Telegram Bot Package Initialization.

This module initializes the `telegram_bot` package by exposing the following components:
- Command Handlers: `start_command`, `get_crypto_price`
- Utility Functions: `fetch_crypto_price`, `check_signals`
- Configuration Management: `ConfigurationManager`

Usage:
    from telegram_bot import start_command, ConfigurationManager
"""

# Expose components as part of the package
from .components.command_handler import start_command, get_crypto_price
from .components.utils import fetch_crypto_price, check_signals
from .config.configuration import ConfigurationManager

# Define the public API for the package
__all__ = [
    "start_command",
    "get_crypto_price",
    "fetch_crypto_price",
    "check_signals",
    "ConfigurationManager",
]
