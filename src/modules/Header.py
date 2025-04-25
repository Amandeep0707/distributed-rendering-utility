import customtkinter as ctk

class Header(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=(5, 0), anchor="n", fill="x")

        # Add Header title
        self.title_label = ctk.CTkLabel(self.frame, text="Render Utility", font=ctk.CTkFont(size=20, weight="bold"), height=40)
        self.title_label.pack(side="left", pady=5, padx=(10, 5))

        # Add Machine Button
        self.add_machine_button = ctk.CTkButton(
            self.frame,
            text="Add Machine"
        )
        self.add_machine_button.pack(side="right", padx=5, pady=5)