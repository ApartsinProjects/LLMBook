"""
Crop excessive white margins from all book images.

Detects near-white borders (top, bottom, left, right) and trims them,
leaving a small padding (10px) for aesthetics. Only crops if the margin
is significant (> 30px on any side).
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image, ImageChops

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
MIN_MARGIN_TO_CROP = 30  # Only crop if margin exceeds this many pixels
PADDING = 10  # Leave this many pixels of padding after cropping
WHITE_THRESHOLD = 245  # Pixels with all channels >= this are "white"


def get_content_bbox(img):
    """Find the bounding box of non-white content."""
    # Convert to RGB if necessary
    if img.mode == 'RGBA':
        # Create white background
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Create a threshold image: pixels near white become black, others white
    pixels = img.load()
    w, h = img.size

    # Find bounds
    top = 0
    for y in range(h):
        row_has_content = False
        for x in range(0, w, 3):  # Sample every 3rd pixel for speed
            r, g, b = pixels[x, y]
            if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
                row_has_content = True
                break
        if row_has_content:
            top = y
            break
    else:
        return None  # All white

    bottom = h
    for y in range(h - 1, -1, -1):
        row_has_content = False
        for x in range(0, w, 3):
            r, g, b = pixels[x, y]
            if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
                row_has_content = True
                break
        if row_has_content:
            bottom = y + 1
            break

    left = 0
    for x in range(w):
        col_has_content = False
        for y in range(top, bottom, 3):
            r, g, b = pixels[x, y]
            if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
                col_has_content = True
                break
        if col_has_content:
            left = x
            break

    right = w
    for x in range(w - 1, -1, -1):
        col_has_content = False
        for y in range(top, bottom, 3):
            r, g, b = pixels[x, y]
            if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
                col_has_content = True
                break
        if col_has_content:
            right = x + 1
            break

    return (left, top, right, bottom)


def crop_image(filepath):
    """Crop white margins from an image if they exceed the threshold."""
    try:
        img = Image.open(filepath)
    except Exception as e:
        return False

    w, h = img.size
    if w < 50 or h < 50:
        return False  # Skip tiny images (icons, etc.)

    bbox = get_content_bbox(img)
    if bbox is None:
        return False  # All white, skip

    left, top, right, bottom = bbox

    # Calculate margins
    margin_top = top
    margin_bottom = h - bottom
    margin_left = left
    margin_right = w - right

    # Only crop if at least one margin exceeds the threshold
    if (margin_top < MIN_MARGIN_TO_CROP and
        margin_bottom < MIN_MARGIN_TO_CROP and
        margin_left < MIN_MARGIN_TO_CROP and
        margin_right < MIN_MARGIN_TO_CROP):
        return False

    # Apply crop with padding
    crop_left = max(0, left - PADDING) if margin_left >= MIN_MARGIN_TO_CROP else 0
    crop_top = max(0, top - PADDING) if margin_top >= MIN_MARGIN_TO_CROP else 0
    crop_right = min(w, right + PADDING) if margin_right >= MIN_MARGIN_TO_CROP else w
    crop_bottom = min(h, bottom + PADDING) if margin_bottom >= MIN_MARGIN_TO_CROP else h

    # Crop
    cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    new_w, new_h = cropped.size

    # Only save if we actually removed significant space
    pixels_saved = (w * h) - (new_w * new_h)
    if pixels_saved < 1000:
        return False

    rel = filepath.relative_to(BOOK_ROOT)
    print(f"  CROPPED: {rel}")
    print(f"    {w}x{h} -> {new_w}x{new_h} (margins: T={margin_top} B={margin_bottom} L={margin_left} R={margin_right})")

    # Save (preserve format)
    if img.mode == 'RGBA' and filepath.suffix.lower() == '.png':
        cropped.save(filepath, 'PNG', optimize=True)
    elif filepath.suffix.lower() == '.png':
        cropped.save(filepath, 'PNG', optimize=True)
    elif filepath.suffix.lower() in ('.jpg', '.jpeg'):
        cropped.save(filepath, 'JPEG', quality=92)
    else:
        cropped.save(filepath)

    return True


def main():
    # Find all images in part-* and appendices directories
    image_dirs = list(BOOK_ROOT.glob("part-*/module-*/images"))
    image_dirs += list(BOOK_ROOT.glob("appendices/*/images"))

    all_images = []
    for d in image_dirs:
        all_images.extend(d.glob("*.png"))
        all_images.extend(d.glob("*.jpg"))
        all_images.extend(d.glob("*.jpeg"))

    all_images = sorted(set(all_images))
    print(f"Scanning {len(all_images)} images...")

    cropped = 0
    for img_path in all_images:
        if crop_image(img_path):
            cropped += 1

    print(f"\nCropped: {cropped} images")


if __name__ == "__main__":
    main()
