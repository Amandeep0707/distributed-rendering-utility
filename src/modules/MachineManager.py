import re
import time
import threading
import socket
import customtkinter as ctk
from tkinter import messagebox

class MachineManager:
    def __init__(self, app):
        self.app = app
        self.log_manager = app.log_manager
        threading.Thread(target=self.check_all_machines, args=(), daemon=True).start()

    def add_machine(self):
        self.dialog = ctk.CTkToplevel(self.app.root)
        self.dialog.title("Add Machine")
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

        def validate_and_save(self):
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

        ctk.CTkButton(
            self.buttons_frame, 
            text="Save", 
            command=lambda: validate_and_save(self),
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Cancel", 
            command=self.dialog.destroy
        ).pack(side="left", padx=10)

    def edit_machine(self, machine):
        if not machine:
            messagebox.showerror("Error", "No machine selected.", parent=self.app.root)
            return
        
        machine_index = self.app.machines.index(machine)

        self.dialog = ctk.CTkToplevel(self.app.root)
        self.dialog.title("Add Machine")
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
        self.display_name_var = ctk.StringVar(value=machine.get("display_name", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.display_name_var, width=250).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.dialog, text="Client Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_var = ctk.StringVar(value=machine.get("name", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.name_var, width=250).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="IP Address:").grid(row=2, column=0, padx=10, pady=5)
        self.ip_var = ctk.StringVar(value=machine.get("ip", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.ip_var, width=250).grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="MAC Address:").grid(row=3, column=0, padx=10, pady=5)
        self.mac_var = ctk.StringVar(value=machine.get("mac", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.mac_var, width=250).grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Username:").grid(row=4, column=0, padx=10, pady=5)
        self.username_var = ctk.StringVar(value=machine.get("username", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.username_var, width=250).grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Password:").grid(row=5, column=0, padx=10, pady=5)
        self.password_var = ctk.StringVar(value=machine.get("password", ""))
        password_entry = ctk.CTkEntry(self.dialog, textvariable=self.password_var, width=250, show="*")
        password_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        self.buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)

        def validate_and_save(self):
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
            
            # Update the machine
            self.updated_machine = {
                "display_name": self.display_name,
                "name": self.name,
                "ip": self.ip,
                "mac": self.mac,
                "username": self.username,
                "password": self.password,
                "status": machine.get("status", "offline"),
                "selected": True
            }

            self.app.machines[machine_index] = self.updated_machine
            self.app.config_manager.save_config(self.app.machines)
            self.app.machine_list.update_list(self.app.machines)
            self.dialog.destroy()

        ctk.CTkButton(
            self.buttons_frame, 
            text="Save", 
            command=lambda: validate_and_save(self),
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Cancel", 
            command=self.dialog.destroy
        ).pack(side="left", padx=10)

    def remove_machine(self, machine):
        if not machine:
            messagebox.showerror("Error", "No machine selected.", parent=self.app.root)
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this machine?", parent=self.app.root):
            
            self.app.machines.remove(machine)
            self.app.config_manager.save_config(self.app.machines)
            self.app.machine_list.update_list(self.app.machines)
            self.app.machine_details.initialize_details()

    def wake_machine(self, machine):
        if not machine:
            messagebox.showerror("Error", "No machine selected.", parent=self.app.root)
            return
        
        if machine.get("status") == "online":
            messagebox.showinfo("Info", "Machine is already online.", parent=self.app.root)
            return
        
        threading.Thread(target=self.wake, args=(machine,), daemon=True).start()

    def wake(self, machine):
        try:
            self.log_manager.log(machine, "Trying to Wakeup up machine...")

            mac = machine.get("mac").replace(":", "").replace("-", "").upper()
            if len(mac) != 12:
                raise ValueError("Invalid MAC address format.")
            
            # Create magic packet
            magic_packet = b'\xff' * 6 + bytes.fromhex(mac) * 16

            # Sens the Magic Packet to the broadcast address
            broadcast_address = ('<broadcast>', 9)  # Port 9 is the default for Wake-on-LAN
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, broadcast_address)
            sock.close()
            self.log_manager.log(machine, "Magic packet sent successfully.")
            self.log_manager.log(machine, "Waiting for machine to boot up...")

            def check_online():
                for _ in range(30):
                    try:
                        with socket.create_connection((machine.get("ip"), 22), timeout=2):
                            return True
                    except (socket.timeout, ConnectionRefusedError, OSError):
                        time.sleep(2)
                    return False
                    
            def check_online():
                for attempt in range(30):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)  # Short timeout
                        result = sock.connect_ex((machine.get("ip"), 22))
                        sock.close()
                        
                        if result == 0:
                            return True
                        
                        self.log_manager.log(machine, f"Waiting for machine to respond... ({attempt+1}/{30})")
                        time.sleep(2)
                    except Exception as e:
                        self.log_manager.log(machine, f"Connection attempt failed: {e}")
                        time.sleep(2)
                return False
                    
            if check_online():
                self.log_manager.log(machine, "Machine is now online.")
                machine["status"] = "online"
            else:
                self.log_manager.log(machine, "Machine did not respond within timeout period.")
                machine["status"] = "offline"

            # self.app.config_manager.save_config(self.app.machines)
            self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
        
        except Exception as e:
            self.log_manager.log(machine, f"Error waking machine: {str(e)}")

    def check_all_machines(self):
        """
        Check the status of all machines in the list.
        This is run in a separate thread to avoid blocking the main thread.
        """
        try:
            for machine in self.app.machines:
                try:
                    # Create a socket and set a shorter timeout
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)  # 1 second timeout
                    
                    result = sock.connect_ex((machine.get("ip"), 22))
                    sock.close()
                    
                    # If result is 0, connection was successful
                    if result == 0:
                        machine["status"] = "online"
                        self.log_manager.log(machine, f"Machine status: online", False)
                    else:
                        machine["status"] = "offline"
                        self.log_manager.log(machine, f"Machine status: offline (connection failed)", False)
                except Exception as e:
                    machine["status"] = "unknown"
                    self.log_manager.log(machine, f"Error checking machine status: {str(e)}", False)

            # Update the UI from the main thread
            self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
            # self.app.config_manager.save_config(self.app.machines)
        except Exception as e:
            print(f"Error in check_all_machines: {e}")
            # We're in a thread, so we need to use after to schedule UI updates
            self.app.root.after(0, lambda: messagebox.showerror("Error", f"Error checking machine.", parent=self.app.root))