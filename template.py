from pathlib import Path
import logging

# Configure logging for structured output
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Prompt for project name
project_name = input("Enter the project name: ").strip() or "telegram_bot"

# List of files and directories to create
list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/command_handler.py",
    f"src/{project_name}/components/utils.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/main.py",
    "config/config.yaml",
    "requirements.txt",
    ".env",
    "setup.py",
    "README.md",
]

# File templates for default content
file_templates = {
    "requirements.txt": "# Add your Python dependencies here\n",
    ".env": "# Store your environment variables here\n",
    "README.md": f"# {project_name.capitalize()} Documentation\n\nThis project is a Telegram bot for cryptocurrency signals.\n",
    "setup.py": f"""import setuptools

setuptools.setup(
    name="{project_name}",
    version="0.1.0",
    description="A Telegram bot for cryptocurrency signals",
    author="Your Name",
    packages=setuptools.find_packages(where='src'),
    package_dir={{'': 'src'}},
    install_requires=[
        "requests",
        "numpy",
        "python-decouple",
        "python-telegram-bot",
        "pyyaml",
    ],
)
""",
    f"src/{project_name}/main.py": """# Main entry point for the bot
def main():
    print("Starting the Telegram bot...")

if __name__ == "__main__":
    main()
""",
    "config/config.yaml": """bot:
  token: "YOUR_TELEGRAM_BOT_TOKEN"
  chat_id: "YOUR_TELEGRAM_CHAT_ID"
  symbols:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - ADAUSDT
    - XRPUSDT
  interval: "1hour"
  monitoring_interval: 60

api:
  coinmarketcap:
    key: "YOUR_COINMARKETCAP_API_KEY"

logging:
  level: "INFO"
  format: "[%(asctime)s] %(levelname)s: %(message)s"
"""
}

# Create files and directories
created_files = []
existing_files = []

for filepath_str in list_of_files:
    filepath = Path(filepath_str)

    # Create parent directories if they don't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)
    logging.info(f"Verified directory: {filepath.parent}")

    # Create the file with default content if it doesn't exist
    if not filepath.exists():
        default_content = file_templates.get(filepath.name, "")
        with filepath.open("w") as file:
            file.write(default_content)
        created_files.append(filepath)
        logging.info(f"Created file: {filepath} with default content.")
    else:
        existing_files.append(filepath)
        logging.info(f"File already exists: {filepath}")

# Summary
logging.info("\nProject structure creation complete!")
logging.info(f"Created files: {len(created_files)}")
logging.info(f"Existing files: {len(existing_files)}")
