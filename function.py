from tkinter import filedialog
from tkinter import filedialog
import os
import struct
from typing import Any


def browse_file(file_var: Any) -> None:
    """Open a file dialog and set the selected path on the provided Tk variable.

    file_var should be a Tkinter StringVar or any object with a .set(str) method.
    """
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        file_var.set(file_path)


def _nibble_encrypt_bytes(data: bytes) -> bytes:
    """Encrypt raw bytes using a nibble-rechunking algorithm.

    The algorithm splits the input into 4-bit chunks, groups them in blocks
    of four (16 bits) and produces two output bytes per block by concatenating
    chunk0+chunk2 and chunk1+chunk3. This function returns the encrypted
    payload (no header).
    """
    if not data:
        return b""

    bitstring = ''.join(format(b, '08b') for b in data)
    # split into 4-bit chunks
    chunks = [bitstring[i:i + 4] for i in range(0, len(bitstring), 4)]
    # pad with zeros so the number of 4-bit chunks is a multiple of 4
    while len(chunks) % 4 != 0:
        chunks.append('0000')

    out = bytearray()
    for i in range(0, len(chunks), 4):
        # safe because we padded
        b0 = chunks[i] + chunks[i + 2]
        b1 = chunks[i + 1] + chunks[i + 3]
        out.append(int(b0, 2))
        out.append(int(b1, 2))

    return bytes(out)


def _nibble_decrypt_bytes(enc: bytes) -> bytes:
    """Reverse of _nibble_encrypt_bytes.

    Takes encrypted bytes and reconstructs the original raw bytes. Note that
    this function cannot know the original length if padding was applied;
    callers should provide/trust an external original length when necessary.
    """
    if not enc:
        return b""

    bit8 = [format(b, '08b') for b in enc]
    chunks = []
    # process pairs of bytes produced by the encryptor
    for i in range(0, len(bit8), 2):
        if i + 1 >= len(bit8):
            break
        b0 = bit8[i]
        b1 = bit8[i + 1]
        c0 = b0[:4]
        c2 = b0[4:]
        c1 = b1[:4]
        c3 = b1[4:]
        chunks.extend([c0, c1, c2, c3])

    bitstring = ''.join(chunks)
    out = bytearray()
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i + 8]
        if len(byte) < 8:
            break
        out.append(int(byte, 2))

    return bytes(out)


def encrypt_file_path(path: str) -> str:
    """Encrypt the file at `path` and write {path}.enc.

    The encrypted file format is: 8-byte big-endian unsigned original length
    followed by the encrypted payload. Returns the path to the written file.
    """
    if not path:
        raise ValueError("Empty path")
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, 'rb') as fh:
        data = fh.read()

    enc = _nibble_encrypt_bytes(data)
    out_path = path + '.enc'
    with open(out_path, 'wb') as fh:
        fh.write(struct.pack('>Q', len(data)))
        fh.write(enc)

    print(f"Encrypted {path} -> {out_path}")
    return out_path


def decrypt_file_path(path: str) -> str:
    """Decrypt a file produced by `encrypt_file_path` and write {path}.dec.

    Returns the path to the written file.
    """
    if not path:
        raise ValueError("Empty path")
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, 'rb') as fh:
        header = fh.read(8)
        if len(header) < 8:
            raise ValueError("Invalid encrypted file: too short")
        orig_len = struct.unpack('>Q', header)[0]
        enc = fh.read()

    dec = _nibble_decrypt_bytes(enc)
    dec = dec[:orig_len]
    out_path = path + '.dec'
    with open(out_path, 'wb') as fh:
        fh.write(dec)

    print(f"Decrypted {path} -> {out_path}")
    return out_path


def encrypt_file(file_var: Any) -> None:
    """GUI helper: encrypt file using a Tkinter StringVar-like object."""
    file_path = getattr(file_var, 'get', lambda: str(file_var))().strip()
    if not file_path:
        print("No file selected")
        return
    if not os.path.exists(file_path):
        print("Invalid file path")
        return
    try:
        encrypt_file_path(file_path)
    except Exception as e:
        print("Encryption failed:", e)


def decrypt_file(file_var: Any) -> None:
    """GUI helper: decrypt file using a Tkinter StringVar-like object."""
    file_path = getattr(file_var, 'get', lambda: str(file_var))().strip()
    if not file_path:
        print("No file selected")
        return
    if not os.path.exists(file_path):
        print("Invalid file path")
        return
    try:
        decrypt_file_path(file_path)
    except Exception as e:
        print("Decryption failed:", e)


def nibble_encrypt(input_string: str):
    """Backward-compatible wrapper for text input.

    Returns a list of characters (like the original implementation) by
    encrypting the UTF-8 bytes and returning the encrypted bytes decoded
    using latin-1 so the full byte range is preserved as a Python str.
    """
    enc = _nibble_encrypt_bytes(input_string.encode('utf-8'))
    # return list of characters to preserve original API (each char represents a byte)
    return [chr(b) for b in enc]