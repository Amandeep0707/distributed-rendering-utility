import customtkinter as ctk

class MachineDetails(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=(5, 0), anchor="n", fill="x")

        self.machine_info_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.machine_info_frame.pack(anchor="w", side="left", expand=True)

        self.edit_machine_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.edit_machine_frame.pack(anchor="e", side="right", expand=True)

        self.main_activity_frame = ctk.CTkFrame(master)
        self.main_activity_frame.pack(padx=5, pady=5, anchor="n", side="top", fill="x")

        self.wake_button = ctk.CTkButton(self.main_activity_frame, text="Wake Node")
        self.wake_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.wake_button.configure(state="disabled")

        self.start_render_button = ctk.CTkButton(self.main_activity_frame, text="Start Render")
        self.start_render_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.start_render_button.configure(state="disabled", fg_color="#37da6d")

        self.stop_render_button = ctk.CTkButton(self.main_activity_frame, text="Stop Render", fg_color="#8c031e")
        self.stop_render_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.stop_render_button.configure(state="disabled")

        self.machine_name = ctk.StringVar(value="Machine Details")
        self.machine_details_label = ctk.CTkLabel(self.machine_info_frame, textvariable=self.machine_name, font=ctk.CTkFont(size=15, weight="bold"))
        self.machine_details_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        self.machine_details = ctk.StringVar(value=self.prepare_machine_info("Hostname", "Status", "IP Address"))
        self.machine_details_label = ctk.CTkLabel(self.machine_info_frame, textvariable=self.machine_details)
        self.machine_details_label.pack(anchor="w", side="bottom", pady=5, padx=(10, 5))

        self.edit_machine_button = ctk.CTkButton(self.edit_machine_frame, text="Edit Machine")
        self.edit_machine_button.pack(anchor="e", side="top", padx=(0, 5), pady=5)
        self.edit_machine_button.configure(state="disabled")

        self.remove_machine_button = ctk.CTkButton(self.edit_machine_frame, text="Remove Machine", fg_color="#8c031e")
        self.remove_machine_button.pack(anchor="e", side="bottom", padx=(0, 5), pady=5)
        self.remove_machine_button.configure(state="disabled")

    def on_machine_select(self, machine):

        # Deselect all machines
        for m in self.app.machines:
            m["selected"] = False
        
        machine["selected"] = True

        self.machine_name.set(machine["name"])
        self.machine_details.set(self.prepare_machine_info(machine["name"], machine["status"], machine["ip"]))

        # Enable buttons
        self.wake_button.configure(state="normal")
        self.start_render_button.configure(state="normal")
        self.stop_render_button.configure(state="normal")
        self.edit_machine_button.configure(state="normal")
        self.remove_machine_button.configure(state="normal")

        self.app.log_manager.change_log_display(machine)

    def prepare_machine_info(self, hostname="Test Machine", status="Unknown", ip_address=""):
        return f"Hostname: {hostname},   Status: {status},   IP Address: {ip_address}"