import re
import socket
import customtkinter as ctk
from tkinter import messagebox

class MachineManager:
    def __init__(self, app):
        self.app = app

    def add_machine(self):
        self.dialog = ctk.CTkToplevel(self.app.root)
        self.dialog.title("Add Machine")
        # self.dialog.geometry("600x300")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")

        # Form fields
        ctk.CTkLabel(self.dialog, text="Display Name:").grid(row=0, column=0, padx=10, pady=5)
        self.display_name_var = ctk.StringVar()
        ctk.CTkEntry(self.dialog, textvariable=self.display_name_var, width=250).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.dialog, text="Client Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_var = ctk.StringVar()
        ctk.CTkEntry(self.dialog, textvariable=self.name_var, width=250).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="IP Address:").grid(row=2, column=0, padx=10, pady=5)
        self.ip_var = ctk.StringVar()
        ctk.CTkEntry(self.dialog, textvariable=self.ip_var, width=250).grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="MAC Address:").grid(row=3, column=0, padx=10, pady=5)
        self.mac_var = ctk.StringVar()
        ctk.CTkEntry(self.dialog, textvariable=self.mac_var, width=250).grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Username:").grid(row=4, column=0, padx=10, pady=5)
        self.username_var = ctk.StringVar()
        ctk.CTkEntry(self.dialog, textvariable=self.username_var, width=250).grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Password:").grid(row=5, column=0, padx=10, pady=5)
        self.password_var = ctk.StringVar()
        password_entry = ctk.CTkEntry(self.dialog, textvariable=self.password_var, width=250, show="*")
        password_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        self.buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Save", 
            command=self.validate_and_save_machine
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Cancel", 
            command=self.dialog.destroy
        ).pack(side="left", padx=10)

    def validate_and_save_machine(self):
        # Validate inputs
        self.display_name = self.display_name_var.get().strip()
        self.name = self.name_var.get().strip()
        self.ip = self.ip_var.get().strip()
        self.mac = self.mac_var.get().strip()
        self.username = self.username_var.get().strip()
        self.password = self.password_var.get()

        if not self.display_name or not self.name or not self.ip or not self.mac or not self.username or not self.password:
            messagebox.showerror("Error", "All fields are required.", parent=self.dialog)
            return
        
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', self.mac):
            messagebox.showerror("Error", "Invalid MAC address format. Use format like 00:11:22:33:44:55", parent=self.dialog)
            return
        
        try:
            socket.inet_aton(self.ip)
        except socket.error:
            messagebox.showerror("Error", "Invalid IP address format.", parent=self.dialog)
            return
        
        # Add the machine
        new_machine = {
            "display_name": self.display_name,
            "name": self.name,
            "ip": self.ip,
            "mac": self.mac,
            "username": self.username,
            "password": self.password,
            "status": "unknown",
            "selected": False,
        }

        self.app.machines.append(new_machine)
        self.app.config_manager.save_config(self.app.machines)
        self.app.machine_list.update_list(self.app.machines)
        self.app.machine_details.on_machine_select(new_machine)
        
        self.dialog.destroy()
