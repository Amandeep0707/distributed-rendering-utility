import customtkinter as ctk

class MachineDetails(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=5, anchor="ne", fill="x", expand=True)

        self.machine_info_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.machine_info_frame.pack(anchor="w", side="left", expand=True)

        self.machine_name = ctk.StringVar(value="Machine Details")
        self.machine_details_label = ctk.CTkLabel(self.machine_info_frame, textvariable=self.machine_name, font=ctk.CTkFont(size=15, weight="bold"))
        self.machine_details_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        self.machine_hostname = "Test Machine"
        self.machine_status = "Unknown"
        self.machine_ip = "192.168.1.1"

        self.machine_details = ctk.StringVar(value=f"Hostname: {self.machine_hostname},   Status: {self.machine_status},   IP Address: {self.machine_ip}")
        self.machine_details_label = ctk.CTkLabel(self.machine_info_frame, textvariable=self.machine_details)
        self.machine_details_label.pack(anchor="w", side="bottom", pady=5, padx=(10, 5))

        self.edit_machine_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.edit_machine_frame.pack(anchor="e", side="right", expand=True)

        self.edit_machine_button = ctk.CTkButton(self.edit_machine_frame, text="Edit Machine")
        self.edit_machine_button.pack(anchor="e", side="top", padx=(0, 5), pady=5)

        self.remove_machine_button = ctk.CTkButton(self.edit_machine_frame, text="Remove Machine", fg_color="#8c031e")
        self.remove_machine_button.pack(anchor="e", side="bottom", padx=(0, 5), pady=5)