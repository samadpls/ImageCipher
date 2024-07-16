async function main() {
    console.log("Loading pyodide.");
    window.pyodide = await loadPyodide();
    console.log("Loading imagcipher...");
    await pyodide.loadPackage("micropip");
    const pip = pyodide.pyimport("micropip");
    await pip.install("imagecipher", { headers: { pragma: "no-cache", "cache-control": "no-cache" } });
}

main();

function showSection(id) {
    const sections = ['encrypt-section', 'decrypt-section', 'about-section'];
    sections.forEach(section => {
        document.getElementById(section).style.display = section === id ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('encrypt-link').addEventListener('click', (event) => {
        event.preventDefault();
        showSection('encrypt-section');
    });
    document.getElementById('decrypt-link').addEventListener('click', (event) => {
        event.preventDefault();
        showSection('decrypt-section');
    });
    document.getElementById('about-link').addEventListener('click', (event) => {
        event.preventDefault();
        showSection('about-section');
    });

    // Initial display setup
    showSection('encrypt-section');

    document.getElementById('encrypt-button').addEventListener('click', handleEncrypt);
    document.getElementById('decrypt-button').addEventListener('click', handleDecrypt);
});

async function encryptImage(imageFile, message) {
    const base64Image = await fileToBase64(imageFile);

    const pythonCode = `
        from image_cipher import ImageCipher
        from PIL import Image
        from io import BytesIO
        import base64
        import json

        def encrypt_image(base64_image, message):
            image_data = base64.b64decode(base64_image.split(",")[1])
            image = Image.open(BytesIO(image_data))
            cipher = ImageCipher()
            encrypted_image = cipher.encode(image, message)

            buffer = BytesIO()
            encrypted_image.save(buffer, format="PNG")
            encoded_image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            encoded_image_path = "data:image/png;base64," + encoded_image_str

            return json.dumps({"encoded_image_path": encoded_image_path})

        encrypt_image("${base64Image}", "${message}")
    `;

    const result = await pyodide.runPythonAsync(pythonCode);
    return result;
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);
    });
}

async function decryptImage(imageFilePath, key) {
    return pyodide.runPython(`
from image_cipher import ImageCipher
import json

# Define a function to handle decryption
def decrypt_image(image_file_path, key):
    cipher = ImageCipher()
    decoded_message = cipher.decode(image_file_path, key)
    return json.dumps({'decoded_message': decoded_message})

# Call the function with passed arguments
decrypt_image(image_file_path, key)
    `, { image_file_path: imageFilePath, key }); // Pass JavaScript variables here
}


async function handleEncrypt() {
    const imageFile = document.getElementById("encrypt-image").files[0];
    const message = document.getElementById("encrypt-message").value;
    console.log("image:", imageFile);

    if (imageFile && message) {
        // Create a URL for the file
        const imageUrl = URL.createObjectURL(imageFile);
        console.log("image URL:", imageUrl);

        // Display the image
        document.getElementById("encrypt-result").innerHTML = `<h3>Selected Image</h3><img src="${imageUrl}" alt="Selected Image">`;

        // Encrypt the image
        const result = await encryptImage(imageFile, message);
        const data = JSON.parse(result);
        console.log(data);

        // Display the encrypted image
        document.getElementById("encrypt-result").innerHTML += `<h3>Encrypted Image</h3><img src="${data.encoded_image_path}" alt="Encrypted Image"><br><a href="${data.encoded_image_path}" download="encrypted_image.png">Download</a>`;
    } else {
        alert("Please select an image and enter a message.");
    }
}

async function handleDecrypt() {
    const imageFile = document.getElementById("decrypt-image").files[0];
    const key = document.getElementById("decrypt-key").value;

    if (imageFile) {
        const reader = new FileReader();
        reader.onload = async function(event) {
            const imageFilePath = event.target.result;
            const result = await decryptImage(imageFilePath, key);
            const data = JSON.parse(result);
            document.getElementById("decrypt-result").innerHTML = `<h3>Decrypted Message</h3><p>${data.decoded_message}</p>`;
        };
        reader.readAsDataURL(imageFile);
    } else {
        alert("Please select an image to decrypt.");
    }
}
