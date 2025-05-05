import json

class ConfigManager:
    """
    This class is responsible for loading the configuration file.
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}

        self.nodes = []
        self.drive_credentials = {}

        self.load_config()

    def load_config(self):
        """
        Load the configuration file.
        """
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
                self.nodes = self.config.get("nodes", [])
                self.drive_credentials = self.config.get("drive_credentials", {})
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file {self.config_file}.")

    def save_config(self, obj):
        """
        Save the configuration to the file.
        """
        try:
            with open(self.config_file, 'w') as file:
                json.dump(
                    {
                        "drive_credentials": self.drive_credentials,
                        "nodes": obj
                    },
                    file, indent=4
                    )
        except Exception as e:
            print(f"Error saving configuration to {self.config_file}: {e}")