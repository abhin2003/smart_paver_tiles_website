import os
import shutil

src_tiles_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\src\assets\tiles"
public_images_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\images"
catalog_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\catalog"

categories = [
    "SDP_1004_ZIGZAG", "SDP_1005", "SDP_1007", "SDP_1010", "SDP_1011",
    "SDP_1012_COBBLE", "SDP_1013_COBBLE", "SDP_1014_GRASS", "SDP_1015_PEBBLE",
    "BANGALORE_STONES", "Unclassified"
]

for cat in categories:
    os.makedirs(os.path.join(catalog_dir, cat), exist_ok=True)

# Map for manually analyzed images from public/assets/images
manual_map = {
    "paver_img_1.png": "Unclassified",
    "paver_img_2.png": "Unclassified",
    "paver_img_3.jpeg": "SDP_1004_ZIGZAG",
    "paver_img_4.jpeg": "SDP_1004_ZIGZAG",
    "paver_img_5.jpeg": "SDP_1004_ZIGZAG",
    "paver_img_6.jpeg": "SDP_1004_ZIGZAG",
    "paver_img_7.jpeg": "SDP_1005",
    "paver_img_8.jpeg": "SDP_1004_ZIGZAG",
    "paver_img_9.jpeg": "SDP_1014_GRASS",
    "paver_img_10.jpeg": "SDP_1013_COBBLE",
    "paver_img_11.jpeg": "SDP_1014_GRASS",
    "paver_img_12.jpeg": "SDP_1010",
    "paver_img_13.jpeg": "SDP_1010",
    "paver_img_14.jpeg": "SDP_1010",
    "paver_img_15.jpeg": "SDP_1013_COBBLE",
    "paver_img_16.jpeg": "SDP_1013_COBBLE",
    "paver_img_17.jpeg": "SDP_1013_COBBLE",
    "paver_img_18.jpeg": "SDP_1013_COBBLE",
    "paver_img_19.jpeg": "SDP_1013_COBBLE",
    "paver_img_20.jpeg": "SDP_1013_COBBLE",
    "paver_img_21.jpeg": "SDP_1015_PEBBLE",
    "paver_img_22.jpeg": "SDP_1015_PEBBLE",
    "paver_img_23.jpeg": "SDP_1015_PEBBLE",
    "paver_img_24.jpeg": "SDP_1013_COBBLE",
    "paver_img_25.jpeg": "SDP_1011",
    "paver_img_26.jpeg": "SDP_1014_GRASS",
    "paver_img_27.jpeg": "SDP_1014_GRASS",
    "paver_img_28.jpeg": "SDP_1014_GRASS",
}

# Organize public/assets/images
if os.path.exists(public_images_dir):
    for filename in os.listdir(public_images_dir):
        if not os.path.isfile(os.path.join(public_images_dir, filename)): continue
        cat = manual_map.get(filename, "Unclassified")
        shutil.copy(
            os.path.join(public_images_dir, filename),
            os.path.join(catalog_dir, cat, f"cat_{filename}")
        )

# Organize src/assets/tiles using timestamp clustering
if os.path.exists(src_tiles_dir):
    for filename in os.listdir(src_tiles_dir):
        if not filename.endswith(('.jpeg', '.png', '.jpg', '.mp4')): continue
        
        # Parse time from "WhatsApp Image 2026-08-01 at 17.30.05.jpeg"
        # We can extract the "17.30.xx" part
        time_str = filename.split("at ")[-1].split(".")[0].split(" ")[0] if "at " in filename else ""
        
        cat = "Unclassified"
        if time_str.startswith("17.29"):
            cat = "SDP_1014_GRASS"
        elif time_str.startswith("17.30"):
            # 17.30.00 to 17.30.15
            sec_str = time_str.split(".")[-1]
            try:
                sec = int(sec_str)
                if sec <= 15:
                    cat = "SDP_1012_COBBLE"
                elif sec <= 25:
                    cat = "BANGALORE_STONES"
                else:
                    cat = "SDP_1013_COBBLE"
            except:
                pass
        
        shutil.copy(
            os.path.join(src_tiles_dir, filename),
            os.path.join(catalog_dir, cat, f"wa_{filename}")
        )

print("Image categorization and organization complete!")
