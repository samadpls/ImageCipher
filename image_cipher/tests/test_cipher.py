import pytest
import os
from cryptography.fernet import Fernet
from image_cipher import ImageCipher

@pytest.fixture
def image_path():
    """Fixture that returns the path of the test image."""
    test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
    yield test_image_path
    encoded_image_path = os.path.splitext(test_image_path)[0] + "_encoded.png"
    if os.path.exists(encoded_image_path):
        os.remove(encoded_image_path)

@pytest.fixture
def encryption_key():
    """Fixture that generates and returns an encryption key."""
    return Fernet.generate_key()

class TestImageCipher:
    def test_encode_without_encryption(self, image_path):
        """Test encoding without encryption."""
        cipher = ImageCipher()
        message = "Test message without encryption"
        output_path = cipher.encode(image_path, message, encrypt=False)
        assert os.path.exists(output_path)
        assert output_path.endswith("_encoded.png")
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_encode_with_generated_key(self, image_path):
        """Test encoding with a generated encryption key."""
        cipher = ImageCipher()
        message = "Test message with encryption using generated key"
        output_path = cipher.encode(image_path, message, encrypt=True)
        assert output_path.endswith("_encoded.png")
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_encode_with_specific_key(self, image_path, encryption_key):
        """Test encoding with a specific encryption key."""
        cipher = ImageCipher()
        message = "Test message with encryption using specific key"
        output_path = cipher.encode(image_path, message, encrypt=True)
        assert os.path.exists(output_path)
        assert output_path.endswith("_encoded.png")
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_decode_without_encryption(self, image_path):
        """Test decoding without encryption."""
        cipher = ImageCipher()
        message = "Test message without encryption"
        encoded_path = cipher.encode(image_path, message, encrypt=False)
        decoded_message = cipher.decode(encoded_path)
        assert decoded_message == message

    def test_decode_with_correct_key(self, image_path, encryption_key):
        """Test decoding with the correct encryption key."""
        cipher = ImageCipher()
        message = "Test message with encryption using specific key"
        encoded_path = cipher.encode(image_path, message, encrypt=True)
        decoded_message = cipher.decode(encoded_path, cipher.key)
        assert decoded_message == message

    def test_decode_with_incorrect_key(self, image_path, encryption_key):
        """Test decoding with an incorrect encryption key."""
        cipher = ImageCipher()
        message = "Test message with encryption using specific key"
        encoded_path = cipher.encode(image_path, message, encrypt=True)
        incorrect_key = Fernet.generate_key()
        with pytest.raises(ValueError, match="The provided key is incorrect."):
            cipher.decode(encoded_path, incorrect_key)
