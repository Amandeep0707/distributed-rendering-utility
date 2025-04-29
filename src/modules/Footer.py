import customtkinter as ctk

class Footer(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=5, pady=(0, 5), anchor="s", fill="x")

        self.blender_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.blender_frame.pack(fill="x", expand=True)

        self.output_path_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.output_path_frame.pack(fill="x", expand=True)

        self.render_args_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.render_args_frame.pack(fill="x", expand=True)

        self.blender_label = ctk.CTkLabel(self.blender_frame, text="Browse File:")
        self.blender_label.pack(side="left", padx=10, pady=5)

        self.blender_path_field = ctk.StringVar(value="\\\\RT-SHAREDSTORAG\VR-Warriors\Automated Rendering Test\Test.blend")
        self.blender_path_entry = ctk.CTkEntry(self.blender_frame, textvariable=self.blender_path_field, width=300)
        self.blender_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.browse_button = ctk.CTkButton(self.blender_frame, text="Browse", command=lambda: self.on_browse(self.blender_path_field))
        self.browse_button.pack(side="left", padx=(0, 5), pady=5)

        self.output_path_label = ctk.CTkLabel(self.output_path_frame, text="Output Path:")
        self.output_path_label.pack(side="left", padx=10, pady=5)

        self.output_path_field = ctk.StringVar(value="//render_output/output_##")
        self.output_path_entry = ctk.CTkEntry(self.output_path_frame, textvariable=self.output_path_field, width=300)
        self.output_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.render_args_label = ctk.CTkLabel(self.render_args_frame, text="Render Arguments:")
        self.render_args_label.pack(side="left", padx=10, pady=5)

        self.render_args_field = ctk.StringVar(value="-F PNG -s 1 -e 10 -a")
        self.render_args_entry = ctk.CTkEntry(self.render_args_frame, textvariable=self.render_args_field)
        self.render_args_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.render_all_button = ctk.CTkButton(self.frame, height=40, font=ctk.CTkFont(size=15, weight="bold"), text="Render(All Available Nodes)", command=lambda: self.app.render_manager.render_all())
        self.render_all_button.pack(fill="x", padx=5, pady=5)

    def on_browse(self, callback):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Blender Files", "*.blend")])
        if file_path:
            callback.set(file_path)
            self.blender_path_entry.configure(state="normal")