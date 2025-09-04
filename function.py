from tkinter import filedialog
import os





def browse_file(file_var):
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        file_var.set(file_path)






def encrypt_file(file_var):
    file_path = file_var.get().strip()
    if not file_path:
        print("No file selected")
        return
    if not os.path.exists(file_path):
        print("Invalid file path")
        return
    print("Encrypting:", file_path)





def decrypt_file(file_var):
    file_path = file_var.get().strip()
    if not file_path:
        print("No file selected")
        return
    if not os.path.exists(file_path):
        print("Invalid file path")
        return
    print("Decrypting:", file_path)
