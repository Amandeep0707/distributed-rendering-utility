import customtkinter as ctk

class NodeList(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master, border_width=0, corner_radius=0)
        self.frame.pack(padx=(5, 0), pady=5, anchor="w", side="left", fill="y")

        # Add Node List title
        self.title_label = ctk.CTkLabel(self.frame, text="Render Nodes", font=ctk.CTkFont(size=15, weight="bold"), height=40)
        self.title_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        # Add Node Listbox
        self.node_list_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent", width=450, border_width=0)
        self.node_list_frame.pack(fill="both", expand=True)

        self.update_list(app.nodes)

    def update_list(self, nodes):
        """
        Update the node list with the current nodes.
        This function should be called whenever the node list changes.
        """
        # Clear the current list
        for widget in self.node_list_frame.winfo_children():
            widget.destroy()

        # Add nodes to the list
        self.node_buttons = []
        for i, node in enumerate(nodes):
            node_frame = ctk.CTkFrame(self.node_list_frame)
            node_frame.pack(fill="x", padx=0, pady=5)

            # Determine status indicator color
            status_color = "#3a3a3a"  # Default gray for unknown
            status_text = "Unknown"
            if node.get("status") == "online":
                status_color = "#4CAF50"  # Green for online
                status_text = "Online"
            elif node.get("status") == "offline":
                status_color = "#F44336"  # Red for offline
                status_text = "Offline"
            elif node.get("status") == "rendering":
                status_color = "#2196F3"  # Blue for rendering
                status_text = "Rendering"
            elif node.get("status") == "error":
                status_color = "#f1dd5a"  # Yellow for Error
                status_text = "Error"
            elif node.get("status") == "unknown":
                status_color = "#202020"  # Grey for rendering
                status_text = "Unknown"

            # In the update_node_list method, add a progress indicator for rendering nodes
            if node.get("status") == "rendering":
                # Existing code
                self.status_label = ctk.CTkLabel(
                    node_frame,
                    text=f"Rendering: {node.get('current_frame', ' ')}",
                    width=70,
                )
                self.status_label.pack(side="right", padx=5, pady=5)
                node["status_label"] = self.status_label
                
                # Add a progress indicator (You could use a determinate progress bar when you have actual progress data)
                self.progress_bar = ctk.CTkProgressBar(node_frame, width=100)
                self.progress_bar.pack(side="right", padx=5, pady=5)
                self.progress_bar.configure(mode="determinate", require_redraw=True)
                self.progress_bar.set(0)
                node["progress_bar"] = self.progress_bar

            self.status_indicator = ctk.CTkLabel(
                node_frame, 
                text="",
                width=16,
                height=10,
                fg_color=status_color,
                corner_radius=20
            )
            self.status_indicator.pack(side="left", padx=(10,5), pady=5)

            node_button = ctk.CTkButton(
                node_frame,
                text=node.get("display_name", f"Node {i+1}"),
                fg_color="grey25",
                anchor="w",
                command=lambda m=node: self.app.node_details.on_node_select(m)
            )
            node_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            self.node_buttons.append(node_button)

            if not node.get("status") == "rendering":
                status_label = ctk.CTkLabel(
                    node_frame,
                    text=status_text,
                    width=70
                )
                status_label.pack(side="right", padx=5, pady=5)