#!/usr/bin/env python3
"""Deploy generated illustrations to their target locations in the textbook."""

import json
import os
import shutil

base = "E:/Projects/LLMCourse"
mapping_path = f"{base}/scripts/illustration_mapping.json"
source_dir = f"{base}/scripts/generated-illustrations"

with open(mapping_path) as f:
    mapping = json.load(f)

copied = 0
errors = 0

for entry in mapping:
    idx = entry["prompt_index"]
    target = entry["target_path"]
    source = f"{source_dir}/img_{idx:03d}.png"

    if not os.path.exists(source):
        print(f"ERROR: Source not found: {source}")
        errors += 1
        continue

    # Create target directory if needed
    target_dir = os.path.dirname(target)
    os.makedirs(target_dir, exist_ok=True)

    # If target is .jpg, we still copy the .png (HTML will reference .jpg but
    # we may need to convert; for now just copy with correct extension)
    if target.endswith(".jpg"):
        # Convert PNG to JPEG using PIL if available, else just copy as-is
        try:
            from PIL import Image
            img = Image.open(source)
            img = img.convert("RGB")
            img.save(target, "JPEG", quality=90)
            print(f"  Converted: {os.path.basename(source)} -> {target}")
            copied += 1
        except ImportError:
            shutil.copy2(source, target)
            print(f"  Copied (as PNG, rename needed): {os.path.basename(source)} -> {target}")
            copied += 1
    else:
        shutil.copy2(source, target)
        print(f"  Copied: {os.path.basename(source)} -> {target}")
        copied += 1

print(f"\nDone: {copied} images deployed, {errors} errors")
