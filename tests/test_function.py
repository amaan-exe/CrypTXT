import os
import importlib.util
from pathlib import Path


def _load_function_module():
    root = Path(__file__).resolve().parents[1]
    module_path = root / 'function.py'
    spec = importlib.util.spec_from_file_location('cryp_function', str(module_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_nibble_roundtrip_bytes():
    mod = _load_function_module()
    data = b"Hello, CrypTXT! \x00\x01"
    enc = mod._nibble_encrypt_bytes(data)
    dec = mod._nibble_decrypt_bytes(enc)
    assert dec[:len(data)] == data


def test_encrypt_decrypt_files(tmp_path):
    mod = _load_function_module()
    p = tmp_path / "sample.txt"
    p.write_bytes(b"This is a test file")
    enc_path = mod.encrypt_file_path(str(p))
    assert os.path.exists(enc_path)
    dec_path = mod.decrypt_file_path(enc_path)
    assert os.path.exists(dec_path)
    assert open(dec_path, 'rb').read() == b"This is a test file"
