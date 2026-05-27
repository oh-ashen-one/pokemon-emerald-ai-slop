from pathlib import Path
from collections import deque

from PIL import Image, ImageChops, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "ai-slop" / "gpt-generated" / "pokemon"

MONS = {
    "badvid": "zigzagoon",
    "promptrot": "shroomish",
    "tokenburn": "numel",
    "slopjet": "corphish",
    "bootdog": "poochyena",
    "bugfixme": "wurmple",
    "chatbot": "ralts",
    "dataduck": "lotad",
    "seedbug": "seedot",
    "jpegull": "taillow",
}

PALETTE_FILES = (
    "normal.pal",
    "normal_gba.pal",
    "shiny.pal",
    "shiny_gba.pal",
    "overworld_normal.pal",
    "overworld_shiny.pal",
)

PNG_TARGETS = (
    "anim_front.png",
    "anim_front_gba.png",
    "back.png",
    "back_gba.png",
    "icon.png",
    "icon_gba.png",
    "overworld.png",
)


def color_distance(a, b):
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(3)) ** 0.5


def remove_connected_background(image):
    rgba = image.convert("RGBA")
    px = rgba.load()
    width, height = rgba.size
    corners = [px[0, 0], px[width - 1, 0], px[0, height - 1], px[width - 1, height - 1]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    visited = set()
    q = deque()

    for x in range(width):
        q.append((x, 0))
        q.append((x, height - 1))
    for y in range(height):
        q.append((0, y))
        q.append((width - 1, y))

    while q:
        x, y = q.popleft()
        if (x, y) in visited or not (0 <= x < width and 0 <= y < height):
            continue
        visited.add((x, y))
        r, g, b, a = px[x, y]
        bright = max(r, g, b)
        channel_spread = max(r, g, b) - min(r, g, b)
        if a == 0 or color_distance((r, g, b), bg) < 42 or (bright > 205 and channel_spread < 42):
            px[x, y] = (0, 0, 0, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    bbox = rgba.getbbox()
    if not bbox:
        raise ValueError("source image became empty after background removal")
    return rgba.crop(bbox)


def fit_subject(subject, size, max_scale, y_bias=0):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    src = subject.copy()
    src.thumbnail((int(size[0] * max_scale), int(size[1] * max_scale)), Image.Resampling.LANCZOS)
    x = (size[0] - src.width) // 2
    y = max(0, size[1] - src.height - y_bias)
    canvas.alpha_composite(src, (x, y))
    return canvas


def make_back(front):
    # Practical back-sprite derivation from the generated concept: use the same
    # silhouette, mirrored and darkened, so it remains recognizable in battle.
    back = ImageOps.mirror(front)
    back = ImageEnhance.Brightness(back).enhance(0.72)
    back = ImageEnhance.Contrast(back).enhance(1.08)
    return back


def make_icon(subject):
    icon = Image.new("RGBA", (32, 64), (0, 0, 0, 0))
    frame = fit_subject(subject, (32, 32), 0.92, y_bias=2)
    icon.alpha_composite(frame, (0, 0))
    icon.alpha_composite(ImageChops.offset(frame, 0, 1), (0, 32))
    return icon


def make_overworld(subject):
    sheet = Image.new("RGBA", (192, 32), (0, 0, 0, 0))
    base = fit_subject(subject, (32, 32), 0.72, y_bias=1)
    for i in range(6):
        frame = ImageChops.offset(base, (i % 3) - 1, 0 if i % 2 else 1)
        sheet.alpha_composite(frame, (i * 32, 0))
    return sheet


def quantize_rgba(image):
    matte = Image.new("RGBA", image.size, (0, 0, 0, 0))
    matte.alpha_composite(image)
    rgb = Image.new("RGB", image.size, (255, 0, 255))
    hard_mask = matte.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    rgb.paste(matte.convert("RGB"), mask=hard_mask)
    quantized = rgb.quantize(colors=15, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()[:45]
    colors = [tuple(palette[i : i + 3]) for i in range(0, len(palette), 3)]
    final_palette = [(255, 0, 255)] + colors[:15]
    final = Image.new("P", image.size, 0)
    flat = []
    for color in final_palette:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    final.putpalette(flat)

    rgba = image.convert("RGBA")
    qpx = quantized.load()
    fpx = final.load()
    apx = rgba.load()
    for y in range(image.height):
        for x in range(image.width):
            if apx[x, y][3] < 128:
                fpx[x, y] = 0
            else:
                fpx[x, y] = min(qpx[x, y] + 1, 15)
    return final, final_palette


def write_pal(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette)
    path.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def save_indexed(image, path):
    indexed, palette = quantize_rgba(image)
    indexed.save(path, transparency=0)
    return palette


def main():
    for slug, species_dir in MONS.items():
        source = SOURCE_DIR / f"{slug}-source.png"
        subject = remove_connected_background(Image.open(source))
        front_frame = fit_subject(subject, (64, 64), 0.92, y_bias=4)
        front_anim = Image.new("RGBA", (64, 128), (0, 0, 0, 0))
        front_anim.alpha_composite(front_frame, (0, 0))
        front_anim.alpha_composite(ImageChops.offset(front_frame, 0, 1), (0, 64))
        back = make_back(front_frame)
        icon = make_icon(subject)
        overworld = make_overworld(subject)

        target_dir = ROOT / "graphics" / "pokemon" / species_dir
        palette = save_indexed(front_anim, target_dir / "anim_front.png")
        save_indexed(front_anim, target_dir / "anim_front_gba.png")
        save_indexed(back, target_dir / "back.png")
        save_indexed(back, target_dir / "back_gba.png")
        save_indexed(icon, target_dir / "icon.png")
        save_indexed(icon, target_dir / "icon_gba.png")
        save_indexed(overworld, target_dir / "overworld.png")

        if species_dir == "numel":
            save_indexed(front_anim, target_dir / "anim_frontf.png")
            save_indexed(back, target_dir / "backf.png")
            save_indexed(overworld, target_dir / "overworldf.png")

        for pal_name in PALETTE_FILES:
            pal_path = target_dir / pal_name
            if pal_path.exists():
                write_pal(pal_path, palette)


if __name__ == "__main__":
    main()
