import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigurationManager:
    """
    A utility class to manage configuration loading and retrieval from a YAML file.
    """

    def __init__(self, config_file_path="config/config.yaml"):
        """
        Initialize the ConfigurationManager.

        Args:
            config_file_path (str): Path to the configuration YAML file.
        """
        self.config_file_path = os.path.abspath(config_file_path)  # Normalize the file path
        self.config = self._load_config()

    def _load_config(self):
        """
        Load the configuration from the YAML file.

        Returns:
            dict: Loaded configuration data.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If there is an error parsing the YAML file.
        """
        if not os.path.exists(self.config_file_path):
            logger.error(f"Configuration file not found: {self.config_file_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_file_path}")

        with open(self.config_file_path, "r") as yaml_file:
            try:
                config = yaml.safe_load(yaml_file)
                logger.info(f"Configuration loaded successfully from {self.config_file_path}")
                return config
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML file {self.config_file_path}: {e}")
                raise ValueError(f"Error loading YAML configuration: {e}")

    def get(self, key, default=None):
        """
        Retrieve a configuration value using a dot-separated key.

        Args:
            key (str): Dot-separated key to the configuration value (e.g., "bot.token").
            default: Default value to return if the key is not found.

        Returns:
            Any: The configuration value or the default value if the key is not found.
        """
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            # Fallback to environment variable
            env_value = os.getenv(key.replace(".", "_").upper())
            if env_value is not None:
                return env_value
            return default

    def __repr__(self):
        """
        Return a string representation of the ConfigurationManager.

        Returns:
            str: String representation of the loaded configuration.
        """
        return f"<ConfigurationManager(config_file_path={self.config_file_path})>"
