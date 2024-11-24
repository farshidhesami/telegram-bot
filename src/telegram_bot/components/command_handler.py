from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.components.utils import fetch_crypto_price
from telegram_bot.config.configuration import ConfigurationManager

# Load configuration dynamically
config_manager = ConfigurationManager()
symbols = config_manager.get("bot.symbols", [])
COIN_REFERENCES = {symbol.split("USDT")[0]: f"https://coinmarketcap.com/currencies/{symbol.split('USDT')[0].lower()}/" for symbol in symbols}


def start_command(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command to introduce the bot and provide help instructions.

    Args:
        update (Update): Incoming Telegram update.
        context (CallbackContext): Callback context for the command.

    Returns:
        None
    """
    message = (
        "👋 Welcome to Crypto Signals Bot! 🚀\n\n"
        "Here are the available commands:\n"
        "1. `/start` - View this help message.\n"
        "2. `/price [symbol]` - Get the current price of a cryptocurrency.\n\n"
        "Supported cryptocurrencies:\n"
        + "\n".join([f"- {symbol} ({symbol.lower().capitalize()})" for symbol in COIN_REFERENCES.keys()])
        + "\n\nExample: `/price BTC`"
    )
    update.message.reply_text(message)


def get_crypto_price(update: Update, context: CallbackContext) -> None:
    """
    Handle the /price command to fetch cryptocurrency prices.

    Args:
        update (Update): Incoming Telegram update.
        context (CallbackContext): Callback context for the command.

    Returns:
        None
    """
    args = context.args
    if not args:
        update.message.reply_text("❗ Please specify a cryptocurrency symbol (e.g., BTC, ETH).")
        return

    symbol = args[0].upper()
    if symbol not in COIN_REFERENCES:
        update.message.reply_text(
            f"❌ '{symbol}' is not supported. Try one of the following: {', '.join(COIN_REFERENCES.keys())}."
        )
        return

    # Fetch the price using the utility function
    price, error = fetch_crypto_price(symbol)
    if error:
        if "Invalid API Key" in error:
            update.message.reply_text("❌ The API key for CoinMarketCap is invalid. Please check your configuration.")
        else:
            update.message.reply_text(f"⚠️ Error fetching price for {symbol}: {error}")
        return

    # Format the response with the price and reference link
    reference_link = COIN_REFERENCES[symbol]
    message = (
        f"💰 *{symbol} Price*: ${price:.2f}\n"
        f"🔗 [View on CoinMarketCap]({reference_link})"
    )
    update.message.reply_text(message, parse_mode="Markdown")
