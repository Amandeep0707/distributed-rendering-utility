import customtkinter as ctk
from modules.Header import Header
from modules.Footer import Footer
from modules.MachineList import MachineList
from modules.MachineDetails import MachineDetails
from modules.RenderLog import RenderLog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomTkinter Test")
        self.root.geometry("1280x720")
        # Create Main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        # Create header
        self.header = Header(self.main_frame)

        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.middle_frame.pack(fill="both", expand=True)

        # Create Machine List
        self.machine_list = MachineList(self.middle_frame)

        # Create Machine Details Panel
        self.machine_details_frame = ctk.CTkFrame(self.middle_frame, fg_color="transparent")
        self.machine_details_frame.pack(anchor="e", fill="both", expand=True)

        self.machine_details = MachineDetails(self.machine_details_frame)
        self.render_log = RenderLog(self.machine_details_frame)

        # Create Footer
        self.footer = Footer(self.main_frame)

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()