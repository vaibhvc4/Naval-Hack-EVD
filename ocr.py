import pytesseract
from PIL import Image
import re

# Set the path to the Tesseract executable (only needed on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load an image from file
image_path = 'enhanced_image.png'  # Replace with your image path
image = Image.open(image_path)

# Specify custom configuration
custom_config = r'--oem 3 '  # Example: using LSTM engine and treating the image as a single block of text

# Perform OCR on the image with custom configuration
text = pytesseract.image_to_string(image, config=custom_config)

# Filter the text to keep only English characters (a-z, A-Z) and spaces

# Print the extracted text
print("Extracted Text (English charaters only):")
print(text)
