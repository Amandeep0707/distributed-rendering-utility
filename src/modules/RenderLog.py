import customtkinter as ctk
from modules.ImageViewer import ImageViewer

class RenderLog(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master, border_width=0, corner_radius=0)
        self.frame.pack(padx=5, pady=(0, 5), anchor="s",side="bottom", fill="both", expand=True)

        # Add Render Log Textbox
        self.title = "Render Log:"
        self.render_log_label = ctk.CTkLabel(self.frame, text=self.title, font=ctk.CTkFont(size=15, weight="bold"))
        self.render_log_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        self.log_text = ctk.CTkTextbox(self.frame, border_width=0)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.log_text.configure(state="disabled")

    def update_title(self):
        if not self.app.active_node["name"]: return
        
        self.title = self.app.active_node["name"]
        self.render_log_label.configure(text=f"Render Log({self.title}):")