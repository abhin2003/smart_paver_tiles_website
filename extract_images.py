import fitz
import os
import io
from PIL import Image

pdf_path = r"C:\Users\abhin\Downloads\SMART PAVERS CATLOG1.pdf"
output_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\images"

os.makedirs(output_dir, exist_ok=True)

pdf_document = fitz.open(pdf_path)

image_count = 0
for page_index in range(len(pdf_document)):
    page = pdf_document[page_index]
    image_list = page.get_images()
    
    for image_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_count += 1
        
        image_filename = os.path.join(output_dir, f"paver_img_{image_count}.{image_ext}")
        with open(image_filename, "wb") as image_file:
            image_file.write(image_bytes)
        print(f"Extracted {image_filename}")

print(f"Done. Extracted {image_count} images.")
