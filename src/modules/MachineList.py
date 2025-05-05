import customtkinter as ctk

class MachineList(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=(5, 0), pady=5, anchor="w", side="left", fill="y")

        # Add Machine List title
        self.title_label = ctk.CTkLabel(self.frame, text="Render Nodes", font=ctk.CTkFont(size=15, weight="bold"), height=40)
        self.title_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        # Add Machine Listbox
        self.machine_list_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent", width=450)
        self.machine_list_frame.pack(fill="both", expand=True)

        self.update_list(app.machines)

    def update_list(self, machines):
        """
        Update the machine list with the current machines.
        This function should be called whenever the machine list changes.
        """
        # Clear the current list
        for widget in self.machine_list_frame.winfo_children():
            widget.destroy()

        # Add machines to the list
        self.machine_buttons = []
        for i, machine in enumerate(machines):
            machine_frame = ctk.CTkFrame(self.machine_list_frame)
            machine_frame.pack(fill="x", padx=5, pady=2)

            # Determine status indicator color
            status_color = "#3a3a3a"  # Default gray for unknown
            status_text = "Unknown"
            if machine.get("status") == "online":
                status_color = "#4CAF50"  # Green for online
                status_text = "Online"
            elif machine.get("status") == "offline":
                status_color = "#F44336"  # Red for offline
                status_text = "Offline"
            elif machine.get("status") == "rendering":
                status_color = "#2196F3"  # Blue for rendering
                status_text = "Rendering"
            elif machine.get("status") == "error":
                status_color = "#f1dd5a"  # Yellow for Error
                status_text = "Error"
            elif machine.get("status") == "unknown":
                status_color = "#202020"  # Grey for rendering
                status_text = "Unknown"

            # In the update_machine_list method, add a progress indicator for rendering machines
            if machine.get("status") == "rendering":
                # Existing code
                self.status_label = ctk.CTkLabel(
                    machine_frame,
                    text=f"Rendering: {machine.get('current_frame', ' ')}",
                    width=70,
                )
                self.status_label.pack(side="right", padx=5, pady=5)
                machine["status_label"] = self.status_label
                
                # Add a progress indicator (You could use a determinate progress bar when you have actual progress data)
                self.progress_bar = ctk.CTkProgressBar(machine_frame, width=100)
                self.progress_bar.pack(side="right", padx=5, pady=5)
                self.progress_bar.configure(mode="determinate", require_redraw=True)
                progress_value = machine.get("progress", 0) / 100
                self.progress_bar.set(progress_value)
                machine["progress_bar"] = self.progress_bar

            self.status_indicator = ctk.CTkLabel(
                machine_frame, 
                text="",
                width=16,
                height=10,
                fg_color=status_color,
                corner_radius=20
            )
            self.status_indicator.pack(side="left", padx=5, pady=5)

            machine_button = ctk.CTkButton(
                machine_frame,
                text=machine.get("display_name", f"Machine {i+1}"),
                fg_color="transparent",
                hover_color="#505050",
                anchor="w",
                command=lambda m=machine: self.app.machine_details.on_machine_select(m)
            )
            machine_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            self.machine_buttons.append(machine_button)

            if not machine.get("status") == "rendering":
                status_label = ctk.CTkLabel(
                    machine_frame,
                    text=status_text,
                    width=70
                )
                status_label.pack(side="right", padx=5, pady=5)