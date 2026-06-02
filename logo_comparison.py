from PIL import Image, ImageDraw, ImageFont
import os

# Directory with logos
logo_dir = r'C:\Users\cadel\deep_council_final'

# Logo files to compare (local files only)
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

# Target size for each logo cell
TARGET_SIZE = 64
GAP = 20
LABEL_HEIGHT = 30

# Calculate grid dimensions
num_logos = len(logos)
cols = 5
rows = (num_logos + cols - 1) // cols

# Calculate canvas size
canvas_width = cols * (TARGET_SIZE + GAP) + GAP
canvas_height = rows * (TARGET_SIZE + GAP + LABEL_HEIGHT) + GAP

# Create white canvas
canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Try to load a font, fallback to default
font = ImageFont.load_default()

# Draw title
draw.text((GAP, 10), "Logo Comparison (All resized to same visual size)", fill=(0, 0, 0))

# Process each logo
for i, (filename, label) in enumerate(logos):
    filepath = os.path.join(logo_dir, filename)
    if not os.path.exists(filepath):
        print(f"Missing: {filepath}")
        continue
    
    # Load image
    try:
        img = Image.open(filepath)
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        continue
    
    # Calculate position in grid
    col = i % cols
    row = i // cols
    x = GAP + col * (TARGET_SIZE + GAP)
    y = GAP + 40 + row * (TARGET_SIZE + GAP + LABEL_HEIGHT)
    
    # Resize to fit in TARGET_SIZE while maintaining aspect ratio
    img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    
    # Create a white background square
    cell = Image.new('RGB', (TARGET_SIZE, TARGET_SIZE), (255, 255, 255))
    
    # Paste the logo centered
    offset_x = (TARGET_SIZE - img.width) // 2
    offset_y = (TARGET_SIZE - img.height) // 2
    
    if img.mode == 'RGBA':
        cell.paste(img, (offset_x, offset_y), img)
    else:
        cell.paste(img, (offset_x, offset_y))
    
    # Draw border around cell
    draw.rectangle([x, y, x + TARGET_SIZE, y + TARGET_SIZE], outline=(200, 200, 200), width=1)
    
    # Paste onto canvas
    canvas.paste(cell, (x, y))
    
    # Draw label
    label_y = y + TARGET_SIZE + 5
    draw.text((x, label_y), label, fill=(0, 0, 0))
    
    # Draw original dimensions
    dim_text = f"{img.width}x{img.height}"
    draw.text((x, label_y + 14), dim_text, fill=(100, 100, 100))

# Save
output_path = r'C:\Users\cadel\deep_council_final\logo_comparison.png'
canvas.save(output_path, 'PNG')
print(f"Saved comparison to: {output_path}")
print(f"Canvas size: {canvas_width}x{canvas_height}")
