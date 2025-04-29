from datetime import datetime
import customtkinter as ctk

class LogManager:
    def __init__(self, app):
        self.app = app

    def log(self, machine, message):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {message}\n"

        if machine["name"] not in self.app.render_logs:
            self.app.render_logs[machine["name"]] = ""
        self.app.render_logs[machine["name"]] += line

        if machine and machine.get("name") == machine["name"]:
            self.change_log_display(machine)

    def change_log_display(self, machine):
        self.machine_id = machine["name"]

        self.app.render_log.log_text.configure(state="normal")
        self.app.render_log.log_text.delete("1.0", "end")

        if self.machine_id in self.app.render_logs:
            self.app.render_log.log_text.insert("1.0", self.app.render_logs[self.machine_id])
        else:
            self.app.render_log.log_text.insert("1.0", "No logs available for this machine.")

        self.app.render_log.log_text.see("end")
        self.app.render_log.log_text.configure(state="disabled")