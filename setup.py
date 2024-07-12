from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="imagecipher",
    version="0.0.1",
    author="samadpls",
    author_email="abdulsamadsid1@gmail.com",
    description="ImageCipher is a Python library designed for encrypting and"
    " decrypting images, offering a secure way to handle image data through "
    "customizable cipher algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samadpls/ImageCipher",
    packages=find_packages(include=['image_cipher', 'image_cipher.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Pillow>=10.4.0",
        "cryptography>=42.0.8",
        "wheel"
    ],
    tests_require=[
        "pytest>=8.2.2",
        "flake8>=7.1.0"
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
)
