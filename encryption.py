import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import customtkinter as ctk
import threading
import time

class StegoEncryptGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("StegoCrypt - Steganography Encoder")
        self.root.geometry("800x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="StegoCrypt Encoder", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("Encode")
        self.tabview.add("About")
        
        self.setup_encode_tab()
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

    def setup_encode_tab(self):
        encode_frame = self.tabview.tab("Encode")
        
        preview_frame = ctk.CTkFrame(encode_frame)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="No image selected",
            width=300,
            height=200
        )
        self.preview_label.pack(pady=10)
        
        control_frame = ctk.CTkFrame(encode_frame)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.select_btn = ctk.CTkButton(
            control_frame,
            text="Select Input Image",
            command=self.select_image
        )
        self.select_btn.pack(pady=10)
        
        self.output_btn = ctk.CTkButton(
            control_frame,
            text="Select Output Location",
            command=self.select_output
        )
        self.output_btn.pack(pady=10)
        
        message_label = ctk.CTkLabel(control_frame, text="Secret Message:")
        message_label.pack(pady=(10,0))
        
        self.message_entry = ctk.CTkTextbox(
            control_frame,
            height=100,
            width=400
        )
        self.message_entry.pack(pady=10)
        
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
        
        self.encode_btn = ctk.CTkButton(
            control_frame,
            text="Encode Message",
            command=self.start_encoding
        )
        self.encode_btn.pack(pady=10)

    def setup_about_tab(self):
        about_frame = self.tabview.tab("About")
        
        about_text = """
        StegoCrypt Encoder - Steganography Message Hiding Tool
        
        This application allows you to hide secret messages in images 
        using steganography techniques. The messages are encrypted using 
        XOR cipher and can only be extracted with the correct password.
        
        Features:
        • Modern user interface
        • Dark/Light mode support
        • Real-time image preview
        • Secure password entry
        • Progress visualization
        
        How to use:
        1. Click 'Select Input Image' to choose an image
        2. Click 'Select Output Location' to choose where to save
        3. Enter your secret message
        4. Enter an encryption password
        5. Click 'Encode Message' to hide your message
        
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
            self.input_path = filename
            self.update_preview(filename)
            self.status_var.set(f"Selected input: {os.path.basename(filename)}")

    def select_output(self):
        filetypes = [
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes
        )
        if filename:
            self.output_path = filename
            self.status_var.set(f"Output will be saved as: {os.path.basename(filename)}")

    def update_preview(self, image_path):
        try:
            image = Image.open(image_path)
            image.thumbnail((300, 200))
            photo = ImageTk.PhotoImage(image)
            
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def text_to_binary(self, text):
        return ''.join(format(ord(char), '08b') for char in text)

    def xor_encrypt(self, text, password):
        return ''.join(chr(ord(t) ^ ord(password[i % len(password)]))
                      for i, t in enumerate(text))

    def start_encoding(self):
        if not hasattr(self, 'input_path'):
            messagebox.showwarning("Warning", "Please select an input image first.")
            return
        
        if not hasattr(self, 'output_path'):
            messagebox.showwarning("Warning", "Please select an output location.")
            return
            
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to hide.")
            return
            
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return
        
        self.encode_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.output_btn.configure(state="disabled")
        
        thread = threading.Thread(
            target=self.hide_text,
            args=(message, password)
        )
        thread.start()

    def hide_text(self, secret_message, password):
        try:
            self.status_var.set("Encoding message...")
            self.progress.set(0)
            
            img = Image.open(self.input_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            encrypted_message = self.xor_encrypt(secret_message, password)
            binary_message = self.text_to_binary(encrypted_message) + '1111111111111110'
            
            pixels = list(img.getdata())
            total_pixels = len(pixels)
            
            new_pixels = []
            binary_index = 0
            
            for i, pixel in enumerate(pixels):
                r, g, b = pixel
                
                if binary_index < len(binary_message):
                    r = (r & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                
                new_pixels.append((r, g, b))
                
                if i % 1000 == 0:
                    progress = i / total_pixels
                    self.progress.set(progress)
                    self.root.update_idletasks()
            
            img.putdata(new_pixels)
            img.save(self.output_path)
            
            self.status_var.set("Message hidden successfully!")
            self.progress.set(1)
            messagebox.showinfo("Success", 
                              f"Message hidden successfully in {os.path.basename(self.output_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hide message: {str(e)}")
            self.status_var.set("Encoding failed!")
        
        finally:
            # Re-enable buttons
            self.encode_btn.configure(state="normal")
            self.select_btn.configure(state="normal")
            self.output_btn.configure(state="normal")

def main():
    app = StegoEncryptGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()