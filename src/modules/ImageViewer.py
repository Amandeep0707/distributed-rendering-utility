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
        
    def update_title(self, node_name=None):
        if node_name:
            self.title = f"Render Preview ({node_name}):"
        else:
            self.title = "Render Preview:"
        self.image_viewer_label.configure(text=self.title)
        
    def display_image(self, image_path):
        """Display an image from the given path"""
        if not image_path or not os.path.exists(image_path):
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
            self.show_no_image()
            return False
    
    def show_no_image(self):
        """Show the 'no image' placeholder"""
        self.image_label.pack_forget()
        if hasattr(self, 'caption_label'):
            self.caption_label.pack_forget()
        self.no_image_label.pack(expand=True)
        self.current_image_path = None
        
    def start_monitoring(self, output_dir, node):

        """Monitor the output directory for new images"""
        if not output_dir or output_dir.startswith("//"):
            self.app.log_manager.log(node, "Cannot monitor relative output paths (//)", False)
            return
            
        self.monitor_running = True
        
        def monitor_thread():
            print("start monitoring")
            while self.monitor_running and node.get("status") == "rendering":
                try:
                    # Check if directory exists
                    if not os.path.exists(output_dir):
                        time.sleep(2)
                        continue
                        
                    # Get all image files in the directory
                    image_files = [f for f in os.listdir(output_dir) 
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
                    
                    if not image_files:
                        time.sleep(2)
                        continue
                        
                    # Sort by modification time (newest last)
                    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
                    
                    # Get the newest file
                    newest_file = image_files[-1]
                    newest_path = os.path.join(output_dir, newest_file)
                    
                    # Check if the file is different from the current one
                    mod_time = os.path.getmtime(newest_path)
                    if mod_time > self.last_modified_time:
                        self.last_modified_time = mod_time
                        # Update the image on the main thread
                        self.app.root.after(0, lambda: self.display_image(newest_path))
                        print(newest_path)
                    
                    time.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    self.app.log_manager.log(node, f"Image monitor error: {e}", False)
                    time.sleep(5)  # Back off on errors
            
        threading.Thread(target=monitor_thread, daemon=True).start()
        
    def stop_monitoring(self):
        """Stop the image monitoring thread"""
        self.monitor_running = False
        print("Stop monitoring")