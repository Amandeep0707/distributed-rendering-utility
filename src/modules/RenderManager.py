import paramiko

class RenderManager:
    def __init__(self, app):
        self.app = app
        self.log_manager = app.log_manager

    def start_render(self, machine):
        try:
            self.log_manager.log(machine, "Trying to connect...")

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                machine["ip"],
                port=22,
                username=machine["username"],
                password=machine["password"],
                timeout=10,
            )
            
            self.log_manager.log(machine, "Connection established. Mapping Drives")

            # share_path = r"\\RT-SHAREDSTORAG\VR-Warriors"
            # mapped_file_path = self.app.footer.blender_path_field.get()
            # map_cmd = f'net use Y: {share_path} /user:{machine["username"]} {machine["password"]} && echo DriveMapped'
            # stdin, stdout, stderr = client.exec_command(map_cmd)
            # output = stdout.read().decode()
            # error = stderr.read().decode()
        
        except Exception as e:
            self.log_manager.log(machine, f"Error starting render: {e}")

    def stop_render(self, machine):
        try:
            self.log_manager.log(machine, "Stopping render...")
        
        except Exception as e:
            self.log_manager.log(machine, f"Error stopping render: {e}")