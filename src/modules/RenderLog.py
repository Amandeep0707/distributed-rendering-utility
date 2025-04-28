import customtkinter as ctk

class RenderLog(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=(0, 5), anchor="se", fill="both", expand=True)

        # Add Render Log Textbox
        self.render_log_label = ctk.CTkLabel(self.frame, text="Render Log:", font=ctk.CTkFont(size=15, weight="bold"))
        self.render_log_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        self.log_text = ctk.CTkTextbox(self.frame)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.log_text.configure(state="disabled")