import json


class ConfigManager:
    """A class for managing configuration settings.

    This class provides methods for loading, retrieving, updating, and saving configuration settings.
    Configuration settings are stored in a JSON file.

    Attributes:
        `file_path`: The path to the JSON configuration file.
    """

    def __init__(self, file_path: str = "config/config.json") -> None:
        """
        Initialize the JSONConfig object.

        Args:
            file_path (str): The path to the JSON configuration file.
        """
        self.file_path = file_path
        self._load_config()

    def _load_config(self) -> None:
        """
        Load the configuration from the JSON file.
        """
        with open(self.file_path, "r") as file:
            self.config = json.load(file)

    def get(self, key: str) -> any:
        """
        Retrieve the value associated with the given key.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            any: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the configuration.
        """
        if key in self.config:
            return self.config[key]
        else:
            raise KeyError(f"The key '{key}' is not found in the JSON.")

    def set(self, key: str, value: any) -> None:
        """
        Set the value associated with the given key.

        Args:
            key (str): The key to set the value for.
            value (any): The value to be set.
        """

        if key in self.config:
            self.config[key] = value
        else:
            raise KeyError(f"The key '{key}' is not found in the JSON.")

    def save(self) -> bool:
        """
        Saves the configuration data to a file.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.config, file, indent=4)
            return True
        except Exception:
            return False

    def json(self) -> dict:
        """
        Returns the configuration data as a dictionary.

        Returns:
            dict: The configuration data.
        """
        return self.config
