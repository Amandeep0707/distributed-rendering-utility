import re
import time
import threading
import socket
import customtkinter as ctk
from tkinter import messagebox

class NodeManager:
    def __init__(self, app):
        self.app = app
        self.log_manager = app.log_manager
        threading.Thread(target=self.check_all_nodes, args=(), daemon=True).start()

    def add_node(self):
        self.dialog = ctk.CTkToplevel(self.app.root)
        self.dialog.title("Add Node")
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
        self.buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent", border_width=0)
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
            
            # Add the node
            new_node = {
                "display_name": self.display_name,
                "name": self.name,
                "ip": self.ip,
                "mac": self.mac,
                "username": self.username,
                "password": self.password,
                "status": "unknown",
                "selected": False,
            }

            self.app.nodes.append(new_node)
            self.app.config_manager.save_config(self.app.nodes)
            self.app.node_list.update_list(self.app.nodes)
            self.app.node_details.on_node_select(new_node)
            
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

    def edit_node(self, node):
        if not node:
            messagebox.showerror("Error", "No node selected.", parent=self.app.root)
            return
        
        node_index = self.app.nodes.index(node)

        self.dialog = ctk.CTkToplevel(self.app.root)
        self.dialog.title("Add Node")
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
        self.display_name_var = ctk.StringVar(value=node.get("display_name", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.display_name_var, width=250).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.dialog, text="Client Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_var = ctk.StringVar(value=node.get("name", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.name_var, width=250).grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="IP Address:").grid(row=2, column=0, padx=10, pady=5)
        self.ip_var = ctk.StringVar(value=node.get("ip", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.ip_var, width=250).grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="MAC Address:").grid(row=3, column=0, padx=10, pady=5)
        self.mac_var = ctk.StringVar(value=node.get("mac", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.mac_var, width=250).grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Username:").grid(row=4, column=0, padx=10, pady=5)
        self.username_var = ctk.StringVar(value=node.get("username", ""))
        ctk.CTkEntry(self.dialog, textvariable=self.username_var, width=250).grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.dialog, text="SSH Password:").grid(row=5, column=0, padx=10, pady=5)
        self.password_var = ctk.StringVar(value=node.get("password", ""))
        password_entry = ctk.CTkEntry(self.dialog, textvariable=self.password_var, width=250, show="*")
        password_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent", border_width=0)
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
            
            # Update the node
            self.updated_node = {
                "display_name": self.display_name,
                "name": self.name,
                "ip": self.ip,
                "mac": self.mac,
                "username": self.username,
                "password": self.password,
                "status": node.get("status", "offline"),
                "selected": True
            }

            self.app.nodes[node_index] = self.updated_node
            self.app.config_manager.save_config(self.app.nodes)
            self.app.node_list.update_list(self.app.nodes)
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

    def remove_node(self, node):
        if not node:
            messagebox.showerror("Error", "No node selected.", parent=self.app.root)
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this node?", parent=self.app.root):
            
            self.app.nodes.remove(node)
            self.app.config_manager.save_config(self.app.nodes)
            self.app.node_list.update_list(self.app.nodes)
            self.app.node_details.initialize_details()

    def wake_node(self, node):
        if not node:
            messagebox.showerror("Error", "No node selected.", parent=self.app.root)
            return
        
        if node.get("status") == "online":
            messagebox.showinfo("Info", "Node is already online.", parent=self.app.root)
            return
        
        threading.Thread(target=self.wake, args=(node,), daemon=True).start()

    def wake(self, node):
        try:
            self.log_manager.log(node, "Trying to Wakeup up node...")

            mac = node.get("mac").replace(":", "").replace("-", "").upper()
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
            self.log_manager.log(node, "Magic packet sent successfully.")

            def check_online():
                for _ in range(30):
                    try:
                        with socket.create_connection((node.get("ip"), 22), timeout=2):
                            return True
                    except (socket.timeout, ConnectionRefusedError, OSError):
                        time.sleep(2)
                    return False
                    
            def check_online():
                self.log_manager.log(node, f"Waiting for node to respond...")
                for attempt in range(30):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)  # Short timeout
                        result = sock.connect_ex((node.get("ip"), 22))
                        sock.close()
                        
                        if result == 0:
                            return True
                        time.sleep(2)
                    except Exception as e:
                        self.log_manager.log(node, f"Connection attempt failed: {e}")
                        time.sleep(2)
                return False
                    
            if check_online():
                self.log_manager.log(node, "Node is now online.")
                node["status"] = "online"
            else:
                self.log_manager.log(node, "Node did not respond within timeout period.")
                node["status"] = "offline"

            self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))
        
        except Exception as e:
            self.log_manager.log(node, f"Error waking node: {str(e)}")

    def shutdown(self, node):
        try:
            self.log_manager.log(node, "Shutting down node...")
            
            # Create a socket and set a shorter timeout
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 2 second timeout
            
            result = sock.connect_ex((node.get("ip"), 22))
            sock.close()
            
            if result == 0:
                # Send shutdown command via SSH
                self.log_manager.log(node, "Sending shutdown command...")
                import paramiko
                
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                try:
                    ssh.connect(
                        node.get("ip"),
                        username=node.get("username"),
                        password=node.get("password"),
                        timeout=5
                    )
                    
                    shutdown_command = "shutdown /s /t 0"
                    stdin, stdout, stderr = ssh.exec_command(shutdown_command)
                    
                    # Check for errors
                    error = stderr.read().decode()
                    if error:
                        self.log_manager.log(node, f"Shutdown error: {error}")
                    else:
                        self.log_manager.log(node, "Shutdown command sent successfully")
                    
                    ssh.close()
                    
                    # Wait a bit for the node to begin shutdown
                    self.log_manager.log(node, "Waiting for node to shut down...")
                    time.sleep(10)  # Wait for 10 seconds before checking status
                    
                    # Check if the node is actually offline
                    try:
                        check_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        check_sock.settimeout(2)
                        result = check_sock.connect_ex((node.get("ip"), 22))
                        check_sock.close()
                        
                        if result == 0:
                            self.log_manager.log(node, "Node is still online, shutdown may have failed or delayed.")
                            node["status"] = "online"
                        else:
                            node["status"] = "offline"
                            self.log_manager.log(node, "Node is now offline.")
                    except Exception as check_error:
                        self.log_manager.log(node, f"Error checking node status: {str(check_error)}")
                        node["status"] = "unknown"
                    
                except Exception as ssh_error:
                    self.log_manager.log(node, f"SSH error: {str(ssh_error)}")
            else:
                self.log_manager.log(node, "Node is not reachable.")

            self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))

        except Exception as e:
            self.log_manager.log(node, f"Error shutting down node: {str(e)}")

    def shutdown_node(self, node):
        if not node:
            messagebox.showerror("Error", "No node selected.", parent=self.app.root)
            return
        
        if node.get("status") == "offline":
            messagebox.showinfo("Info", "Node is already offline.", parent=self.app.root)
            return
        
        threading.Thread(target=self.shutdown, args=(node,), daemon=True).start()

    def check_all_nodes(self):
        """
        Check the status of all nodes in the list.
        This is run in a separate thread to avoid blocking the main thread.
        """
        try:
            for node in self.app.nodes:
                try:
                    # Create a socket and set a shorter timeout
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)  # 1 second timeout
                    
                    result = sock.connect_ex((node.get("ip"), 22))
                    sock.close()
                    
                    # If result is 0, connection was successful
                    if result == 0:
                        node["status"] = "online"
                        self.log_manager.log(node, f"Node status: online", False)
                    else:
                        node["status"] = "offline"
                        self.log_manager.log(node, f"Node status: offline (connection failed)", False)
                except Exception as e:
                    node["status"] = "unknown"
                    self.log_manager.log(node, f"Error checking node status: {str(e)}", False)

            # Update the UI from the main thread
            self.app.node_list.on_button_clicked(self.app.nodes[0])
            self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))

        except Exception as e:
            print(f"Error in check_all_nodes: {e}")
            # We're in a thread, so we need to use after to schedule UI updates
            self.app.root.after(0, lambda: messagebox.showerror("Error", f"Error checking node.", parent=self.app.root))