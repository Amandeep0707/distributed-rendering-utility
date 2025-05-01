import os
import threading
import paramiko

class RenderManager:
    def __init__(self, app):
        self.app = app
        self.log_manager = app.log_manager
        self.ssh_clients = {} # Store SSH clients for each machine

    def start_render(self, machine):
        """
        Start a render on the selected machine.
        """
        try:

            self.log_manager.log(machine, "Trying to connect...")

            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    machine["ip"],
                    port=22,
                    username=machine["username"],
                    password=machine["password"],
                    timeout=10,
                )
                
                self.log_manager.log(machine, "Connection established successfully.")
                self.ssh_clients[machine["name"]] = client

                # Get the file paths and render arguments
                blender_file = self.app.footer.blender_path_field.get()
                output_path = self.app.footer.output_path_field.get()
                render_args = self.app.footer.render_args_field.get()

                if not blender_file:
                    self.log_manager.log(machine, "Error: No Blender file selected.")
                    return
                
                self.log_manager.log(machine, "Mapping network drive for Blender file...")

                # Get the server path without the filename
                server_path = os.path.dirname(blender_file)
                
                # Map the drive
                map_cmd = f'net use Y: "{server_path}" /user:Admin 123456 /persistent:yes 2>&1'
                stdin, stdout, stderr = client.exec_command(map_cmd)
                output = stdout.read().decode() + stderr.read().decode()
                
                if "Drive already mapped" in output or "command completed successfully" in output.lower():
                    self.log_manager.log(machine, "Network drive mapped or already available.")
                else:
                    self.log_manager.log(machine, f"Drive mapping output: {output}")
                
                # Update file path to use mapped drive
                local_file_path = blender_file

                # Create the render command
                # Adjust this command based on your specific requirements
                # This example assumes blender is in the PATH
                render_cmd = f'blender -b "{local_file_path}" -o "{output_path}" {render_args}'
                
                self.log_manager.log(machine, f"Executing render command: {render_cmd}")
                machine["status"] = "rendering"
                machine["progress"] = 0

                def run_render():
                    try:
                        stdin, stdout, stderr = client.exec_command(render_cmd)
                        
                        # Monitor the output
                        for line in stdout:
                            if "Sample" in line:
                                try:
                                    parts = line.split()
                                    for i, part in enumerate(parts):
                                        if "/" in part and i > 0 and parts[i-1] == "Sample":
                                            current, total = map(int, part.split("/"))
                                            progress = int(current / total * 100)
                                            self.app.machine_list.progress_bar.set(progress / 100)
                                        if "Fra" in part:
                                            machine["current_frame"] = part.strip("Fra:")
                                            self.app.machine_list.status_label.configure(text=f"Rendering: {machine['current_frame']}")
                                except Exception as e:
                                    self.log_manager.log(machine, f"Error parsing progress: {e}")
                        
                        # Check for errors
                        error_output = stderr.read().decode()
                        if error_output:
                            self.log_manager.log(machine, f"Render errors: {error_output}")
                        
                        # Mark as complete
                        machine["status"] = "online"
                        self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
                        self.log_manager.log(machine, "Render completed.")
                    
                    except Exception as e:
                        machine["status"] = "online"
                        self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
                        self.log_manager.log(machine, f"Error during render: {e}")

                # Start the render thread
                render_thread = threading.Thread(target=run_render, daemon=True)
                render_thread.start()
                
                # Update UI
                self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
            
            except paramiko.AuthenticationException:
                self.log_manager.log(machine, "Authentication failed. Check username and password.")
            except paramiko.SSHException as e:
                self.log_manager.log(machine, f"SSH error: {e}")
            except Exception as e:
                self.log_manager.log(machine, f"Connection error: {e}")
        
        except Exception as e:
            self.log_manager.log(machine, f"Error starting render: {e}")

    def stop_render(self, machine):
        """
        Stop a render on the selected machine.
        """
        try:
            self.log_manager.log(machine, "Stopping render...")
            
            # Get the stored SSH client
            client = self.ssh_clients.get(machine["name"])
            
            if client:
                # Kill blender processes
                stdin, stdout, stderr = client.exec_command("taskkill /F /IM blender.exe")
                output = stdout.read().decode()
                error = stderr.read().decode()
                
                if error:
                    self.log_manager.log(machine, f"Error stopping render: {error}")
                else:
                    self.log_manager.log(machine, f"Render stopped: {output}")
                
                # Update machine status
                machine["status"] = "online"
                machine["progress"] = 0
                self.app.root.after(0, lambda: self.app.machine_list.update_list(self.app.machines))
            else:
                self.log_manager.log(machine, "No active SSH connection found.")
        
        except Exception as e:
            self.log_manager.log(machine, f"Error stopping render: {e}")

    def render_all(self):
        """
        Start rendering on all available machines.
        """
        for machine in self.app.machines:
            if machine.get("status") == "online":
                threading.Thread(target=self.start_render, args=(machine,), daemon=True).start()