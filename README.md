
<img align='right' src="https://github.com/user-attachments/assets/79b7dc25-55c2-4fc1-84fc-551a73d37c7d" height=350px>



# ImageCipherLib

ImageCipherLib is a Python library for encoding and decoding messages in images using steganography and optional encryption.  
![Supported python versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-black.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Run Unittests](https://github.com/samadpls/ImageCipherLib/actions/workflows.yml/badge.svg)](https://github.com/samadpls/ImageCipherLib/actions/workflows.yml)
[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](LICENSE)
<img src='https://img.shields.io/github/stars/samadpls/ImageCipherLib?color=red&label=stars&logoColor=black&style=social'>
## Installation 🚀

You can install ImageCipherLib using pip:

```
pip install ImageCipherLib
```

## Features ✨

- Encode text messages into images
- Decode messages from encoded images
- Optional encryption of messages before encoding
- Support for various image formats

## Usage 📝

Here's a quick example of how to use ImageCipherLib:

```python
from ImageCipherLib import ImageCipher

# Create an instance of ImageCipher
cipher = ImageCipher()

# Encode a message
encoded_image_path = cipher.encode("original_image.png", "Secret message", encrypt=True)

# Decode a message
decoded_message = cipher.decode(encoded_image_path, key=cipher.key)

print(decoded_message)  # Output: Secret message
```

## API Reference 📘

### `ImageCipher` class

#### `encode(image_path, message, encrypt=True)`

Encodes a message into an image.

- `image_path` (str): The path to the input image file.
- `message` (str): The message to be encoded.
- `encrypt` (bool, optional): Whether to encrypt the message. Defaults to True.

Returns:
- str: The path to the output encoded image file.

#### `decode(image_path, key=None)`

Decodes a message from an encoded image.

- `image_path` (str): The path to the input encoded image file.
- `key` (str, optional): The encryption key for decryption. Required if the message was encrypted.

Returns:
- str: The decoded message.

## Requirements 🛠️

- Python 3.6+
- Pillow (PIL)
- cryptography

## Contributing 🙌

Contributions are welcome! Please feel free to submit a Pull Request.
