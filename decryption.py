import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from ttkthemes import ThemedTk
import customtkinter as ctk
import threading
import time

class ModernStegoGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("StegoCrypt - Steganography Decoder")
        self.root.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="StegoCrypt", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("Decode")
        self.tabview.add("About")
       
        self.setup_decode_tab()
        
        self.setup_about_tab()
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ctk.CTkLabel(
            self.root,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
        self.progress = ctk.CTkProgressBar(self.root)
        self.progress.pack(side="bottom", fill="x", padx=10, pady=5)
        self.progress.set(0)
        
        self.theme_button = ctk.CTkButton(
            self.root,
            text="Toggle Theme",
            command=self.toggle_theme,
            width=100
        )
        self.theme_button.place(relx=0.95, rely=0.02, anchor="ne")

    def setup_decode_tab(self):
        decode_frame = self.tabview.tab("Decode")
        
        preview_frame = ctk.CTkFrame(decode_frame)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="No image selected",
            width=300,
            height=200
        )
        self.preview_label.pack(pady=10)
        
        control_frame = ctk.CTkFrame(decode_frame)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.select_btn = ctk.CTkButton(
            control_frame,
            text="Select Image",
            command=self.select_image
        )
        self.select_btn.pack(pady=10)
        
        self.password_frame = ctk.CTkFrame(control_frame)
        self.password_frame.pack(pady=10)
        
        password_label = ctk.CTkLabel(
            self.password_frame,
            text="Password:"
        )
        password_label.pack(side="left", padx=5)
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            show="•",
            width=200
        )
        self.password_entry.pack(side="left", padx=5)
        
        self.extract_btn = ctk.CTkButton(
            control_frame,
            text="Extract Message",
            command=self.start_extraction
        )
        self.extract_btn.pack(pady=10)
        
        result_frame = ctk.CTkFrame(decode_frame)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.result_text = ctk.CTkTextbox(
            result_frame,
            height=100,
            width=400
        )
        self.result_text.pack(pady=10, fill="both", expand=True)

    def setup_about_tab(self):
        about_frame = self.tabview.tab("About")
        
        about_text = """
        StegoCrypt - Advanced Steganography Decoder
        
        This application allows you to extract hidden messages from images 
        using steganography techniques. The messages are encrypted using 
        XOR cipher and can only be extracted with the correct password.
        
        Features:
        • Modern user interface
        • Dark/Light mode support
        • Real-time image preview
        • Secure password entry
        • Progress visualization
        
        How to use:
        1. Click 'Select Image' to choose an image
        2. Enter the decryption password
        3. Click 'Extract Message' to decode
        
        Version 1.0.0
        """
        
        about_label = ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        about_label.pack(padx=20, pady=20)

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

    def select_image(self):
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.image_path = filename
            self.update_preview(filename)
            self.status_var.set(f"Selected: {os.path.basename(filename)}")

    def update_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(image)
            
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def binary_to_text(self, binary_string):
        chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def xor_decrypt(self, text, password):
        return ''.join(chr(ord(t) ^ ord(password[i % len(password)]))
                      for i, t in enumerate(text))

    def start_extraction(self):
        if not hasattr(self, 'image_path'):
            messagebox.showwarning("Warning", "Please select an image first.")
            return
            
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        self.extract_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        
        thread = threading.Thread(target=self.extract_message, args=(password,))
        thread.start()

    def extract_message(self, password):
        try:
            self.status_var.set("Extracting message...")
            self.progress.set(0)
            
            img = Image.open(self.image_path)
            pixels = list(img.getdata())
            total_pixels = len(pixels)
            
            binary_message = ""
            for i, pixel in enumerate(pixels):
                r, g, b = pixel
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)
                
                if i % 1000 == 0:
                    progress = i / total_pixels
                    self.progress.set(progress)
                    self.root.update_idletasks()
            
            end_marker = "1111111111111110"
            binary_message = binary_message.split(end_marker)[0]
            
            encrypted_message = self.binary_to_text(binary_message)
            secret_message = self.xor_decrypt(encrypted_message, password)
            
            self.result_text.delete("1.0", tk.END)
            for char in "Hidden Message: " + secret_message:
                self.result_text.insert(tk.END, char)
                self.result_text.see(tk.END)
                time.sleep(0.02)
                self.root.update_idletasks()
            
            self.status_var.set("Message extracted successfully!")
            self.progress.set(1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")
            self.status_var.set("Extraction failed!")
        
        finally:
            self.extract_btn.configure(state="normal")
            self.select_btn.configure(state="normal")

def main():
    app = ModernStegoGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()