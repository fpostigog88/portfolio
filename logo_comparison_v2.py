from PIL import Image, ImageDraw, ImageFont
import os

logo_dir = r'C:\Users\cadel\deep_council_final'
output_dir = r'C:\Users\cadel\deep_council_final\logos_resized'
os.makedirs(output_dir, exist_ok=True)

# Icons without text (new versions)
icon_logos = [
    ('logo_uc_chile_icon.png', 'UC Chile'),
    ('logo_claude_icon.png', 'Claude'),
    ('logo_fireworks_icon.png', 'Fireworks'),
    ('logo_qwen_icon.png', 'Qwen'),
    ('logo_discord_icon.png', 'Discord'),
    ('logo_windows_icon.png', 'Windows'),
]

# Old versions (with text)
old_logos = [
    ('logo_uc.png', 'UC Chile (old)'),
    ('logo_claude.png', 'Claude (old)'),
    ('logo_fireworks.png', 'Fireworks (old)'),
    ('logo_qwen.png', 'Qwen (old)'),
    ('logo_discord.png', 'Discord (old)'),
    ('logo_windows.png', 'Windows (old)'),
]

TARGET_SIZE = 64
GAP = 20
LABEL_HEIGHT = 40

# Create comparison canvas
num_logos = len(icon_logos)
cols = 6
rows = 2

canvas_width = cols * (TARGET_SIZE + GAP) + GAP
canvas_height = rows * (TARGET_SIZE + GAP + LABEL_HEIGHT) + GAP + 60

canvas = Image.new('RGB', (canvas_width, canvas_height), (245, 245, 240))
draw = ImageDraw.Draw(canvas)

draw.text((GAP, 15), "Logo Comparison: OLD (top) vs NEW icon-only (bottom)", fill=(30, 30, 30))

# Process old logos (top row)
for i, (filename, label) in enumerate(old_logos):
    filepath = os.path.join(logo_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    try:
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    except:
        continue
    
    orig_w, orig_h = img.size
    img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    
    col = i % cols
    x = GAP + col * (TARGET_SIZE + GAP)
    y = GAP + 50
    
    draw.rectangle([x, y, x + TARGET_SIZE, y + TARGET_SIZE], fill=(255, 255, 255), outline=(180, 180, 180))
    
    if img.mode == 'RGBA':
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2), img)
    else:
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2))
    
    label_y = y + TARGET_SIZE + 8
    draw.text((x, label_y), label, fill=(100, 100, 100))
    draw.text((x, label_y + 14), f"{orig_w}x{orig_h}", fill=(150, 150, 150))

# Process new icons (bottom row)
for i, (filename, label) in enumerate(icon_logos):
    filepath = os.path.join(logo_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    try:
        img = Image.open(filepath)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
    except:
        continue
    
    orig_w, orig_h = img.size
    img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    
    # Save individual resized logo
    resized_path = os.path.join(output_dir, f"{label.lower().replace(' ', '_')}_64.png")
    resized_img = Image.new('RGBA', (TARGET_SIZE, TARGET_SIZE), (255, 255, 255, 0))
    offset_x = (TARGET_SIZE - img.width) // 2
    offset_y = (TARGET_SIZE - img.height) // 2
    if img.mode == 'RGBA':
        resized_img.paste(img, (offset_x, offset_y), img)
    else:
        resized_img.paste(img, (offset_x, offset_y))
    resized_img.save(resized_path, 'PNG')
    
    col = i % cols
    x = GAP + col * (TARGET_SIZE + GAP)
    y = GAP + 50 + TARGET_SIZE + GAP + LABEL_HEIGHT + 20
    
    draw.rectangle([x, y, x + TARGET_SIZE, y + TARGET_SIZE], fill=(255, 255, 255), outline=(0, 150, 0))
    
    if img.mode == 'RGBA':
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2), img)
    else:
        canvas.paste(img, (x + (TARGET_SIZE - img.width) // 2, y + (TARGET_SIZE - img.height) // 2))
    
    label_y = y + TARGET_SIZE + 8
    draw.text((x, label_y), label, fill=(0, 150, 0))
    draw.text((x, label_y + 14), f"{orig_w}x{orig_h}", fill=(100, 100, 100))

comparison_path = r'C:\Users\cadel\deep_council_final\logo_comparison_v2.png'
canvas.save(comparison_path, 'PNG')
print(f"Saved comparison to: {comparison_path}")
