import tkinter as tk
from PIL import Image, ImageTk
import function as f


# ---------- Hover Effect ----------
def on_enter(e):
    e.widget['background'] = '#2ecc71'  
    e.widget['foreground'] = 'white'

def on_leave(e):
    e.widget['background'] = '#27ae60'  
    e.widget['foreground'] = 'white'

# ---------- Main Window ----------
root = tk.Tk()
root.title("CRYPTXT")
root.geometry("750x500")
root.config(bg="#f4f4f4")
root.resizable(False, False)

# ---------- Main Frame ----------
main_frame = tk.Frame(root, bg="#f4f4f4")
main_frame.place(x=0, y=0, width=750, height=500)

# ---------- Header Bar ----------
header = tk.Frame(main_frame, bg="#222831")
header.place(x=0, y=0, width=750, height=80)

# --- Lock Icon (Transparent Background) ---
try:
    img = Image.open(r"images\lock.jpg").convert("RGBA")
    img = img.resize((45, 45), Image.LANCZOS)
    icon_img = ImageTk.PhotoImage(img)
    lbl_icon = tk.Label(header, image=icon_img, bg="#222831", bd=0)
    lbl_icon.place(x=20, y=20)

except Exception:
    lbl_icon = tk.Label(header, text="#", font=("Segoe UI", 28),
                        bg="#222831", fg="white")
    lbl_icon.place(x=20, y=15)

# --- Title & Subtitle ---
lbl_title = tk.Label(header, text="CRYPTXT", font=("Segoe UI", 32, "bold"),
                     bg="#222831", fg="#eeeeee", anchor="w")
lbl_title.place(x=80, y=10, height=40)

lbl_sub = tk.Label(header, text="Secure Text Encryption Tool", font=("Segoe UI", 12),
                   bg="#222831", fg="#bbbbbb", anchor="w")
lbl_sub.place(x=82, y=45)

# ---------- File Path ----------
frame_path = tk.Frame(main_frame, bg="#f4f4f4")
frame_path.place(x=50, y=120)

path_label = tk.Label(frame_path, text="Selected File:", font=("Arial", 12),
                      bg="#f4f4f4", fg="#222831")
path_label.pack(side="left", padx=5)

file_var = tk.StringVar()
file_entry = tk.Entry(frame_path, textvariable=file_var, width=40, font=("Arial", 11))
file_entry.pack(side="left", padx=50)

browse_btn = tk.Button(frame_path, text="Browse", font=("Arial", 11),
                       bg="#27ae60", fg="white", relief="flat",
                       command=lambda: f.browse_file(file_var))

browse_btn.pack(side="left", padx=5)

browse_btn.bind("<Enter>", on_enter)
browse_btn.bind("<Leave>", on_leave)

# ---------- Buttons ----------
frame_buttons = tk.Frame(main_frame, bg="#f4f4f4")
frame_buttons.place(x=150, y=200)

btn_encrypt = tk.Button(frame_buttons, text="Encrypt File", font=("Arial", 14, "bold"),
                        bg="#27ae60", fg="white", width=15, relief="flat")

btn_encrypt.grid(row=0, column=0, padx=20, pady=10)

btn_decrypt = tk.Button(frame_buttons, text="Decrypt File", font=("Arial", 14, "bold"),
                        bg="#27ae60", fg="white", width=15, relief="flat")
btn_decrypt.grid(row=0, column=1, padx=20, pady=10)

btn_encrypt.config(command=lambda: f.encrypt_file(file_var))
btn_decrypt.config(command=lambda: f.decrypt_file(file_var))


for b in (btn_encrypt, btn_decrypt):
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    
# ---------- Exit Button ----------
btn_exit = tk.Button(main_frame, text="Exit", font=("Arial", 12, "bold"),
                     bg="#d63031", fg="white", relief="flat", width=12, command=root.destroy)
btn_exit.place(x=300, y=300)

btn_exit.bind("<Enter>", lambda e: btn_exit.config(bg="#e74c3c"))
btn_exit.bind("<Leave>", lambda e: btn_exit.config(bg="#d63031"))

root.mainloop()
