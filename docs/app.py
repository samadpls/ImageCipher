import streamlit as st
from image_cipher import ImageCipher
import tempfile
import os


def save_uploaded_file_to_temp(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path


def encrypt_image(image_path, message, encrypt):
    cipher = ImageCipher()
    encoded_image_path = cipher.encode(image_path, message, encrypt=encrypt)
    return encoded_image_path, cipher.key


def decrypt_image(image_path, key):
    cipher = ImageCipher()
    decoded_message = cipher.decode(image_path, key)
    return decoded_message


def main():
    st.sidebar.image("docs/assets/image1.png", use_column_width=True)
    with open("docs/css/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.sidebar.markdown(
        """<a href='https://github.com/samadpls/ImageCipher'>\
        <img src='https://img.shields.io/github/stars/samadpls/ImageCipher?\
            color=red&label=star%20me&logoColor=red&style=social'></a>""",
        unsafe_allow_html=True,
    )
    st.title("Image Cipher")
    app_mode = st.sidebar.radio(
        "Choose the app mode", ["Encrypt", "Decrypt", "About Us"]
    )

    if app_mode == "Encrypt":
        st.header("Encrypt Image")
        uploaded_image = st.file_uploader(
            "Choose an image...", type=["png"]
        )
        message = st.text_area("Enter your message")
        use_encryption = st.checkbox("Use Encryption")

        if st.button("Encrypt"):
            if uploaded_image and message:
                temp_image_path = save_uploaded_file_to_temp(uploaded_image)
                encoded_image_path, key = encrypt_image(
                    temp_image_path, message, use_encryption
                )
                if use_encryption:
                    st.markdown("### Encryption Key:")
                    st.markdown(f"```\n{key.decode()}\n```")
                with open(encoded_image_path, "rb") as file:
                    st.download_button(
                        "Download Encrypted Image",
                        file,
                        file_name="encrypted_image.png",
                    )
                st.image(encoded_image_path, caption="Encrypted Image")
            else:
                st.error(
                    "Please upload an image and enter a message\
                         to encrypt."
                )

    elif app_mode == "Decrypt":
        st.header("Decrypt Image")
        uploaded_image = st.file_uploader(
            "Choose an image...", type=["png"]
        )
        key = st.text_input("Enter key (if any)")

        if st.button("Decrypt"):
            try:
                if uploaded_image:
                    temp_path = save_uploaded_file_to_temp(uploaded_image)
                    decrypted_message = decrypt_image(temp_path, key)
                    st.text_area(
                        "Decrypted Message",
                        value=decrypted_message,
                        height=200
                    )

                else:
                    st.error("Please upload an image to decrypt.")

            except Exception as e:
                st.error(e)

    elif app_mode == "About Us":
        st.header("About Us")
        st.markdown(
            "This project is developed by <ul> <li>[Abdul Samad]\
                    (https://github.com/samadpls/) </li>\
                     <li> [Maira Usman](https://github.com/Myrausman/)</li> \
                    </ul>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
