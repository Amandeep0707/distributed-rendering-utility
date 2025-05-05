from datetime import datetime
import customtkinter as ctk

class LogManager:
    def __init__(self, app):
        self.app = app

    def log(self, node, message, update_display=True):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {message}\n"

        if node["name"] not in self.app.render_logs:
            self.app.render_logs[node["name"]] = ""
        self.app.render_logs[node["name"]] += line

        if update_display and node and node.get("name") == node["name"]:
            self.change_log_display(node)

    def change_log_display(self, node):
        self.node_id = node["name"]

        self.app.render_log.log_text.configure(state="normal")
        self.app.render_log.log_text.delete("1.0", "end")

        if self.node_id in self.app.render_logs:
            self.app.render_log.log_text.insert("1.0", self.app.render_logs[self.node_id])
        else:
            self.app.render_log.log_text.insert("1.0", "No logs available for this node.")

        self.app.render_log.log_text.see("end")
        self.app.render_log.log_text.configure(state="disabled")