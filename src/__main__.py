import customtkinter as ctk
from modules.Header import Header
from modules.Footer import Footer
from modules.NodeList import NodeList
from modules.NodeDetails import NodeDetails
from modules.RenderLog import RenderLog
from modules.ConfigManager import ConfigManager
from modules.LogManager import LogManager
from modules.NodeManager import NodeManager
from modules.RenderManager import RenderManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Render Utility")
        self.root.geometry("1400x900")
        self.root.minsize(1100, 600)

        ctk.ThemeManager().load_theme("theme.json")

        self.active_node = None  # Currently selected node
        self.render_logs = {}  # Dictionary to hold render logs for each node

        # Load configuration
        self.config_manager = ConfigManager("config.json")
        self.nodes = self.config_manager.nodes
        self.drive_credentials = self.config_manager.drive_credentials

        # Create Main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="transparent", border_width=0)
        self.main_frame.pack(fill="both", expand=True)

        # Create header
        self.header = Header(self, self.main_frame)

        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", border_width=0)
        self.middle_frame.pack(fill="both", expand=True)

        # Create Node List
        self.node_list = NodeList(self, self.middle_frame)

        # Create Node Details Panel
        self.node_details_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent", border_width=0)
        self.node_details_frame.pack(anchor="e", fill="both", expand=True)

        self.node_details = NodeDetails(self, self.node_details_frame)
        self.render_log = RenderLog(self, self.node_details_frame)

        # Create Footer
        self.footer = Footer(self, self.main_frame)

        self.log_manager = LogManager(self)
        self.node_manager = NodeManager(self)
        self.render_manager = RenderManager(self)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()