import requests
import numpy as np
import telebot
from decouple import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Load environment variables
TOKEN = config("TELEGRAM_BOT_TOKEN")  # Telegram bot token
CHAT_ID = config("TELEGRAM_CHAT_ID")  # Telegram chat/channel ID
COINMARKETCAP_API_KEY = config("COINMARKETCAP_API_KEY")  # CoinMarketCap API key
bot = telebot.TeleBot(TOKEN)

# Store the last signal states
last_signals = {}  # Track the last signal for each cryptocurrency


def fetch_crypto_price(symbol):
    """
    Fetch the latest cryptocurrency price using CoinMarketCap API.

    Args:
        symbol (str): Cryptocurrency symbol (e.g., "BTC").

    Returns:
        tuple: (float, str) - Current price of the cryptocurrency, or an error message.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    params = {"symbol": symbol.upper(), "convert": "USD"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        price = data["data"][symbol]["quote"]["USD"]["price"]
        return price, None
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None, str(e)


def get_candles(symbol, interval, limit=50):
    """
    Fetch candle data (OHLC) for a cryptocurrency.

    Args:
        symbol (str): Cryptocurrency pair symbol (e.g., "BTCUSDT").
        interval (str): Candle interval (e.g., "1hour").
        limit (int): Number of candles to fetch.

    Returns:
        np.ndarray: Array of candle data (time, close price, volume).
    """
    url = "https://api.coinex.com/v1/market/kline"
    params = {"market": symbol, "type": interval, "limit": limit}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        return np.array([[float(item[0]), float(item[2]), float(item[5])] for item in data])  # time, close, volume
    except Exception as e:
        logging.error(f"Error fetching candles for {symbol}: {e}")
        raise


def highpass_filter(close, alpha1):
    """
    Apply a high-pass filter to a series of closing prices.

    Args:
        close (np.ndarray): Array of closing prices.
        alpha1 (float): Filter coefficient.

    Returns:
        np.ndarray: Filtered data.
    """
    hp = np.zeros(len(close))
    for i in range(2, len(close)):
        hp[i] = (
            (1 - alpha1 / 2) * (1 - alpha1 / 2) * (close[i] - 2 * close[i - 1] + close[i - 2])
            + 2 * (1 - alpha1) * hp[i - 1]
            - (1 - alpha1) * (1 - alpha1) * hp[i - 2]
        )
    return hp


def quotient(x, k1, k2):
    """
    Calculate quotient values for signal processing.

    Args:
        x (np.ndarray): Input data.
        k1 (float): Constant 1.
        k2 (float): Constant 2.

    Returns:
        tuple: Quotient values (q1, q2).
    """
    return (x + k1) / (k1 * x + 1), (x + k2) / (k2 * x + 1)


def signal_cross(q1, trigger):
    """
    Detect buy and sell signals based on crossing a threshold.

    Args:
        q1 (np.ndarray): Signal values.
        trigger (float): Threshold value.

    Returns:
        tuple: Boolean arrays for buy and sell signals.
    """
    buy_signal = (q1 < trigger)
    sell_signal = (q1 > trigger)
    return buy_signal, sell_signal


def send_signal(message):
    """
    Send a message to the configured Telegram chat/channel.

    Args:
        message (str): The message to send.

    Returns:
        None
    """
    try:
        bot.send_message(CHAT_ID, message)
        logging.info(f"Message sent: {message}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


def calculate_risk_levels(entry_price, take_profit_percentage=2, stop_loss_percentage=1):
    """
    Calculate take-profit and stop-loss levels based on entry price.

    Args:
        entry_price (float): Entry price for the signal.
        take_profit_percentage (float): Take-profit percentage.
        stop_loss_percentage (float): Stop-loss percentage.

    Returns:
        tuple: Formatted take-profit and stop-loss levels.
    """
    take_profit = entry_price * (1 + take_profit_percentage / 100)
    stop_loss = entry_price * (1 - stop_loss_percentage / 100)
    return f"{take_profit:.6f}", f"{stop_loss:.6f}"


def check_signals(symbol, interval, bot_token, chat_id):
    """
    Analyze and send buy/sell signals based on trading data.

    Args:
        symbol (str): Cryptocurrency pair symbol (e.g., "BTCUSDT").
        interval (str): Candle interval (e.g., "1hour").
        bot_token (str): Telegram bot token.
        chat_id (str): Telegram chat ID.

    Returns:
        None
    """
    try:
        global last_signals
        candles = get_candles(symbol, interval)
        close_prices = candles[:, 1]

        alpha1 = 0.07
        filtered = highpass_filter(close_prices, alpha1)

        k1, k2 = 0.5, 0.3
        q1, q2 = quotient(filtered, k1, k2)

        trigger = 0
        buy_signal, sell_signal = signal_cross(q1, trigger)

        current_price, error = fetch_crypto_price(symbol.split("USDT")[0])
        if error:
            return

        if symbol not in last_signals:
            last_signals[symbol] = {"buy": False, "sell": False}

        if buy_signal[-1] and not last_signals[symbol]["buy"]:
            take_profit, stop_loss = calculate_risk_levels(current_price)
            message = (
                f"🔵 **Buy Signal ({symbol})** 🔵\n"
                f"🔹 Entry Price: {current_price:.6f} USD\n"
                f"🔹 Take Profit: {take_profit} USD\n"
                f"🔹 Stop Loss: {stop_loss} USD"
            )
            send_signal(message)
            last_signals[symbol]["buy"] = True
            last_signals[symbol]["sell"] = False

        if sell_signal[-1] and not last_signals[symbol]["sell"]:
            take_profit, stop_loss = calculate_risk_levels(current_price, take_profit_percentage=-2, stop_loss_percentage=-1)
            message = (
                f"🔴 **Sell Signal ({symbol})** 🔴\n"
                f"🔹 Sell Price: {current_price:.6f} USD\n"
                f"🔹 Take Profit: {take_profit} USD\n"
                f"🔹 Stop Loss: {stop_loss} USD"
            )
            send_signal(message)
            last_signals[symbol]["sell"] = True
            last_signals[symbol]["buy"] = False

    except Exception as e:
        logging.error(f"Error during signal analysis for {symbol}: {e}")
