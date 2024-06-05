from PIL import Image
import pytesseract

# Load images
image_paths = [
    "/mnt/data/Screenshot 2024-05-28 101942.png",
    "/mnt/data/Screenshot 2024-05-28 102006.png",
    "/mnt/data/Screenshot 2024-05-28 102021.png"
]


def run():
    # Extract text from images
    extracted_texts = [pytesseract.image_to_string(Image.open(image_path)) for image_path in image_paths]
    extracted_texts
    print()