from PIL import Image, ImageDraw, ImageFont
import os

# Directory with logos
logo_dir = r'C:\Users\cadel\deep_council_final'
output_dir = r'C:\Users\cadel\deep_council_final\logos_resized'

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Logo files to resize (local files only)
logos = [
    ('logo_dell.png', 'Dell'),
    ('logo_moller.png', 'Moller'),
    ('logo_uc.png', 'UC Chile'),
    ('logo_acgs.png', 'ACHS'),
    ('logo_claude.png', 'Claude'),
    ('logo_fireworks.png', 'Fireworks'),
    ('logo_llama.png', 'llama.cpp'),
    ('logo_qwen.png', 'Qwen'),
    ('logo_advisor.webp', 'Hermes'),
    ('logo_excel.png', 'Excel'),
    ('logo_discord.png', 'Discord'),
    ('logo_openclaw.webp', 'OpenClaw'),
    ('logo_powerpoint.png', 'PowerPoint'),
    ('logo_windows.png', 'Windows'),
    ('logo_word.png', 'Word'),
]

# Target size for website (32px for display, but we'll make 64px for quality)
TARGET_SIZE = 64

# Create comparison canvas
GAP = 30
LABEL_HEIGHT = 40
num_logos = len(logos)
cols = 5
rows = (num_logos + cols - 1) // cols

canvas_width = cols * (TARGET_SIZE + GAP) + GAP
canvas_height = rows * (TARGET_SIZE + GAP + LABEL_HEIGHT) + GAP

canvas = Image.new('RGB', (canvas_width, canvas_height), (245, 245, 240))
draw = ImageDraw.Draw(canvas)

# Draw title
draw.text((GAP, 15), "Logo Size Comparison (all normalized to 64x64 visual)", fill=(30, 30, 30))

# Process each logo
for i, (filename, label) in enumerate(logos):
    filepath = os.path.join(logo_dir, filename)
    if not os.path.exists(filepath):
        print(f"Missing: {filepath}")
        continue
    
    # Load image
    try:
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        continue
    
    # Get original size
    orig_w, orig_h = img.size
    
    # Resize to fit in TARGET_SIZE while maintaining aspect ratio
    img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    
    # Save individual resized logo
    resized_path = os.path.join(output_dir, f"{label.lower().replace('.', '').replace(' ', '_')}_64.png")
    
    # Create transparent background for PNG
    resized_img = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (255, 255, 255, 0))
    offset_x = (TARGET_SIZE - img.width) // 2
    offset_y = (TARGET_SIZE - img.height) // 2
    if img.mode == 'RGBA':
        resized_img.paste(img, (offset_x, offset_y), img)
    else:
        resized_img.paste(img, (offset_x, offset_y))
    resized_img.save(resized_path, 'PNG')
    print(f"Saved: {resized_path} ({orig_w}x{orig_h} -> {img.width}x{img.height})")
    
    # Add to comparison canvas
    col = i % cols
    row = i // cols
    x = GAP + col * (TARGET_SIZE + GAP)
    y = GAP + 50 + row * (TARGET_SIZE + GAP + LABEL_HEIGHT)
    
    # Draw white background
    draw.rectangle([x, y, x + TARGET_SIZE, y + TARGET_SIZE], fill=(255, 255, 255), outline=(180, 180, 180))
    
    # Paste logo
    if img.mode == 'RGBA':
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2), img)
    else:
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2))
    
    # Draw label
    label_y = y + TARGET_SIZE + 8
    draw.text((x, label_y), label, fill=(30, 30, 30))
    draw.text((x, label_y + 18), f"{orig_w}x{orig_h}", fill=(100, 100, 100))

# Save comparison
comparison_path = r'C:\Users\cadel\deep_council_final\logo_comparison.png'
canvas.save(comparison_path, 'PNG')
print(f"\nSaved comparison to: {comparison_path}")
print(f"Resized logos saved to: {output_dir}")
