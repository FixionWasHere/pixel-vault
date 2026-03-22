from PIL import Image


def text_to_binary(text):
    """Converts a standard text string into 8-bit binary."""
    binary_list = [format(ord(char), '08b') for char in text]
    return ''.join(binary_list)


def binary_to_text(binary_string):
    """Converts a continuous string of binary back into readable text."""
    # Split the long binary string into chunks of 8 bits
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    # Convert each 8-bit chunk back to a character, ignoring any incomplete chunks
    return ''.join([chr(int(char, 2)) for char in chars if len(char) == 8])


def encode_image(image_path, secret_text, output_path):
    """Hides the secret text inside the image pixels with a safety signature."""
    # Add 'STEG' at the front as a signature, and '=====' at the end as a stop sign
    secret_text = "STEG" + secret_text + "====="
    binary_secret = text_to_binary(secret_text)
    data_len = len(binary_secret)
    data_index = 0

    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"[-] Error: Could not find image '{image_path}'")
        return

    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            if data_index < data_len:
                r, g, b = pixels[x, y]

                if data_index < data_len:
                    r = (r & 254) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < data_len:
                    g = (g & 254) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < data_len:
                    b = (b & 254) | int(binary_secret[data_index])
                    data_index += 1

                pixels[x, y] = (r, g, b)
            else:
                img.save(output_path)
                print(
                    f"[+] Success! Secret successfully hidden in '{output_path}'")
                return

    print("[-] Error: The image is too small to hold all this data!")


def decode_image(image_path):
    """Extracts hidden text and checks for compression corruption."""
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"[-] Error: Could not find image '{image_path}'")
        return

    pixels = img.load()
    binary_data = ""

    # Read the least significant bit of every single pixel
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Convert the massive binary string back to text
    extracted_text = binary_to_text(binary_data)

    # 1. The Sanity Check: Did the signature survive?
    if not extracted_text.startswith("STEG"):
        return "[-] Error: No hidden message found, or the image was compressed/corrupted by a messaging app."

    # 2. Look for our stop sign and cut off the garbage data after it
    if "=====" in extracted_text:
        # Split by the stop sign, take the first part, and remove the "STEG" signature
        clean_text = extracted_text.split("=====")[0][4:]
        return clean_text
    else:
        return "[-] Error: Message signature found, but the end of the message was corrupted."


# --- Terminal Interface ---
if __name__ == "__main__":
    print("\n--- 🕵️‍♂️ Image Steganography Tool ---")
    print("1. Encode a secret message into an image")
    print("2. Decode a secret message from an image")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        img_in = input("Enter input image name (e.g., test.png): ")
        text = input("Enter the secret message to hide: ")
        img_out = input("Enter output image name (e.g., encoded.png): ")
        encode_image(img_in, text, img_out)

    elif choice == '2':
        img_in = input("Enter the image to decode (e.g., encoded.png): ")
        secret = decode_image(img_in)
        if secret:
            print(f"\n[+] Extracted Message: \n{secret}\n")

    else:
        print("[-] Invalid choice. Please run the script again.")
