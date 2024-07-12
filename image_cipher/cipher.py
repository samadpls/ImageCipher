from PIL import Image
from cryptography.fernet import Fernet
import os


class ImageCipher:
    """
    A class for encoding and decoding messages in images using steganography.
    """

    def __init__(self):
        self.key = None

    def encode(self, image_path, message, encrypt=True):
        """
        Encodes a message into an image using steganography.

        Args:
            image_path (str): The path to the input image file.
            message (str): The message to be encoded.
            encrypt (bool, optional): Whether to encrypt the message. 
                                    Defaults to True.

        Returns:
            str: The path to the output encoded image file.

        Raises:
            ValueError: If encryption is enabled but no key is provided.
        """
        if encrypt:
            self.key = Fernet.generate_key()
            fernet = Fernet(self.key)
            message = fernet.encrypt(message.encode()).decode()

        img = Image.open(image_path)
        pixels = img.load()

        binary_message = ''.join(format(ord(char), '08b') for char in message)

        length = len(message)
        encrypted = 1 if encrypt else 0
        if len(pixels[0, 0]) == 3:
            pixels[0, 0] = (length, encrypted, pixels[0, 0][2])
        else:
            pixels[0, 0] = (length, encrypted, pixels[0, 0]
                            [2], pixels[0, 0][3])

        index = 0
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if x == 0 and y == 0:
                    continue
                pixel = list(pixels[x, y])
                for i in range(3):
                    if index < len(binary_message):
                        pixel[i] = (pixel[i] & 0xFE) | int(
                            binary_message[index])
                        index += 1
                pixels[x, y] = tuple(pixel)
                if index >= len(binary_message):
                    break
            if index >= len(binary_message):
                break

        output_path = f"{os.path.splitext(image_path)[0]}_encoded" \
                  f"{os.path.splitext(image_path)[1]}"
        img.save(output_path)
        return output_path

    def decode(self, image_path, key=None):
        """
        Decodes a message from an image using steganography.

        Args:
            image_path (str): The path to the input encoded image file.
            key (str, optional): The encryption key for decryption. 
                                Defaults to None.

        Returns:
            str: The decoded message.

        Raises:
            ValueError: If the image contains encrypted text but 
                        no key is provided.
            ValueError: If the provided key is incorrect.
        """
        img = Image.open(image_path)
        pixels = img.load()

        length, encrypted = pixels[0, 0][:2]

        binary_message = ""
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if x == 0 and y == 0:
                    continue
                pixel = pixels[x, y]
                for i in range(3):
                    binary_message += str(pixel[i] & 1)
                if len(binary_message) >= length * 8:
                    break
            if len(binary_message) >= length * 8:
                break

        message = ''.join(chr(int(binary_message[i:i+8], 2))
                          for i in range(0, length * 8, 8))

        if encrypted:
            if key or self.key:
                try:
                    fernet = Fernet(key or self.key)
                    message = fernet.decrypt(message.encode()).decode()
                except Exception as e:
                    raise ValueError("The provided key is incorrect.")
            else:
                raise ValueError("This image contains encrypted text."
                                 " A key is required for decryption.")

        return message
