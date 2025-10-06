# CrypTXT

Simple nibble-based demonstration tool to encrypt and decrypt text files.

Features
- Minimal GUI using Tkinter (see `demo.py`).
- Nibble-based byte transformation with file helpers in `function.py`.

Quick start
1. Install requirements (Pillow is optional for the GUI icon):

```
pip install -r requirements.txt
```

2. Run the GUI:

```
python demo.py
```

Running tests

```
pip install pytest
pytest -q
```

Notes
- This project is a learning/demo project and the "encryption" is not
	cryptographically secure. Do not use for protecting sensitive data.
