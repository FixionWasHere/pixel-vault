# LSB Image Steganography

A lightweight command-line tool written in Python that hides secret text messages inside ordinary images. 

It uses Least Significant Bit (LSB) manipulation to alter the pixel data of an image. To the human eye, the output image looks 100% identical to the original, but it secretly carries encoded binary data.

## How It Works
Every pixel in an image is made of Red, Green, and Blue (RGB) values. This script converts your secret text into binary and replaces the very last bit (the least significant bit) of those color values with your data. 

## ⚠️ Important: Sharing Encoded Images
This tool relies on exact byte-level data. If an image is compressed, the hidden binary data is permanently destroyed. 

**Do NOT send encoded images normally through:**
* WhatsApp, Telegram, or Instagram (They automatically compress uploads)
* Discord (Unless sent inside a `.zip` file)

**How to successfully send an encoded image:**
1. Send it as a **"Document"** or **"File"** in WhatsApp/Telegram to bypass compression.
2. Zip the file before sending it over Discord.
3. Upload the raw `.png` to Google Drive/Dropbox and share the link.

*Note: The script includes a built-in file integrity check. It hides a `STEG` signature at the beginning of the binary chain. If the decoder does not detect this signature, it will immediately abort and warn you that the image has been corrupted by compression.*

## Requirements
You just need Python and the Pillow library for image processing:
```bash
pip install Pillow
