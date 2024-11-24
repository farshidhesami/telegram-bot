from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.components.utils import fetch_crypto_price

# Cryptocurrency references for detailed links
COIN_REFERENCES = {
    "BTC": "https://coinmarketcap.com/currencies/bitcoin/",
    "ETH": "https://coinmarketcap.com/currencies/ethereum/",
    "SOL": "https://coinmarketcap.com/currencies/solana/",
    "BNB": "https://coinmarketcap.com/currencies/bnb/",
    "ADA": "https://coinmarketcap.com/currencies/cardano/",
    "XRP": "https://coinmarketcap.com/currencies/xrp/",
}

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
        "- BTC (Bitcoin)\n"
        "- ETH (Ethereum)\n"
        "- SOL (Solana)\n"
        "- BNB (Binance Coin)\n"
        "- ADA (Cardano)\n"
        "- XRP (Ripple)\n\n"
        "Example: `/price BTC`"
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
            f"❌ '{symbol}' is not supported. Try BTC, ETH, SOL, BNB, ADA, or XRP."
        )
        return

    # Fetch the price using the utility function
    price, error = fetch_crypto_price(symbol)
    if error:
        update.message.reply_text(f"⚠️ Error fetching price for {symbol}: {error}")
        return

    # Format the response with the price and reference link
    reference_link = COIN_REFERENCES[symbol]
    message = (
        f"💰 *{symbol} Price*: ${price:.2f}\n"
        f"🔗 [View on CoinMarketCap]({reference_link})"
    )
    update.message.reply_text(message, parse_mode="Markdown")
