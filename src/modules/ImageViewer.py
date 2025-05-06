import customtkinter as ctk
from PIL import Image, ImageTk
import os
import threading
import time

class ImageViewer(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.frame = ctk.CTkFrame(master, border_width=0, corner_radius=0)
        self.frame.pack(padx=(0, 5), pady=5, anchor="e", side="right", fill="both", expand=True)

        # Add image viewer title
        self.title = "Render Preview:"
        self.image_viewer_label = ctk.CTkLabel(self.frame, text=self.title, font=ctk.CTkFont(size=15, weight="bold"))
        self.image_viewer_label.pack(anchor="w", side="top", pady=5, padx=(10, 5))

        # Image display area
        self.image_frame = ctk.CTkFrame(self.frame)
        self.image_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # No image placeholder
        self.no_image_label = ctk.CTkLabel(self.image_frame, text="No rendered image available")
        self.no_image_label.pack(expand=True)

        # Image label (hidden initially)
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        
        # Current image path being displayed
        self.current_image_path = None
        
        # Monitor thread for image updates
        self.monitor_running = False
        self.last_modified_time = 0
        self.output_directory = None
        self.current_node = None
        
    def update_title(self, node_name=None):
        if node_name:
            self.title = f"Render Preview ({node_name}):"
        else:
            self.title = "Render Preview:"
        self.image_viewer_label.configure(text=self.title)
        
    def display_image(self, image_path):
        """Display an image from the given path"""
        if not image_path or not os.path.exists(image_path):
            # Don't clear the image if we already have one displayed
            if not self.current_image_path or not os.path.exists(self.current_image_path):
                self.show_no_image()
            return False
            
        try:
            # Keep track of this path
            self.current_image_path = image_path
            
            # Load and resize the image to fit the frame
            pil_image = Image.open(image_path)
            
            # Get frame dimensions
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            
            # Use reasonable defaults if frame hasn't been fully rendered yet
            if frame_width < 50:
                frame_width = 400
            if frame_height < 50:
                frame_height = 300
                
            # Calculate new dimensions while preserving aspect ratio
            img_width, img_height = pil_image.size
            aspect_ratio = img_width / img_height
            
            if img_width > img_height:
                new_width = min(frame_width - 20, img_width)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(frame_height - 20, img_height)
                new_width = int(new_height * aspect_ratio)
            
            # Resize the image
            resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert PIL image to CTk image
            ctk_image = ctk.CTkImage(light_image=resized_image, 
                                     dark_image=resized_image,
                                     size=(new_width, new_height))
            
            # Hide the no image label
            self.no_image_label.pack_forget()
            
            # Update the image label
            self.image_label.configure(image=ctk_image)
            if not self.image_label.winfo_ismapped():
                self.image_label.pack(expand=True)
                
            # Store the image reference to prevent garbage collection
            self.image_label.image = ctk_image
            
            # Create caption with file info
            file_size = os.path.getsize(image_path) / 1024  # KB
            mod_time = time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(image_path)))
            caption = f"File: {os.path.basename(image_path)} ({file_size:.1f} KB, {mod_time})"
            
            # Add caption below image
            if hasattr(self, 'caption_label'):
                self.caption_label.configure(text=caption)
            else:
                self.caption_label = ctk.CTkLabel(self.image_frame, text=caption, font=ctk.CTkFont(size=12))
                self.caption_label.pack(side="bottom", pady=(0, 5))
            
            return True
        except Exception as e:
            self.app.log_manager.log({"name": "System"}, f"Error displaying image: {e}", False)
            # Don't clear the image if there's an error, keep showing the previous one
            if not self.current_image_path or not os.path.exists(self.current_image_path):
                self.show_no_image()
            return False
    
    def show_no_image(self):
        """Show the 'no image' placeholder"""
        self.image_label.pack_forget()
        if hasattr(self, 'caption_label'):
            self.caption_label.pack_forget()
        self.no_image_label.pack(expand=True)
        
    def start_monitoring(self, node=None):
        """Monitor the output directory for new images"""
        # Store the current node being monitored
        self.current_node = node
        
        # Store the output directory
        self.output_directory = self.app.footer.orig_file_path + self.app.defaults.get("output_path", "\Output").replace("//", "\\")
        
        # Update the node name in the title
        if node:
            self.update_title(node.get("display_name", node.get("name", "Unknown")))
        
        # Check if the directory exists or can be accessed
        if not os.path.exists(self.output_directory):
            self.app.log_manager.log(node, f"Output directory does not exist: {self.output_directory}", False)
            self.app.log_manager.log(node, "Will start monitoring when directory becomes available", False)
        
        self.monitor_running = True
        
        def monitor_thread():
            self.app.log_manager.log(node, f"Image monitoring started for: {self.output_directory}", False)
            last_image_path = None
            
            while self.monitor_running:
                try:
                    # Check if directory exists
                    if not os.path.exists(self.output_directory):
                        time.sleep(2)
                        continue
                        
                    # Get all image files in the directory
                    image_files = [f for f in os.listdir(self.output_directory) 
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.tif', '.bmp', '.exr'))]
                    
                    if not image_files:
                        # If we previously had an image and now there are none, don't clear
                        time.sleep(2)
                        continue
                        
                    # Sort by modification time (newest last)
                    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.output_directory, x)))
                    
                    # Get the newest file
                    newest_file = image_files[-1]
                    newest_path = os.path.join(self.output_directory, newest_file)
                    
                    # Check if the file is different from the current one
                    mod_time = os.path.getmtime(newest_path)
                    if mod_time > self.last_modified_time:
                        self.last_modified_time = mod_time
                        last_image_path = newest_path
                        # Update the image on the main thread
                        self.app.root.after(0, lambda: self.display_image(newest_path))
                    
                    time.sleep(1)  # Check every second for more responsive updates
                    
                except Exception as e:
                    self.app.log_manager.log(node, f"Image monitor error: {e}", False)
                    time.sleep(3)  # Back off on errors
            
            # After monitoring stops, ensure we're still showing the last image
            if last_image_path and os.path.exists(last_image_path):
                self.app.root.after(0, lambda: self.display_image(last_image_path))
                
            self.app.log_manager.log(node, "Image monitoring stopped", False)
        
        # Start the monitoring thread
        threading.Thread(target=monitor_thread, daemon=True).start()
        
    def stop_monitoring(self):
        """Stop the image monitoring thread, but keep the current image displayed"""
        self.monitor_running = False
        
    def resume_monitoring(self):
        """Resume monitoring the output directory for the current node"""
        if self.output_directory and self.current_node:
            self.start_monitoring(self.output_directory, self.current_node)
            
    def check_for_latest_image(self, output_dir=None):
        """One-time check for the latest image in the output directory"""
        # If no output directory is specified, use the stored one or the one from the footer
        if not output_dir:
            output_dir = self.output_directory or self.app.footer.output_path_field.get()
            
        if not output_dir or not os.path.exists(output_dir):
            return
            
        try:
            # Get all image files in the directory
            image_files = [f for f in os.listdir(output_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.tif', '.bmp', '.exr'))]
            
            if not image_files:
                return
                
            # Sort by modification time (newest last)
            image_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
            
            # Get the newest file
            newest_file = image_files[-1]
            newest_path = os.path.join(output_dir, newest_file)
            
            # Display the image
            self.display_image(newest_path)
                
        except Exception as e:
            print(f"Error checking for latest image: {e}")