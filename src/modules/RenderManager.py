import os
import threading
import paramiko

class RenderManager:
    def __init__(self, app):
        self.app = app
        self.log_manager = app.log_manager
        self.ssh_clients = {} # Store SSH clients for each node

    def start_render(self, node):
        """
        Start a render on the selected node.
        """
        try:

            self.log_manager.log(node, "Trying to connect...")

            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    node["ip"],
                    port=22,
                    username=node["username"],
                    password=node["password"],
                    timeout=10,
                )
                
                self.log_manager.log(node, "Connection established successfully.")
                self.ssh_clients[node["name"]] = client

                # Get the file paths and render arguments
                blender_file = self.app.footer.blender_path_field.get()
                output_path = self.app.footer.output_path_field.get()
                render_args = self.app.footer.render_args_field.get()
                drive_username = self.app.config_manager.drive_credentials.get("username")
                drive_password = self.app.config_manager.drive_credentials.get("password")
                drive_path = self.app.config_manager.drive_credentials.get("path")

                if not blender_file:
                    self.log_manager.log(node, "Error: No Blender file selected.")
                    return
                
                self.log_manager.log(node, "Mapping network drive for Blender file...")
                
                # Map the drive
                map_cmd = f'net use Y: /delete /y & net use Y: "{drive_path}" /user:{drive_username} {drive_password} /persistent:yes 2>&1'
                stdin, stdout, stderr = client.exec_command(map_cmd)
                output = stdout.read().decode() + stderr.read().decode()
                
                if "Drive already mapped" in output or "command completed successfully" in output.lower():
                    self.log_manager.log(node, "Network drive mapped or already available.")
                else:
                    self.log_manager.log(node, f"Drive mapping output: {output}")

                # Create the render command
                # Adjust this command based on your specific requirements
                # This example assumes blender is in the PATH
                render_cmd = f'blender -b "{blender_file}" -o "{output_path}" {render_args}'
                
                self.log_manager.log(node, "Starting Render...")
                node["status"] = "rendering"
                node["progress"] = 0

                def run_render():
                    try:
                        stdin, stdout, stderr = client.exec_command(render_cmd)
                        
                        # Monitor the output
                        for line in stdout:
                            # self.log_manager.log(node, line.strip())
                            if "Sample" in line:
                                try:
                                    parts = line.split()
                                    for i, part in enumerate(parts):
                                        if "/" in part and i > 0 and parts[i-1] == "Sample":
                                            current, total = map(int, part.split("/"))
                                            progress = int(current / total * 100)
                                            node.get("progress_bar").set(progress)
                                        if "Fra" in part:
                                            current_frame = part.strip("Fra:")
                                            node.get("status_label").configure(text=f"Rendering: {current_frame}")

                                except Exception as e:
                                    self.log_manager.log(node, f"Error parsing progress: {e}")

                            elif "cannot read" in line.lower():
                                node["status"] = "error"
                                self.log_manager.log(node, "Error: Cannot Read File. Drive Mount Error")
                        
                        # Check for errors
                        error_output = stderr.read().decode()
                        if error_output:
                            self.log_manager.log(node, f"Render errors: {error_output}")
                        
                        # Mark as complete
                        node["status"] = "online"
                        self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))
                        self.log_manager.log(node, "Render completed.")
                    
                    except Exception as e:
                        node["status"] = "online"
                        self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))
                        self.log_manager.log(node, f"Error during render: {e}")

                # Start the render thread
                render_thread = threading.Thread(target=run_render, daemon=True)
                render_thread.start()
                
                # Update UI
                self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))
            
            except paramiko.AuthenticationException as e:
                self.log_manager.log(node, f"Authentication Error: {e}")
                node["status"] = "error"
            except paramiko.SSHException as e:
                self.log_manager.log(node, f"SSH error: {e}")
                node["status"] = "error"
            except Exception as e:
                self.log_manager.log(node, f"Connection error: {e}")
                node["status"] = "error"
        
        except Exception as e:
            self.log_manager.log(node, f"Error starting render: {e}")
            node["status"] = "error"

    def stop_render(self, node):
        """
        Stop a render on the selected node.
        """
        try:
            self.log_manager.log(node, "Stopping render...")
            
            # Get the stored SSH client
            client = self.ssh_clients.get(node["name"])
            
            if client:
                # Kill blender processes
                stdin, stdout, stderr = client.exec_command("taskkill /F /IM blender.exe")
                output = stdout.read().decode()
                error = stderr.read().decode()
                
                if error:
                    self.log_manager.log(node, f"Error stopping render: {error}")
                else:
                    self.log_manager.log(node, f"Render stopped: {output}")
                
                # Update node status
                node["status"] = "online"
                node["progress"] = 0
                self.app.root.after(0, lambda: self.app.node_list.update_list(self.app.nodes))
            else:
                self.log_manager.log(node, "No active SSH connection found.")
        
        except Exception as e:
            self.log_manager.log(node, f"Error stopping render: {e}")

    def render_all(self):
        """
        Start rendering on all available nodes.
        """
        for node in self.app.nodes:
            if node.get("status") == "online":
                threading.Thread(target=self.start_render, args=(node,), daemon=True).start()