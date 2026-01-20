import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

# ---------- STEGANOGRAPHY FUNCTIONS ----------

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text) + '1111111111111110'

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ""
    for c in chars:
        if c == '11111111':
            break
        message += chr(int(c, 2))
    return message

def hide_data(img_path, secret):
    img = cv2.imread(img_path)
    binary = text_to_binary(secret)
    idx = 0

    for row in img:
        for pixel in row:
            for i in range(3):
                if idx < len(binary):
                    pixel[i] = int(format(pixel[i], '08b')[:-1] + binary[idx], 2)
                    idx += 1
    return img

def extract_data(img_path):
    img = cv2.imread(img_path)
    binary = ""

    for row in img:
        for pixel in row:
            for i in range(3):
                binary += format(pixel[i], '08b')[-1]

    return binary_to_text(binary)

# ---------- GUI FUNCTIONS ----------

def upload_image():
    global img_path
    img_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
    if img_path:
        img = Image.open(img_path).resize((200, 200))
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img

def hide_action():
    if not img_path:
        messagebox.showerror("Error", "Upload an image")
        return

    secret = secret_entry.get()
    if secret == "":
        messagebox.showerror("Error", "Enter secret text")
        return

    stego = hide_data(img_path, secret)
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    cv2.imwrite(save_path, stego)
    messagebox.showinfo("Success", "Data hidden successfully")

def extract_action():
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
    if path:
        msg = extract_data(path)
        extract_entry.delete(0, tk.END)
        extract_entry.insert(0, msg)

# ---------- MAIN GUI ----------

root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x400")

tabs = ttk.Notebook(root)
hide_tab = ttk.Frame(tabs)
extract_tab = ttk.Frame(tabs)

tabs.add(hide_tab, text="Hide Information")
tabs.add(extract_tab, text="Extract Information")
tabs.pack(expand=True, fill="both")

# ----- Hide Tab -----
img_path = None

tk.Button(hide_tab, text="Upload Image", command=upload_image).pack(pady=10)
img_label = tk.Label(hide_tab)
img_label.pack()

tk.Label(hide_tab, text="Enter Secret Word").pack(pady=5)
secret_entry = tk.Entry(hide_tab, width=40)
secret_entry.pack()

tk.Button(hide_tab, text="Hide Data", command=hide_action).pack(pady=10)

# ----- Extract Tab -----
tk.Button(extract_tab, text="Upload Stego Image", command=extract_action).pack(pady=20)
extract_entry = tk.Entry(extract_tab, width=45)
extract_entry.pack()

# ---------- START GUI ----------
root.mainloop()




