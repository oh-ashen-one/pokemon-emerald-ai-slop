from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "ai-slop" / "gpt-generated" / "characters"

CHARACTERS = {
    "prototype-lab-lead": {
        "source": "prototype-lab-lead-source.png",
        "intro": "graphics/birch_speech/birch.png",
        "overworld": "graphics/object_events/pics/people/prof_birch.png",
    },
    "vibe-coder-boy": {
        "source": "vibe-coder-boy-source.png",
        "front": "graphics/trainers/front_pics/brendan.png",
        "back": "graphics/trainers/back_pics/brendan.png",
        "trainer_pal": "graphics/trainers/palettes/brendan.pal",
        "overworld": "graphics/object_events/pics/people/brendan/walking.png",
        "running": "graphics/object_events/pics/people/brendan/running.png",
        "object_pal": "graphics/object_events/palettes/brendan.pal",
        "reflection_pal": "graphics/object_events/palettes/brendan_reflection.pal",
    },
    "actual-coder-girl": {
        "source": "actual-coder-girl-source.png",
        "front": "graphics/trainers/front_pics/may.png",
        "back": "graphics/trainers/back_pics/may.png",
        "trainer_pal": "graphics/trainers/palettes/may.pal",
        "overworld": "graphics/object_events/pics/people/may/walking.png",
        "running": "graphics/object_events/pics/people/may/running.png",
        "object_pal": "graphics/object_events/palettes/may.pal",
        "reflection_pal": "graphics/object_events/palettes/may_reflection.pal",
    },
}


def color_distance(a, b):
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(3)) ** 0.5


def remove_connected_chroma(image):
    rgba = image.convert("RGBA")
    px = rgba.load()
    width, height = rgba.size
    corners = [px[0, 0], px[width - 1, 0], px[0, height - 1], px[width - 1, height - 1]]
    key = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
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
        is_green_key = g > 145 and r < 95 and b < 95
        if a == 0 or color_distance((r, g, b), key) < 95 or is_green_key:
            px[x, y] = (0, 0, 0, 0)
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    bbox = rgba.getbbox()
    if not bbox:
        raise ValueError("source image became empty after background removal")
    return rgba.crop(bbox)


def fit_subject(subject, size, scale=0.94, y_bias=0):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    sprite = subject.copy()
    sprite.thumbnail((int(size[0] * scale), int(size[1] * scale)), Image.Resampling.LANCZOS)
    x = (size[0] - sprite.width) // 2
    y = max(0, size[1] - sprite.height - y_bias)
    canvas.alpha_composite(sprite, (x, y))
    return canvas


def make_back_sheet(front_frame):
    base = ImageOps.mirror(front_frame)
    base = ImageEnhance.Brightness(base).enhance(0.74)
    base = ImageEnhance.Contrast(base).enhance(1.08)
    sheet = Image.new("RGBA", (64, 256), (0, 0, 0, 0))
    for i in range(4):
        sheet.alpha_composite(ImageChops.offset(base, 0, i % 2), (0, i * 64))
    return sheet


def make_overworld_sheet(subject):
    base = fit_subject(subject, (16, 32), scale=0.92, y_bias=1)
    sheet = Image.new("RGBA", (144, 32), (0, 0, 0, 0))
    for i in range(9):
        step = (i % 3) - 1
        bob = 1 if i in (1, 4, 7) else 0
        sheet.alpha_composite(ImageChops.offset(base, step, bob), (i * 16, 0))
    return sheet


def quantize_rgba(image):
    hard_mask = image.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    rgb = Image.new("RGB", image.size, (255, 0, 255))
    rgb.paste(image.convert("RGB"), mask=hard_mask)
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

    qpx = quantized.load()
    fpx = final.load()
    apx = image.load()
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
    indexed.save(path, transparency=0, bits=4)
    return palette


def save_preview(previews):
    sheet = Image.new("RGB", (560, 220), (244, 241, 232))
    draw = ImageDraw.Draw(sheet)
    for i, (label, sprite) in enumerate(previews):
        x = 24 + i * 180
        large = sprite.crop((0, 0, 64, 64)).resize((128, 128), Image.Resampling.NEAREST)
        sheet.paste(large, (x + 24, 16), large)
        draw.text((x, 160), label, fill=(20, 20, 20))
    sheet.save(SOURCE_DIR / "final-rom-character-sprites.png")


def main():
    previews = []
    for label, config in CHARACTERS.items():
        subject = remove_connected_chroma(Image.open(SOURCE_DIR / config["source"]))
        front = fit_subject(subject, (64, 64), scale=0.95, y_bias=2)
        palette = None

        if "intro" in config:
            palette = save_indexed(front, ROOT / config["intro"])

        if "front" in config:
            palette = save_indexed(front, ROOT / config["front"])
            save_indexed(make_back_sheet(front), ROOT / config["back"])
            write_pal(ROOT / config["trainer_pal"], palette)

        if "overworld" in config:
            overworld = make_overworld_sheet(subject)
            object_palette = save_indexed(overworld, ROOT / config["overworld"])
            if "running" in config:
                save_indexed(ImageChops.offset(overworld, 0, 1), ROOT / config["running"])
            if "object_pal" in config:
                write_pal(ROOT / config["object_pal"], object_palette)
            if "reflection_pal" in config:
                reflected = [(max(0, r // 2), max(0, g // 2), max(0, b // 2)) for r, g, b in object_palette]
                write_pal(ROOT / config["reflection_pal"], reflected)

        previews.append((label, front))

    save_preview(previews)


if __name__ == "__main__":
    main()
