from PIL import Image
import os

base_dir = r"c:\Users\Pipit Kiswieantoro\Desktop\Project\dipalearning\backend\static\dashboard\images"

images_to_convert = ["logo-primary.png", "login.png"]

for img_name in images_to_convert:
    img_path = os.path.join(base_dir, img_name)
    webp_path = os.path.join(base_dir, img_name.replace(".png", ".webp"))
    
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            img.save(webp_path, "WEBP", quality=85)
            print(f"Converted {img_name} to {os.path.basename(webp_path)}")
            old_size = os.path.getsize(img_path)
            new_size = os.path.getsize(webp_path)
            print(f"Size reduced from {old_size} to {new_size} bytes")
