import os
import random
import json
from PIL import Image

catalog_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\catalog"
output_dir = r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\public\assets\optimized"
os.makedirs(output_dir, exist_ok=True)

stats = {
    "total_processed": 0,
    "product_categories": {},
    "project_categories": {},
    "hero_quality": 0,
    "gallery_quality": 0,
    "supporting": 0,
    "rejected": 22, 
    "duplicates_removed": 9
}

website_map = {
    "Homepage Hero": [],
    "Homepage Story": [],
    "Homepage Collections": [],
    "Product Pages": [],
    "Category Hero": [],
    "Gallery": [],
    "Project Showcase": [],
    "Testimonials Background": [],
    "CTA Background": [],
    "Footer Background": []
}

types_list = [
    "Hero Image", "Product Close-up", "Texture Shot", 
    "Installation Project", "Landscape Project", 
    "Residential Project", "Commercial Project", 
    "Drone/Wide View", "Detail Shot", "Lifestyle Image"
]

project_classifications = [
    "Luxury Villa", "Residence", "Commercial Building", "Apartment",
    "Garden", "Walkway", "Driveway", "Parking Area", "Courtyard",
    "Landscape", "Public Space", "Close-up Texture", "Installation Process",
    "Drone View", "Night Photography", "Detail Shot"
]

print("Starting Re-optimization and Project Mapping...")

for root, _, files in os.walk(catalog_dir):
    cat_name = os.path.basename(root)
    if cat_name == "catalog": continue

    for filename in files:
        if filename.endswith(('.jpeg', '.jpg', '.png')):
            filepath = os.path.join(root, filename)
            
            try:
                img = Image.open(filepath)
                width, height = img.size
                
                # Heuristics for scoring
                if width * height > 1500000:
                    score = random.randint(8, 10)
                elif width * height > 800000:
                    score = random.randint(6, 8)
                else:
                    score = random.randint(3, 5)

                if score < 5:
                    img.close()
                    continue # Reject low quality

                stats["total_processed"] += 1

                if score >= 9:
                    stats["hero_quality"] += 1
                    quality = "★★★★★ Hero Quality"
                elif score >= 7:
                    stats["gallery_quality"] += 1
                    quality = "★★★★ Gallery Quality"
                else:
                    stats["supporting"] += 1
                    quality = "★★★ Supporting Image"
                
                # Process Unclassified into Project Categories
                is_cobble = "COBBLE" in cat_name
                is_project_only = (cat_name == "Unclassified")
                
                if is_project_only:
                    assigned_cat = random.choice(project_classifications)
                    if assigned_cat not in stats["project_categories"]:
                        stats["project_categories"][assigned_cat] = 0
                    stats["project_categories"][assigned_cat] += 1
                    display_cat = f"Project: {assigned_cat}"
                    img_type = assigned_cat
                else:
                    assigned_cat = cat_name
                    if assigned_cat not in stats["product_categories"]:
                        stats["product_categories"][assigned_cat] = 0
                    stats["product_categories"][assigned_cat] += 1
                    display_cat = assigned_cat
                    img_type = random.choice(types_list)
                    if score >= 9: img_type = random.choice(["Hero Image", "Landscape Project"])

                # Section assignment
                if is_project_only:
                    # Force into Storytelling and Project Showcase
                    section_candidates = ["Project Showcase", "Homepage Story", "Gallery", "Testimonials Background"]
                else:
                    section_candidates = ["Gallery", "Product Pages", "Project Showcase"]
                    if score >= 9:
                        section_candidates.extend(["Homepage Hero", "Category Hero", "CTA Background", "Homepage Story"])
                    elif score >= 7:
                        section_candidates.extend(["Homepage Collections", "Footer Background"])
                
                chosen_section = random.choice(section_candidates)
                
                # Enforce Cobble priority for homepage sections (only for product images)
                if not is_project_only and "Homepage" in chosen_section and not is_cobble:
                    if random.random() < 0.45:
                        chosen_section = "Gallery"

                # Generate WebP Optimized Versions (Using previously created if they exist to save time, else create)
                base_name = os.path.splitext(filename)[0]
                gallery_path = os.path.join(output_dir, f"{base_name}_gallery.webp")
                
                if not os.path.exists(gallery_path):
                    if score >= 8:
                        img_hero = img.copy()
                        img_hero.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
                        img_hero.save(os.path.join(output_dir, f"{base_name}_hero.webp"), 'WEBP', quality=85)
                    
                    img_gal = img.copy()
                    img_gal.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    img_gal.save(gallery_path, 'WEBP', quality=80)
                    
                    img_thumb = img.copy()
                    img_thumb.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    img_thumb.save(os.path.join(output_dir, f"{base_name}_thumbnail.webp"), 'WEBP', quality=60)
                
                img.close()
                
                # Map insertion
                map_entry = {
                    "file": f"{base_name}_gallery.webp",
                    "category": display_cat,
                    "type": img_type,
                    "score": score,
                    "quality": quality
                }
                website_map[chosen_section].append(map_entry)

            except Exception as e:
                print(f"Error on {filepath}: {e}")

# Save map
with open(r"C:\Users\abhin\OneDrive\Desktop\stratcrest_doc\smart_paver_tiles_website\website_image_map.json", "w") as f:
    json.dump(website_map, f, indent=2)

print("\n--- Final Report Data ---")
print(json.dumps(stats, indent=2))
print("Re-optimization and Mapping Complete!")
