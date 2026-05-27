#!/usr/bin/env python3

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "ai-slop" / "gpt-generated" / "title-screen"
MONSTER_SOURCE = SOURCE_DIR / "fat-slop-monster-source.png"
TITLE_DIR = ROOT / "graphics" / "title_screen"

FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]

TITLE_BG_PALETTE = [
    (189, 106, 8),    # transparent title-screen backdrop color
    (248, 226, 147),  # belly highlight
    (255, 255, 255),  # clouds / eye whites
    (187, 154, 70),   # belly shade
    (19, 158, 151),   # bright teal body
    (7, 132, 137),    # teal body
    (0, 108, 122),    # body shade
    (0, 89, 111),     # deep teal
    (0, 72, 93),      # darkest teal
    (181, 91, 155),   # wing purple
    (112, 54, 117),   # dark purple
    (0, 46, 66),      # outline
    (180, 230, 172),  # clouds
    (0, 0, 0),        # black outlines
    (234, 120, 168),  # pink tongue / spots
    (0, 74, 98),      # animated marking color overwritten in-game
]

VERSION_PALETTE = [
    (255, 0, 255),
    (255, 255, 255),
    (223, 223, 223),
    (175, 175, 175),
    (109, 109, 109),
    (52, 52, 52),
    (0, 0, 0),
    (240, 240, 255),
    (188, 194, 216),
    (112, 123, 154),
    (24, 30, 52),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (0, 0, 0),
]


def is_key_green(pixel):
    r, g, b, a = pixel
    return a and g > 135 and r < 135 and b < 135


def remove_green_background(image):
    rgba = image.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if is_key_green(px[x, y]):
                px[x, y] = (0, 0, 0, 0)
    bbox = rgba.getbbox()
    if not bbox:
        raise ValueError("monster source became empty after background removal")
    return rgba.crop(bbox)


def nearest_index(color, palette):
    r, g, b = color
    return min(
        range(1, 16),
        key=lambda i: (r - palette[i][0]) ** 2 + (g - palette[i][1]) ** 2 + (b - palette[i][2]) ** 2,
    )


def put_palette(image, palette):
    flat = []
    for color in palette:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    image.putpalette(flat)
    return image


def quantize_to_palette(rgba, palette, transparent_index=0):
    out = Image.new("P", rgba.size, transparent_index)
    put_palette(out, palette)
    opx = out.load()
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a < 96:
                opx[x, y] = transparent_index
            else:
                opx[x, y] = nearest_index((r, g, b), palette)
    return out


def write_jasc_palette(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette)
    path.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def make_monster_bg():
    monster = remove_green_background(Image.open(MONSTER_SOURCE))
    monster.thumbnail((124, 124), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    canvas.alpha_composite(monster, ((128 - monster.width) // 2, 128 - monster.height - 1))
    canvas = ImageOps.posterize(canvas.convert("RGB"), 5).convert("RGBA")
    alpha = Image.open(MONSTER_SOURCE).convert("RGBA")
    alpha = remove_green_background(alpha)
    alpha.thumbnail((124, 124), Image.Resampling.LANCZOS)
    alpha_canvas = Image.new("L", (128, 128), 0)
    alpha_canvas.paste(alpha.getchannel("A"), ((128 - alpha.width) // 2, 128 - alpha.height - 1))
    canvas.putalpha(alpha_canvas)
    indexed = quantize_to_palette(canvas, TITLE_BG_PALETTE)
    indexed.save(TITLE_DIR / "rayquaza.png", bits=4)
    write_jasc_palette(TITLE_DIR / "rayquaza_and_clouds.pal", TITLE_BG_PALETTE)
    return indexed.convert("RGBA")


def load_font(size):
    for font_path in FONT_PATHS:
        path = Path(font_path)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_font(text, max_width, max_height, start_size, stroke_width):
    size = start_size
    while size > 6:
        font = load_font(size)
        bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox(
            (0, 0), text, font=font, stroke_width=stroke_width
        )
        if (bbox[2] - bbox[0]) <= max_width and (bbox[3] - bbox[1]) <= max_height:
            return font
        size -= 1
    return load_font(size)


def centered_text(draw, y, text, font, fill, stroke_fill, stroke_width=1):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    x = (draw.im.size[0] - (bbox[2] - bbox[0])) // 2
    draw.text(
        (x - bbox[0], y - bbox[1]),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def make_version_banner():
    scale = 4
    rgba = Image.new("RGBA", (128 * scale, 32 * scale), (255, 0, 255, 255))
    draw = ImageDraw.Draw(rgba)
    font_top = fit_font("AI SLOP", 120 * scale, 15 * scale, 17 * scale, 1 * scale)
    font_bottom = fit_font("VERSION", 120 * scale, 13 * scale, 15 * scale, 1 * scale)

    for dx, dy, fill in ((3, 4, (52, 52, 52, 255)), (2, 3, (109, 109, 109, 255))):
        centered_text(draw, 1 * scale + dy, "AI SLOP", font_top, fill, (0, 0, 0, 255), 1 * scale)
        centered_text(draw, 17 * scale + dy, "VERSION", font_bottom, fill, (0, 0, 0, 255), 1 * scale)

    centered_text(draw, 1 * scale, "AI SLOP", font_top, (255, 255, 255, 255), (0, 0, 0, 255), 1 * scale)
    centered_text(draw, 17 * scale, "VERSION", font_bottom, (255, 255, 255, 255), (0, 0, 0, 255), 1 * scale)
    rgba = rgba.resize((128, 32), Image.Resampling.LANCZOS)
    rgba = ImageOps.posterize(rgba.convert("RGB"), 5).convert("RGBA")
    mask = Image.new("L", rgba.size, 255)
    px = rgba.load()
    mpx = mask.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if r > 230 and g < 40 and b > 230:
                mpx[x, y] = 0
    rgba.putalpha(mask)
    indexed = quantize_to_palette(rgba, VERSION_PALETTE)
    indexed.save(TITLE_DIR / "emerald_version.png", transparency=0, bits=8)
    return indexed.convert("RGBA")


def make_preview(monster, version):
    preview = Image.new("RGBA", (240, 160), (0, 112, 132, 255))
    draw = ImageDraw.Draw(preview)
    for y in range(160):
        c = (0, 79 + y // 5, 130 - y // 9, 255)
        draw.line((0, y, 240, y), fill=c)

    clouds = Image.open(TITLE_DIR / "clouds.png").convert("RGBA")
    clouds = clouds.resize((256, 112), Image.Resampling.NEAREST)
    preview.alpha_composite(clouds, (-8, 40))

    big_monster = monster.resize((192, 192), Image.Resampling.NEAREST)
    preview.alpha_composite(big_monster, (24, 18))

    logo = Image.open(TITLE_DIR / "pokemon_logo.png").convert("RGBA").resize((220, 55), Image.Resampling.NEAREST)
    preview.alpha_composite(logo, (10, 12))
    version_preview = version.resize((128, 32), Image.Resampling.NEAREST)
    version_px = version_preview.load()
    for y in range(version_preview.height):
        for x in range(version_preview.width):
            r, g, b, a = version_px[x, y]
            if r > 230 and g < 40 and b > 230:
                version_px[x, y] = (0, 0, 0, 0)
    preview.alpha_composite(version_preview, (56, 62))

    small_font = load_font(10)
    draw.text((88, 112), "PRESS START", font=small_font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    draw.text((42, 145), "AI SLOP PROTOTYPE", font=small_font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    preview.convert("RGB").save(SOURCE_DIR / "final-rom-title-screen-preview.png")


def main():
    monster = make_monster_bg()
    version = make_version_banner()
    make_preview(monster, version)


if __name__ == "__main__":
    main()
