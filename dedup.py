import os
import imagehash
from PIL import Image

catalog_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\catalog"
hashes = {}
removed = 0
total_processed = 0

print("Starting Duplicate Detection...")

for root, _, files in os.walk(catalog_dir):
    for filename in files:
        if filename.endswith(('.jpeg', '.jpg', '.png')):
            filepath = os.path.join(root, filename)
            total_processed += 1
            try:
                img = Image.open(filepath)
                # Compute average hash for speed and basic similarity
                h = imagehash.average_hash(img)
                img.close()
                
                # Check for duplicates
                is_duplicate = False
                for existing_hash, existing_file in hashes.items():
                    if h - existing_hash <= 2: # Tolerance for near-duplicates
                        is_duplicate = True
                        print(f"DUPLICATE DETECTED: {filename} is similar to {os.path.basename(existing_file)}")
                        os.remove(filepath)
                        removed += 1
                        break
                
                if not is_duplicate:
                    hashes[h] = filepath
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"\nSummary:")
print(f"Total Processed: {total_processed}")
print(f"Duplicates Removed: {removed}")
print(f"Unique Images Remaining: {total_processed - removed}")
