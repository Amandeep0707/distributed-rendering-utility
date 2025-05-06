import customtkinter as ctk

class Header(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master, border_width=0, corner_radius=0)
        self.frame.pack(padx=5, pady=(5, 0), anchor="n", fill="x")
        
        # Add Header title
        self.title_label = ctk.CTkLabel(self.frame, text="Render Utility", font=ctk.CTkFont(size=20, weight="bold"), height=40)
        self.title_label.pack(side="left", pady=5, padx=(10, 5))

        # Add Node Button
        self.add_node_button = ctk.CTkButton(
            self.frame,
            text="Add Node",
            command=lambda: self.app.node_manager.add_node()
            )
        self.add_node_button.pack(side="right", padx=5, pady=5)