import customtkinter as ctk

class MachineList(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=(5, 0), pady=5, anchor="w", side="left", fill="y")

        # Add Machine List title
        self.title_label = ctk.CTkLabel(self.frame, text="Render Nodes", font=ctk.CTkFont(size=15, weight="bold"), height=40)
        self.title_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        # Add Machine Listbox
        self.machine_list_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent", width=350)
        self.machine_list_frame.pack(fill="both", expand=True)