import customtkinter as ctk
from modules.Header import Header
from modules.Footer import Footer
from modules.MachineList import MachineList
from modules.MachineDetails import MachineDetails
from modules.RenderLog import RenderLog
from modules.ConfigManager import ConfigManager
from modules.LogManager import LogManager
from modules.MachineManager import MachineManager
from modules.RenderManager import RenderManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Render Utility")
        self.root.geometry("1600x900")
        self.root.minsize(1000, 600)

        self.active_machine = None  # Currently selected machine
        self.render_logs = {}  # Dictionary to hold render logs for each machine

        # Load configuration
        self.config_manager = ConfigManager("config.json")
        self.machines = self.config_manager.load_config()

        # Create Main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Create header
        self.header = Header(self, self.main_frame)

        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.middle_frame.pack(fill="both", expand=True)

        # Create Machine List
        self.machine_list = MachineList(self, self.middle_frame)

        # Create Machine Details Panel
        self.machine_details_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent")
        self.machine_details_frame.pack(anchor="e", fill="both", expand=True)

        self.machine_details = MachineDetails(self, self.machine_details_frame)
        self.render_log = RenderLog(self.machine_details_frame)

        # Create Footer
        self.footer = Footer(self, self.main_frame)

        self.log_manager = LogManager(self)
        self.machine_manager = MachineManager(self)
        self.render_manager = RenderManager(self)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()