import json

class ConfigManager:
    """
    This class is responsible for loading the configuration file.
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}

    def load_config(self):
        """
        Load the configuration file.
        """
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
                return self.config.get("machines", [])
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file {self.config_file}.")
            return []

    def save_config(self, obj):
        """
        Save the configuration to the file.
        """
        try:
            with open(self.config_file, 'w') as file:
                json.dump({"machines": obj}, file, indent=4)
        except Exception as e:
            print(f"Error saving configuration to {self.config_file}: {e}")