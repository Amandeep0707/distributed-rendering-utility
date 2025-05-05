import customtkinter as ctk

class NodeDetails(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=5, anchor="n", fill="x")
        self.main_activity_frame = None
        self.details_frame = None

        self.initialize_details()

    def initialize_details(self):

        # Destroy existing widgets in the frame and main_activity_frame
        # This is to ensure that the frame is cleared before adding new widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        if self.main_activity_frame:
            for widget in self.main_activity_frame.winfo_children():
                widget.destroy()
        if self.details_frame:
            for widget in self.details_frame.winfo_children():
                widget.destroy()

        if not self.details_frame:
            self.details_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=0)
            self.details_frame.pack(anchor="n", side="top", fill="x")

        self.node_info_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent", border_width=0)
        self.node_info_frame.pack(anchor="w", side="left", expand=True)

        self.edit_node_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent", border_width=0)
        self.edit_node_frame.pack(anchor="e", side="right", expand=True)

        if not self.main_activity_frame:
            self.main_activity_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=0)
            self.main_activity_frame.pack(anchor="s", side="bottom", fill="x")

        self.wake_button = ctk.CTkButton(self.main_activity_frame, text="Wake Node", command=lambda: self.app.node_manager.wake_node(self.app.active_node))
        self.wake_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.wake_button.configure(state="disabled")

        self.start_render_button = ctk.CTkButton(self.main_activity_frame, text="Start Render", command=lambda: self.app.render_manager.start_render(self.app.active_node))
        self.start_render_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.start_render_button.configure(state="disabled")

        self.stop_render_button = ctk.CTkButton(self.main_activity_frame, text="Stop Render", command=lambda: self.app.render_manager.stop_render(self.app.active_node))
        self.stop_render_button.pack(anchor="w", side="left", padx=(5, 0), pady=5)
        self.stop_render_button.configure(state="disabled")

        self.node_name = ctk.StringVar(value="Node Details")
        self.node_details_label = ctk.CTkLabel(self.node_info_frame, textvariable=self.node_name, font=ctk.CTkFont(size=15, weight="bold"))
        self.node_details_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        self.node_details = ctk.StringVar(value=self.prepare_node_info("Hostname", "Status", "IP Address"))
        self.node_details_label = ctk.CTkLabel(self.node_info_frame, textvariable=self.node_details)
        self.node_details_label.pack(anchor="w", side="bottom", pady=5, padx=(10, 5))

        self.edit_node_button = ctk.CTkButton(self.edit_node_frame, text="Edit Node", command=lambda: self.app.node_manager.edit_node(self.app.active_node))
        self.edit_node_button.pack(anchor="e", side="top", padx=(0, 5), pady=5)
        self.edit_node_button.configure(state="disabled")

        self.remove_node_button = ctk.CTkButton(self.edit_node_frame, text="Remove Node", command=lambda: self.app.node_manager.remove_node(self.app.active_node))
        self.remove_node_button.pack(anchor="e", side="bottom", padx=(0, 5), pady=5)
        self.remove_node_button.configure(state="disabled")

    def on_node_select(self, node):

        # Deselect all nodes
        for m in self.app.nodes:
            m["selected"] = False
        
        node["selected"] = True
        self.app.active_node = node

        self.node_name.set(node["display_name"])
        self.node_details.set(self.prepare_node_info(node["name"], node["status"], node["ip"]))

        # Enable buttons
        self.wake_button.configure(state="normal")
        self.start_render_button.configure(state="normal")
        self.stop_render_button.configure(state="normal")
        self.edit_node_button.configure(state="normal")
        self.remove_node_button.configure(state="normal")

        self.app.log_manager.change_log_display(node)

    def prepare_node_info(self, hostname="Test Node", status="Unknown", ip_address=""):
        return f"Hostname: {hostname},   Status: {status},   IP Address: {ip_address}"