# Secure Image Steganography Using Python

A Python-based **Image Steganography Application** that allows users to **hide secret text messages inside images** and later **extract them securely** using a simple and interactive **Graphical User Interface (GUI)**.

This project demonstrates how sensitive information can be concealed inside digital images using **Least Significant Bit (LSB)** steganography, making the hidden data invisible to the human eye.

---

## 👨‍💻 Author

**Anuj Gupta**  
Engineering Student  
GitHub: https://github.com/anuj-gupta03  

---

## 📖 Introduction

Steganography is the art of hiding information inside another medium such that the existence of the hidden data is not noticeable. Unlike cryptography, which scrambles data, steganography focuses on **concealing the presence of the message itself**.

This project implements **image steganography** using Python, enabling secure communication by embedding secret text within image pixels.

---

## ✨ Features

- 🖼️ Hide secret text messages inside image files  
- 🔍 Extract hidden messages from stego-images  
- 🧑‍💻 User-friendly GUI built using `tkinter`  
- 🔐 Uses **Least Significant Bit (LSB)** technique  
- 📂 Supports PNG images for better data integrity  
- ⚡ Fast and lightweight execution  

---

## 🧰 Technology Stack

| Component | Technology |
|---------|------------|
| Programming Language | Python |
| GUI Framework | Tkinter |
| Image Processing | Pillow (PIL) |
| Data Handling | NumPy |

---

## ⚙️ Working Principle

1. The user selects an image and enters a secret message.
2. The message is converted into binary format.
3. Binary data is embedded into the **least significant bits of image pixels**.
4. The modified image (stego-image) appears visually unchanged.
5. During decoding, the binary data is extracted and converted back to text.

---

## 📁 Project Structure
