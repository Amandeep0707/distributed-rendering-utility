import customtkinter as ctk

class Footer(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master, border_width=0)
        self.frame.pack(padx=5, pady=(0, 5), anchor="s", fill="x")

        self.blender_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=0)
        self.blender_frame.pack(fill="x", expand=True)

        self.output_path_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=0)
        self.output_path_frame.pack(fill="x", expand=True)

        self.render_args_frame = ctk.CTkFrame(self.frame, fg_color="transparent", border_width=0)
        self.render_args_frame.pack(fill="x", expand=True)

        self.blender_label = ctk.CTkLabel(self.blender_frame, text="Browse File:")
        self.blender_label.pack(side="left", padx=10, pady=5)

        drive_path = self.app.drive_credentials.get("path")
        self.blender_path_field = ctk.StringVar(value=f"{drive_path}\Automated Rendering Test\Test.blend")
        self.blender_path_entry = ctk.CTkEntry(self.blender_frame, textvariable=self.blender_path_field, width=300)
        self.blender_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.browse_button = ctk.CTkButton(self.blender_frame, text="Browse", command=lambda: self.on_input_browse(self.blender_path_field))
        self.browse_button.pack(side="left", padx=(0, 5), pady=5)

        self.output_path_label = ctk.CTkLabel(self.output_path_frame, text="Output Path:")
        self.output_path_label.pack(side="left", padx=10, pady=5)

        self.output_path_field = ctk.StringVar(value="//Output/Frame ###")
        self.output_path_entry = ctk.CTkEntry(self.output_path_frame, textvariable=self.output_path_field, width=300)
        self.output_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.output_browse_button = ctk.CTkButton(self.output_path_frame, text="Browse", command=lambda: self.on_output_browse(self.output_path_field))
        self.output_browse_button.pack(side="left", padx=(0, 5), pady=5)

        self.render_args_label = ctk.CTkLabel(self.render_args_frame, text="Render Arguments:")
        self.render_args_label.pack(side="left", padx=10, pady=5)

        self.render_args_field = ctk.StringVar(value="-s 1 -e 2 -a -F PNG --engine CYCLES")
        self.render_args_entry = ctk.CTkEntry(self.render_args_frame, textvariable=self.render_args_field)
        self.render_args_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand="true")

        self.render_options_button = ctk.CTkButton(self.render_args_frame, text="Render Options", command=lambda: self.on_render_options())
        self.render_options_button.pack(side="left", padx=(0, 5), pady=5)

        self.render_all_button = ctk.CTkButton(self.frame, height=40, font=ctk.CTkFont(size=15, weight="bold"), text="Render(All Available Nodes)", command=lambda: self.app.render_manager.render_all(), border_width=0)
        self.render_all_button.pack(fill="x", padx=5, pady=5)

    def on_input_browse(self, callback):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Blender Files", "*.blend")])
        if file_path:
            if file_path.startswith("Y:"):
                drive_path = self.app.drive_credentials.get("path")
                file_path = file_path.replace("Y:", drive_path)
                file_path = file_path.replace("/", "\\")
            callback.set(file_path)
            self.blender_path_entry.configure(state="normal")

    def on_output_browse(self, callback):
        file_path  = ctk.filedialog.askdirectory()
        if file_path:
            callback.set(file_path)
            self.output_path_entry.configure(state="normal")

    def on_render_options(self):
        # Placeholder for render options dialog
        dialog = ctk.CTkToplevel(self.app.root)
        dialog.title("Render Options")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.update_idletasks()

        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")

        # Form Fields
        ctk.CTkLabel(dialog, text="Render Options", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="n", columnspan=2)

        ctk.CTkLabel(dialog, text="Range Start:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.range_start_var = ctk.StringVar(value="1")
        ctk.CTkEntry(dialog, textvariable=self.range_start_var, width=200).grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(dialog, text="Range End:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.range_end_var = ctk.StringVar(value="2")
        ctk.CTkEntry(dialog, textvariable=self.range_end_var, width=200).grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(dialog, text="Render Engine:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.render_engine_var = ctk.StringVar(value="CYCLES")
        ctk.CTkOptionMenu(dialog, variable=self.render_engine_var, values=["BLENDER_EEVEE_NEXT", "CYCLES", "BLENDER_WORKBENCH"], command=lambda x: self.render_engine_var.set(x)).grid(row=3, column=1, padx=10, pady=5, sticky="e")

        ctk.CTkLabel(dialog, text="Output Format:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.output_format_var = ctk.StringVar(value="PNG")
        ctk.CTkOptionMenu(dialog, variable=self.output_format_var, values=["JPEG", "PNG", "Webp"], command=lambda x: self.output_format_var.set(x)).grid(row=4, column=1, padx=10, pady=5, sticky="e")

        def checkbox_event():
            if check_var.get() == "on":
                self.app.render_manager.suppress_render_errors = True
            else:
                self.app.render_manager.suppress_render_errors = False

        ctk.CTkLabel(dialog, text="Suppress Render Logs").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        check_var = ctk.StringVar(value="on")
        ctk.CTkCheckBox(dialog, text=None, variable=check_var, onvalue="on", offvalue="off", command=checkbox_event).grid(row=5, column=1, padx=10, pady=5, sticky="w")

        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent", border_width=0)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)

        def generate_command():
            # Placeholder for command generation logic
            command = f'-s {self.range_start_var.get()} -e {self.range_end_var.get()} -a -F {self.output_format_var.get()} --engine {self.render_engine_var.get()}'
            self.render_args_field.set(command)
            dialog.destroy()

        ctk.CTkButton(
            buttons_frame, 
            text="Generate Command",
            command=generate_command
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame, 
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
