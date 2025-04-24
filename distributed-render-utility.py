import os
import re
import time
import threading
import socket
import paramiko
import json
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox

class WolSshRenderUtility:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Render Utility")
        self.root.geometry("1280x720")
        
        # Initialize variables
        self.machines = []
        self.render_logs = {}
        self.load_config()
        
        # Create and configure the UI
        self.create_ui()
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
                    self.machines = config.get("machines", [])
        except Exception as e:
            print(f"Error loading config: {e}")
            self.machines = []

    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open("config.json", "w") as f:
                json.dump({"machines": self.machines}, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def create_ui(self):
        """Create the main user interface"""
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Main content
        self.root.grid_rowconfigure(2, weight=0)  # Footer
        
        # Create frames
        self.create_header_frame()
        self.create_main_frame()
        self.create_footer_frame()
        
        # Update the machine list
        self.update_machine_list()

    def create_header_frame(self):
        """Create the header frame with title and buttons"""
        header_frame = ctk.CTkFrame(self.root)
        header_frame.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="ew")
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Distributed Render Utility", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=5, pady=5)
        
        # Add machine button
        add_button = ctk.CTkButton(
            header_frame, 
            text="Add Machine", 
            command=self.add_machine_dialog
        )
        add_button.pack(side="right", padx=5, pady=5)

    def create_main_frame(self):
        """Create the main frame with machines list and details panel"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")
        
        # Configure grid layout for the main frame
        main_frame.grid_columnconfigure(0, minsize=600, weight=0)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Create left pane (machine list)
        self.left_frame = ctk.CTkFrame(main_frame)
        self.left_frame.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")
        
        # Machine list header
        list_header = ctk.CTkFrame(self.left_frame)
        list_header.pack(fill="x", padx=5, pady=5)
        
        machines_label = ctk.CTkLabel(
            list_header, 
            text="Render Machines", 
            font=ctk.CTkFont(weight="bold")
        )
        machines_label.pack(side="left", padx=10, pady=5)
        
        # Create the machine list scrollable frame
        self.machine_list_frame = ctk.CTkScrollableFrame(self.left_frame)
        self.machine_list_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Create right pane (details and logs)
        self.right_frame = ctk.CTkFrame(main_frame)
        self.right_frame.grid(row=0, column=1, pady=0, sticky="nsew")
        
        # Machine details section
        self.details_frame = ctk.CTkFrame(self.right_frame)
        self.details_frame.pack(fill="x", padx=5, pady=5)
        
        self.machine_name_var = ctk.StringVar(value="Select a machine")
        machine_name_label = ctk.CTkLabel(
            self.details_frame,
            textvariable=self.machine_name_var,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        machine_name_label.pack(anchor="w", padx=10, pady=5)
        
        # Machine status and details
        self.machine_details_var = ctk.StringVar(value="")
        machine_details_label = ctk.CTkLabel(
            self.details_frame,
            textvariable=self.machine_details_var,
            anchor="w",
            compound="left",
        )
        machine_details_label.pack(anchor="w", padx=10, pady=5)
        
        # Control buttons
        controls_frame = ctk.CTkFrame(self.right_frame)
        controls_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.wake_button = ctk.CTkButton(
            controls_frame, 
            text="Wake Up", 
            command=self.wake_selected_machine,
            state="disabled"
        )
        self.wake_button.pack(side="left", padx=(5, 0), pady=5)
        
        self.start_render_button = ctk.CTkButton(
            controls_frame, 
            text="Start Render", 
            command=self.start_render_on_selected,
            state="disabled"
        )
        self.start_render_button.pack(side="left", padx=(5, 0), pady=5)
        self.stop_render_button = ctk.CTkButton(
            controls_frame, 
            text="Stop Render", 
            command=self.stop_render_on_selected,
            state="disabled",
            fg_color="#8c031e"
        )
        self.stop_render_button.pack(side="left", padx=(5, 0), pady=5)
        
        self.edit_button = ctk.CTkButton(
            controls_frame, 
            text="Edit", 
            command=self.edit_selected_machine,
            state="disabled"
        )
        self.edit_button.pack(side="right", padx=(0, 5), pady=5)
        
        self.remove_button = ctk.CTkButton(
            controls_frame, 
            text="Remove", 
            command=self.remove_selected_machine,
            state="disabled",
            fg_color="#8c031e"
        )
        self.remove_button.pack(side="right", padx=(0, 5), pady=5)
        
        # Log display
        log_label = ctk.CTkLabel(
            self.right_frame, 
            text="Render Log", 
            font=ctk.CTkFont(weight="bold")
        )
        log_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.log_text = ctk.CTkTextbox(self.right_frame)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.log_text.configure(state="disabled")

    def create_footer_frame(self):
        """Create the footer frame with render settings"""
        footer_frame = ctk.CTkFrame(self.root)
        footer_frame.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")
        
        # Blender file path
        blender_frame = ctk.CTkFrame(footer_frame)
        blender_frame.pack(fill="x", padx=5, pady=5)
        
        blender_label = ctk.CTkLabel(blender_frame, text="Blender File:")
        blender_label.pack(side="left", padx=10, pady=5)
        
        self.blender_path_var = ctk.StringVar(value="Y:/Automated Rendering Test/Test.blend")
        blender_path_entry = ctk.CTkEntry(
            blender_frame,
            textvariable=self.blender_path_var
        )
        blender_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        browse_button = ctk.CTkButton(
            blender_frame, 
            text="Browse", 
            command=self.browse_blender_file
        )
        browse_button.pack(side="left", padx=(0, 5), pady=5)

        # Blender file path
        render_args_frame = ctk.CTkFrame(footer_frame)
        render_args_frame.pack(fill="x", padx=5, pady=5)

        render_args_label = ctk.CTkLabel(render_args_frame, text="Render Arguments:")
        render_args_label.pack(side="left", padx=10, pady=5)

        self.render_args = ctk.StringVar(value="-F PNG -f 1")
        blender_path_entry = ctk.CTkEntry(
            render_args_frame,
            textvariable=self.render_args
        )
        blender_path_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        # Wake and render all button
        wake_render_button = ctk.CTkButton(
            footer_frame, 
            text="Wake & Render All", 
            command=self.wake_and_render_all,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        wake_render_button.pack(padx=10, pady=(5, 10), fill="x")

    def update_machine_list(self):
        """Update the machine list in the UI"""
        # Clear existing machine list items
        for widget in self.machine_list_frame.winfo_children():
            widget.destroy()
        
        
        # Add machine items to the list
        self.machine_buttons = []
        for idx, machine in enumerate(self.machines):
            machine_frame = ctk.CTkFrame(self.machine_list_frame)
            machine_frame.pack(fill="x", padx=5, pady=2)
            
            # Determine status indicator color
            status_color = "#3a3a3a"  # Default gray for unknown
            status_text = "Unknown"
            if machine.get("status") == "online":
                status_color = "#4CAF50"  # Green for online
                status_text = "Online"
            elif machine.get("status") == "offline":
                status_color = "#F44336"  # Red for offline
                status_text = "Offline"
            elif machine.get("status") == "rendering":
                status_color = "#2196F3"  # Blue for rendering
                status_text = "Rendering"

            # In the update_machine_list method, add a progress indicator for rendering machines
            if machine.get("status") == "rendering":
                # Existing code
                status_label = ctk.CTkLabel(
                    machine_frame,
                    text="Rendering",
                    width=70
                )
                status_label.pack(side="right", padx=5, pady=5)
                
                # Add a progress indicator (You could use a determinate progress bar when you have actual progress data)
                progress_bar = ctk.CTkProgressBar(machine_frame, width=100)
                progress_bar.pack(side="right", padx=5, pady=5)
                progress_bar.configure(mode="determinate",require_redraw=True)
                progress_value = machine.get("progress", 0) / 100
                progress_bar.set(progress_value)
                machine["progress_bar"] = progress_bar
            
            status_indicator = ctk.CTkLabel(
                machine_frame, 
                text="",
                width=15,
                fg_color=status_color,
                corner_radius=5
            )
            status_indicator.pack(side="left", padx=5, pady=5)
            
            machine_button = ctk.CTkButton(
                machine_frame,
                text=machine.get("display_name", f"Machine {idx+1}"),
                fg_color="transparent",
                hover_color="#2a2a2a",
                anchor="w",
                command=lambda m=machine: self.select_machine(m)
            )
            machine_button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            self.machine_buttons.append(machine_button)
            
            status_label = ctk.CTkLabel(
                machine_frame,
                text=status_text,
                width=70
            )
            status_label.pack(side="right", padx=5, pady=5)

    def add_machine_dialog(self):
        """Show dialog to add a new machine"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Machine")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Form fields
        ctk.CTkLabel(dialog, text="Display Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        display_name_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=display_name_var, width=250).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(dialog, text="Client Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=name_var, width=250).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="IP Address:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ip_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=ip_var, width=250).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="MAC Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        mac_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=mac_var, width=250).grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="SSH Username:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        username_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=username_var, width=250).grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="SSH Password:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        password_var = ctk.StringVar()
        password_entry = ctk.CTkEntry(dialog, textvariable=password_var, width=250, show="*")
        password_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        def validate_and_save():
            # Validate inputs
            display_name = display_name_var.get().strip()
            name = name_var.get().strip()
            ip = ip_var.get().strip()
            mac = mac_var.get().strip()
            username = username_var.get().strip()
            password = password_var.get()
            
            # Simple validation
            if not display_name or not name or not ip or not mac or not username or not password:
                messagebox.showerror("Error", "All fields are required", parent=dialog)
                return
            
            # Validate MAC address format
            if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
                messagebox.showerror("Error", "Invalid MAC address format. Use format like 00:11:22:33:44:55", parent=dialog)
                return
            
            # Validate IP address format
            try:
                socket.inet_aton(ip)
            except socket.error:
                messagebox.showerror("Error", "Invalid IP address", parent=dialog)
                return
            
            # Add the machine
            new_machine = {
                "display_name": display_name,
                "name": name,
                "ip": ip,
                "mac": mac,
                "username": username,
                "password": password,
                "status": "offline"
            }
            
            self.machines.append(new_machine)
            self.save_config()
            self.update_machine_list()
            dialog.destroy()
        
        ctk.CTkButton(
            buttons_frame,
            text="Save",
            command=validate_and_save
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)

    def edit_selected_machine(self):
        """Edit the currently selected machine"""
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if not selected_machine:
            return
        
        idx = self.machines.index(selected_machine)
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"Edit {selected_machine.get('name', 'Machine')}")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make it modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Form fields
        ctk.CTkLabel(dialog, text="Client Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        display_name_var = ctk.StringVar(value=selected_machine.get("name", ""))
        ctk.CTkEntry(dialog, textvariable=display_name_var, width=250).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(dialog, text="Client Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_var = ctk.StringVar(value=selected_machine.get("name", ""))
        ctk.CTkEntry(dialog, textvariable=name_var, width=250).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="IP Address:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ip_var = ctk.StringVar(value=selected_machine.get("ip", ""))
        ctk.CTkEntry(dialog, textvariable=ip_var, width=250).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="MAC Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        mac_var = ctk.StringVar(value=selected_machine.get("mac", ""))
        ctk.CTkEntry(dialog, textvariable=mac_var, width=250).grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="SSH Username:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        username_var = ctk.StringVar(value=selected_machine.get("username", ""))
        ctk.CTkEntry(dialog, textvariable=username_var, width=250).grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(dialog, text="SSH Password:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        password_var = ctk.StringVar(value=selected_machine.get("password", ""))
        password_entry = ctk.CTkEntry(dialog, textvariable=password_var, width=250, show="*")
        password_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        def validate_and_update():
            # Validate inputs
            display_name = display_name_var.get().strip()
            name = name_var.get().strip()
            ip = ip_var.get().strip()
            mac = mac_var.get().strip()
            username = username_var.get().strip()
            password = password_var.get()
            
            # Simple validation
            if not display_name or not name or not ip or not mac or not username or not password:
                messagebox.showerror("Error", "All fields are required", parent=dialog)
                return
            
            # Validate MAC address format
            if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
                messagebox.showerror("Error", "Invalid MAC address format. Use format like 00:11:22:33:44:55", parent=dialog)
                return
            
            # Validate IP address format
            try:
                socket.inet_aton(ip)
            except socket.error:
                messagebox.showerror("Error", "Invalid IP address", parent=dialog)
                return
            
            # Update the machine
            updated_machine = {
                "display_name": display_name,
                "name": name,
                "ip": ip,
                "mac": mac,
                "username": username,
                "password": password,
                "status": selected_machine.get("status", "offline"),
                "selected": True
            }
            
            self.machines[idx] = updated_machine
            self.save_config()
            self.update_machine_list()
            self.select_machine(updated_machine)
            dialog.destroy()
        
        ctk.CTkButton(
            buttons_frame,
            text="Update",
            command=validate_and_update
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)

    def remove_selected_machine(self):
        """Remove the currently selected machine"""
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if not selected_machine:
            return
        
        if messagebox.askyesno("Confirm", f"Remove machine '{selected_machine.get('name')}'?"):
            # Close any active SSH client
            if selected_machine.get("ssh_client"):
                try:
                    selected_machine["ssh_client"].close()
                except:
                    pass
                    
            self.machines.remove(selected_machine)
            self.save_config()
            self.update_machine_list()
            self.machine_name_var.set("Select a machine")
            self.machine_details_var.set("")
            self.wake_button.configure(state="disabled")
            self.start_render_button.configure(state="disabled")
            self.stop_render_button.configure(state="disabled")
            self.edit_button.configure(state="disabled")
            self.remove_button.configure(state="disabled")
    
    def select_machine(self, machine):
        """Select a machine from the list"""
        # Deselect all machines
        for m in self.machines:
            m["selected"] = False
        
        # Select the machine
        machine["selected"] = True
        
        # Update the UI
        self.machine_name_var.set(machine.get("name", "Machine"))
        
        details = f"HostName: {machine.get('name', 'N/A')}     "
        details += f"IP: {machine.get('ip', 'N/A')}     "
        details += f"MAC: {machine.get('mac', 'N/A')}     "
        details += f"Status: {machine.get('status', 'Unknown').capitalize()}"
        
        self.machine_details_var.set(details)
        
        # Enable buttons
        self.wake_button.configure(state="normal")
        self.start_render_button.configure(state="normal")
        self.stop_render_button.configure(state="normal")
        self.edit_button.configure(state="normal")
        self.remove_button.configure(state="normal")
        
        # Update the log display
        self.update_log_display(machine)
    
    def update_log_display(self, machine):
        """Update the log display for the selected machine"""
        machine_id = machine.get("name")
        
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        
        if machine_id in self.render_logs:
            self.log_text.insert("1.0", self.render_logs[machine_id])
        else:
            self.log_text.insert("1.0", "No logs available for this machine.")

        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def wake_and_render_all(self):
        for machine in self.machines:
            threading.Thread(target=self.wake_and_render_machine, args=(machine,), daemon=True).start()

    def wake_and_render_machine(self, machine):
        self.wake_machine(machine)
        time.sleep(5)  # Give a bit more time after wake before checking status
        if machine.get("status") == "online":
            blender_file = self.blender_path_var.get()
            if blender_file:
                self.start_render(machine, blender_file)

    def wake_selected_machine(self):
        """Wake the selected machine using Wake-on-LAN"""
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if not selected_machine:
            return
        
        threading.Thread(target=self.wake_machine, args=(selected_machine,)).start()
    
    def wake_machine(self, machine):
        """Send Wake-on-LAN magic packet to the specified machine"""
        try:
            self.add_log(machine.get("name"), f"Attempting to wake {machine.get('name')}...")
            
            # Parse the MAC address
            mac = machine.get("mac", "").replace(":", "").replace("-", "")
            if len(mac) != 12:
                raise ValueError("Invalid MAC address length")
            
            # Create the magic packet
            magic_packet = b'\xff' * 6 + bytes.fromhex(mac) * 16
            
            # Send the magic packet
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('<broadcast>', 9))
            sock.close()
            
            self.add_log(machine.get("name"), f"Wake-on-LAN packet sent to {machine.get('name')}.")
            
            # Wait for machine to boot
            self.add_log(machine.get("name"), "Waiting for machine to boot up...")
            
            # Try to ping the machine to check if it's online
            def check_online():
                for _ in range(30):  # Try for 30 attempts (30 * 2 = 60 seconds)
                    try:
                        with socket.create_connection((machine.get("ip"), 22), timeout=2):
                            return True
                    except (socket.timeout, ConnectionRefusedError, OSError):
                        time.sleep(2)
                return False
            
            if check_online():
                self.add_log(machine.get("name"), f"{machine.get('name')} is now online!")
                machine["status"] = "online"
            else:
                self.add_log(machine.get("name"), f"Could not connect to {machine.get('name')} after wake-up.")
                machine["status"] = "offline"
            
            # Update the UI
            self.root.after(0, self.update_machine_list)
            if machine.get("selected", False):
                self.root.after(0, lambda: self.select_machine(machine))
                
        except Exception as e:
            self.add_log(machine.get("name"), f"Error waking machine: {str(e)}")
    
    def start_render_on_selected(self):
        """Start rendering on the selected machine"""
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if not selected_machine:
            return
        
        blender_file = self.blender_path_var.get()
        if not blender_file:
            messagebox.showerror("Error", "No Blender file selected")
            return
        
        threading.Thread(target=self.start_render, args=(selected_machine, blender_file)).start()
    
    def stop_render_on_selected(self):
        """Start rendering on the selected machine"""
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if not selected_machine:
            return
        
        blender_file = self.blender_path_var.get()
        if not blender_file:
            messagebox.showerror("Error", "No Blender file selected")
            return
        
        threading.Thread(target=self.stop_render, args=(selected_machine,)).start()
    
    def start_render(self, machine, blender_file):
        """Start Blender rendering on the specified machine via SSH"""
        try:
            self.add_log(machine.get("name"), f"Connecting to {machine.get('name')} via SSH...")

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                machine.get("ip"),
                port=22,
                username=machine.get("username"),
                password=machine.get("password"),
                timeout=10
            )

            self.add_log(machine.get("name"), "SSH connection established.")
            machine["status"] = "online"
            self.root.after(0, self.update_machine_list)

            # Hardcoded mapping info
            share_path = r"\\RT-SHAREDSTORAG\VR-Warriors"
            mapped_file_path = blender_file.replace(share_path, "Y:")
            map_cmd = f'net use Y: {share_path} /user:Admin 123456 && echo DriveMapped'
            stdin, stdout, stderr = client.exec_command(map_cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()

            render_args = self.render_args.get().strip()

            # self.add_log(machine.get("name"), f"Drive mapping output: {output}")
            if error.strip():
                self.add_log(machine.get("name"), f"Drive mapping error: {error}")

            # Check for success
            if "DriveMapped" in output:
                self.add_log(machine.get("name"), "Drive mapped successfully.")
                render_cmd = f'blender -b "{mapped_file_path}" -o "//render/frame_###" {render_args}'
            else:
                self.add_log(machine.get("name"), "Drive mapping failed.")

            # Write render command to background and log output
            self.add_log(machine.get("name"), "Starting Blender render process...")
            render_cmd_bg = f'{render_cmd} > blender_render.log 2>&1'
            stdin, stdout, stderr = client.exec_command(render_cmd_bg)

            
            self.add_log(machine.get("name"), "Blender render started in background.")
            machine["status"] = "rendering"
            machine["ssh_client"] = client

            # Start monitor thread
            threading.Thread(
                target=self.monitor_render_progress,
                args=(machine,),
                daemon=True
            ).start()

            threading.Thread(
                target=self.monitor_render_process_id,
                args=(machine,),
                daemon=True
            ).start()

        except Exception as e:
            self.add_log(machine.get("name"), f"SSH or render error: {str(e)}")
            machine["status"] = "error"
            if 'client' in locals() and client:
                client.close()

        # UI Refresh
        self.root.after(0, self.update_machine_list)
        if machine.get("selected", False):
            self.root.after(0, lambda: self.select_machine(machine))

    def add_log(self, machine_name, message):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {message}\n"
        if machine_name not in self.render_logs:
            self.render_logs[machine_name] = ""
        self.render_logs[machine_name] += line

        # Update log display if selected
        selected_machine = next((m for m in self.machines if m.get("selected", False)), None)
        if selected_machine and selected_machine.get("name") == machine_name:
            self.update_log_display(selected_machine)

    def stop_render(self, machine):
        """Stop the render process on the specified machine"""
        try:
            client = machine.get("ssh_client")
            if not client:
                self.add_log(machine.get("name"), "Error: No SSH client available to stop render")
                return
            
            # Stop the render process
            pid = machine.get("render_pid")
            if pid:
                client.exec_command(f"taskkill /PID {pid} /F")
                machine["status"] = "online"
                self.update_machine_list()
                self.add_log(machine.get("name"), f"Render process {pid} stopped.")
            else:
                self.add_log(machine.get("name"), "No render process ID found.")
            
            # Close the SSH connection
            client.close()
            machine["ssh_client"] = None
        except Exception as e:
            self.add_log(machine.get("name"), f"Error stopping render: {str(e)}")

    def monitor_render_progress(self, machine):
        """Monitor render progress by checking the log file periodically"""
        try:
            # Get the client from the machine object
            client = machine.get("ssh_client")
            if not client:
                self.add_log(machine.get("name"), "Error: No SSH client available for monitoring")
                return
                
            # Wait a moment for the render to start
            time.sleep(1)
            
            # Poll the log file every 5 seconds
            while machine.get("status") == "rendering":
                try:

                    stdin, stdout, stderr = client.exec_command("type blender_render.log")  # Windows command
                    log_content = stdout.read().decode()

                    empty_log_counter = 0
                    while machine.get("status") == "rendering":
                        stdin, stdout, stderr = client.exec_command("type blender_render.log")
                        log_content = stdout.read().decode()

                        if not log_content.strip():
                            empty_log_counter += 1
                            if empty_log_counter >= 3:
                                self.add_log(machine.get("name"), "No render log found. Assuming render failed.")
                                machine["status"] = "error"
                                self.root.after(0, self.update_machine_list)
                                break
                        else:
                            empty_log_counter = 0

                        # Check for progress indicators in the log
                        progress_matches = re.findall(r'Fra:(\d+) .*? \| Sample (\d+)/(\d+)', log_content)
                        if progress_matches:
                            frame, current_tile, total_tiles = progress_matches[-1]
                            progress = int(float(current_tile) / float(total_tiles) * 100)
                            machine["progress"] = progress
                            machine["frame"] = frame
                            machine["progress_bar"].set(progress / 100)
                        
                        # Check if render is complete
                        if "Blender quit" in log_content or "Rendering completed" in log_content:
                            self.add_log(machine.get("name"), "Render completed!")
                            machine["status"] = "online"
                            self.root.after(0, self.update_machine_list)
                            if machine.get("selected", False):
                                self.root.after(0, lambda: self.select_machine(machine))
                            break
                except Exception as e:
                    self.add_log(machine.get("name"), f"Error reading log: {str(e)}")
                    break
                    
                time.sleep(1)
        except Exception as e:
            self.add_log(machine.get("name"), f"Error monitoring render: {str(e)}")
        finally:
            # Ensure we close the client when done
            try:
                if machine.get("ssh_client"):
                    stdin, stdout, stderr = client.exec_command("net use Y: /delete")
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    self.add_log(machine.get("name"), f"Drive: {output}")

                    self.add_log(machine.get("name"), "Closing SSH connection.")
                    machine["ssh_client"].close()
                    machine["ssh_client"] = None
            except:
                pass
   
    def monitor_render_process_id(self, machine):
        """Monitor the render process ID on the remote machine"""
        try:
            client = machine.get("ssh_client")
            if not client:
                self.add_log(machine.get("name"), "Error: No SSH client available for monitoring")
                return
            
            # Get the process ID of the Blender render
            stdin, stdout, stderr = client.exec_command("tasklist | findstr blender.exe")
            output = stdout.read().decode()

            final_pid = output.split()[1] if output else None
            if final_pid:
                machine["render_pid"] = final_pid
                self.add_log(machine.get("name"), f"Render process ID: {final_pid}")
            else:
                self.add_log(machine.get("name"), "No render process found.")

            if "blender.exe" in output:
                self.add_log(machine.get("name"), "Render process is running.")
            else:
                self.add_log(machine.get("name"), "Render process not found.")
        except Exception as e:
            self.add_log(machine.get("name"), f"Error monitoring render process: {str(e)}")
        
    def browse_blender_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Blender Files", "*.blend")],
            title="Select Blender File"
        )
        if file_path:
            self.blender_path_var.set(file_path)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = WolSshRenderUtility(root)
    root.mainloop()
