import sys
import time
import logging
from pathlib import Path

# Add the project root to PYTHONPATH dynamically
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from telegram.ext import Updater, CommandHandler
from telegram_bot.components.command_handler import start_command, get_crypto_price
from telegram_bot.components.utils import check_signals
from telegram_bot.config.configuration import ConfigurationManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")


def initialize_bot(config_manager):
    """
    Initialize the Telegram bot and register commands.
    
    Args:
        config_manager (ConfigurationManager): The configuration manager to load bot settings.
    
    Returns:
        Updater: The initialized bot Updater.
    """
    bot_token = config_manager.get("bot.token")
    if not bot_token:
        raise ValueError("Bot token is missing in configuration.")

    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Register bot commands
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("price", get_crypto_price))

    logging.info("Commands registered successfully.")
    return updater


def monitor_signals(config_manager):
    """
    Monitor cryptocurrency signals and send alerts via Telegram.
    
    Args:
        config_manager (ConfigurationManager): The configuration manager to load bot settings.
    """
    symbols = config_manager.get("bot.symbols", [])
    interval = config_manager.get("bot.interval", "1hour")
    monitoring_interval = config_manager.get("bot.monitoring_interval", 60)  # Default: 60 seconds

    bot_token = config_manager.get("bot.token")
    chat_id = config_manager.get("bot.chat_id")

    logging.info(f"Starting signal monitoring for symbols: {symbols}")
    try:
        while True:
            for symbol in symbols:
                check_signals(symbol, interval, bot_token, chat_id)
            logging.info(f"Waiting for {monitoring_interval} seconds before the next cycle...")
            time.sleep(monitoring_interval)
    except KeyboardInterrupt:
        logging.info("Signal monitoring stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error during signal monitoring: {e}")


def main():
    """
    Main entry point for the Telegram bot.
    """
    # Load configurations
    config_manager = ConfigurationManager()

    # Initialize bot
    try:
        updater = initialize_bot(config_manager)
        logging.info("🚀 Bot is running... Press Ctrl+C to stop.")
        updater.start_polling()

        # Start monitoring signals
        monitor_signals(config_manager)
    except ValueError as ve:
        logging.error(f"Configuration error: {ve}")
    except Exception as e:
        logging.error(f"Failed to initialize the bot: {e}")
    finally:
        logging.info("Bot stopped.")


if __name__ == "__main__":
    main()
