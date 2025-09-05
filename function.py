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


def nibble_encrypt(input_string):
    def rechunk(a):
        result = []
        for i in range(0, len(a), 4):
            if i + 2 < len(a):
                result.append(a[i] + a[i + 2])
            if i + 3 < len(a):
                result.append(a[i + 1] + a[i + 3])
        return result

    def binary_to_decimal(binary_str):
        decimal = 0
        for i, bit in enumerate(reversed(binary_str)):
            if bit == '1':
                decimal += 2 ** i
        return decimal

    if len(input_string) % 2 != 0:
        input_string = input_string.zfill(len(input_string) + 1)

    cipher = ''.join([bin(ord(ch))[2:].zfill(8) for ch in input_string])
    chunks = [cipher[i:i + 4] for i in range(0, len(cipher), 4)]
    encryptedlst = rechunk(chunks)
    encrypted = [chr(binary_to_decimal(b)) for b in encryptedlst]

    return encrypted