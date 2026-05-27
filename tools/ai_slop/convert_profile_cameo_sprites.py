#!/usr/bin/env python3

from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "ai-slop" / "gpt-generated" / "characters" / "profile-cameos"
MAGENTA = (255, 0, 255)


CAMEOS = [
    {
        "sheet": "profile-cameos-01.png",
        "row": 0,
        "label": "anon_speaker_youngster",
        "output": "graphics/object_events/pics/people/youngster.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_youngster.pal",
    },
    {
        "sheet": "profile-cameos-01.png",
        "row": 1,
        "label": "cyborg_aqua_grunt",
        "output": "graphics/object_events/pics/people/team_aqua/aqua_member_m.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_aqua_grunt.pal",
    },
    {
        "sheet": "profile-cameos-01.png",
        "row": 2,
        "label": "cyan_lass",
        "output": "graphics/object_events/pics/people/lass.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_lass.pal",
    },
    {
        "sheet": "profile-cameos-02.png",
        "row": 0,
        "label": "star_eyes_boy",
        "output": "graphics/object_events/pics/people/boy_1.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_boy_1.pal",
    },
    {
        "sheet": "profile-cameos-02.png",
        "row": 1,
        "label": "pink_shades_maniac",
        "output": "graphics/object_events/pics/people/maniac.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_maniac.pal",
    },
    {
        "sheet": "profile-cameos-02.png",
        "row": 2,
        "label": "suited_rich_boy",
        "output": "graphics/object_events/pics/people/rich_boy.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_rich_boy.pal",
    },
    {
        "sheet": "profile-cameos-03.png",
        "row": 0,
        "label": "cat_devon_employee",
        "output": "graphics/object_events/pics/people/man_2.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_man_2.pal",
    },
    {
        "sheet": "profile-cameos-03.png",
        "row": 1,
        "label": "nervous_pirate_fisherman",
        "output": "graphics/object_events/pics/people/fisherman.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_fisherman.pal",
    },
    {
        "sheet": "profile-cameos-03.png",
        "row": 2,
        "label": "smug_pirate_bug_catcher",
        "output": "graphics/object_events/pics/people/bug_catcher.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_bug_catcher.pal",
    },
    {
        "sheet": "profile-cameos-04.png",
        "row": 0,
        "label": "blue_elf_wally",
        "output": "graphics/object_events/pics/people/wally.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_wally.pal",
    },
    {
        "sheet": "profile-cameos-04.png",
        "row": 1,
        "label": "white_sci_fi_norman",
        "output": "graphics/object_events/pics/people/gym_leaders/norman.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_norman.pal",
    },
    {
        "sheet": "profile-cameos-04.png",
        "row": 2,
        "label": "dark_sci_fi_girl",
        "output": "graphics/object_events/pics/people/girl_3.png",
        "palette": "graphics/object_events/palettes/ai_slop_cameo_girl_3.pal",
    },
]


def is_green_key(r, g, b):
    return g > 135 and r < 135 and b < 135


def non_green_mask(image):
    px = image.load()
    mask = set()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a and not is_green_key(r, g, b):
                mask.add((x, y))
    return mask


def find_components(image, min_pixels=500):
    mask = non_green_mask(image)
    seen = set()
    boxes = []
    for point in list(mask):
        if point in seen:
            continue
        q = deque([point])
        seen.add(point)
        xs = []
        ys = []
        while q:
            x, y = q.popleft()
            xs.append(x)
            ys.append(y)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) in mask and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        if len(xs) >= min_pixels:
            boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1, len(xs)))
    return boxes


def remove_green(image):
    rgba = image.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a and is_green_key(r, g, b):
                px[x, y] = (0, 0, 0, 0)
    bbox = rgba.getbbox()
    if not bbox:
        raise ValueError("empty sprite after green removal")
    return rgba.crop(bbox)


def grouped_boxes(image):
    boxes = find_components(image)
    rows = []
    for box in sorted(boxes, key=lambda b: (b[1] + b[3]) / 2):
        center_y = (box[1] + box[3]) / 2
        for row in rows:
            if abs(row["center_y"] - center_y) < 120:
                row["boxes"].append(box)
                row["center_y"] = sum((b[1] + b[3]) / 2 for b in row["boxes"]) / len(row["boxes"])
                break
        else:
            rows.append({"center_y": center_y, "boxes": [box]})
    rows = sorted(rows, key=lambda row: row["center_y"])
    if len(rows) != 3 or any(len(row["boxes"]) != 3 for row in rows):
        counts = [len(row["boxes"]) for row in rows]
        raise ValueError(f"expected 3 rows of 3 poses, got {counts}")
    return [sorted(row["boxes"], key=lambda b: b[0]) for row in rows]


def crop_pose(image, box, padding=12):
    x0, y0, x1, y1, _ = box
    crop = image.crop(
        (
            max(0, x0 - padding),
            max(0, y0 - padding),
            min(image.width, x1 + padding),
            min(image.height, y1 + padding),
        )
    )
    return remove_green(crop)


def crop_grid_pose(image, row, col, padding=8):
    cell_w = image.width // 3
    cell_h = image.height // 3
    crop = image.crop(
        (
            max(0, col * cell_w - padding),
            max(0, row * cell_h - padding),
            min(image.width, (col + 1) * cell_w + padding),
            min(image.height, (row + 1) * cell_h + padding),
        )
    )
    return remove_green(crop)


def fit_pose(pose, size=(16, 32), max_height=25):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    sprite = pose.copy()
    sprite.thumbnail((size[0] - 1, max_height), Image.Resampling.LANCZOS)
    canvas.alpha_composite(sprite, ((size[0] - sprite.width) // 2, size[1] - sprite.height - 1))
    return canvas


def foot_shift(frame, direction, foot_y=26):
    shifted = frame.copy()
    lower = frame.crop((0, foot_y, 16, 32))
    shifted.paste(Image.new("RGBA", (16, 32 - foot_y), (0, 0, 0, 0)), (0, foot_y))
    shifted.alpha_composite(ImageChops.offset(lower, direction, 0), (0, foot_y))
    return shifted


def side_stride(frame, direction, foot_y=25):
    shifted = frame.copy()
    lower = frame.crop((0, foot_y, 16, 32))
    shifted.paste(Image.new("RGBA", (16, 32 - foot_y), (0, 0, 0, 0)), (0, foot_y))
    shifted.alpha_composite(ImageChops.offset(lower, direction, 0), (0, foot_y))
    return shifted


def make_sheet(poses):
    front = fit_pose(poses[0])
    back = fit_pose(poses[1])
    side = fit_pose(poses[2])
    left = ImageOps.mirror(side)
    frames = [
        front,
        back,
        left,
        foot_shift(front, -1),
        foot_shift(front, 1),
        foot_shift(back, -1),
        foot_shift(back, 1),
        side_stride(left, -1),
        side_stride(side, 1),
    ]
    sheet = Image.new("RGBA", (144, 32), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.alpha_composite(frame, (i * 16, 0))
    return sheet


def is_magenta_key(color):
    r, g, b = color
    return r > 220 and g < 80 and b > 220


def quantize_rgba(image, colors=15):
    hard_mask = image.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    rgb = Image.new("RGB", image.size, MAGENTA)
    rgb.paste(image.convert("RGB"), mask=hard_mask)
    quantized = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    raw = quantized.getpalette()[: colors * 3]
    palette = [tuple(raw[i : i + 3]) for i in range(0, len(raw), 3)]
    palette = [MAGENTA] + [color for color in palette if not is_magenta_key(color)][:15]
    palette.extend([(0, 0, 0)] * (16 - len(palette)))

    out = Image.new("P", image.size, 0)
    flat = []
    for color in palette:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    out.putpalette(flat)

    qpx = quantized.load()
    opx = out.load()
    apx = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if apx[x, y][3] < 128:
                opx[x, y] = 0
            else:
                opx[x, y] = min(qpx[x, y] + 1, 15)
    return out, palette


def write_jasc_palette(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette[:16])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def load_sources():
    sources = {}
    for sheet in sorted({cameo["sheet"] for cameo in CAMEOS}):
        image = Image.open(SOURCE_DIR / sheet).convert("RGBA")
        sources[sheet] = image
    return sources


def main():
    sources = load_sources()
    preview_rows = []
    for cameo in CAMEOS:
        image = sources[cameo["sheet"]]
        poses = [crop_grid_pose(image, cameo["row"], col) for col in range(3)]
        sheet = make_sheet(poses)
        indexed, palette = quantize_rgba(sheet)
        output = ROOT / cameo["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        indexed.save(output, transparency=0, bits=4)
        write_jasc_palette(ROOT / cameo["palette"], palette)
        preview_rows.append((cameo["label"], indexed.convert("RGBA")))

    preview = Image.new("RGB", (640, len(preview_rows) * 48 + 20), (244, 241, 232))
    draw = ImageDraw.Draw(preview)
    for i, (label, sheet) in enumerate(preview_rows):
        y = 10 + i * 48
        large = sheet.resize((288, 64), Image.Resampling.NEAREST)
        preview.paste(large, (10, y), large)
        draw.text((316, y + 18), label, fill=(20, 20, 20))
    preview.save(SOURCE_DIR / "final-rom-profile-cameo-overworld-sprites.png")


if __name__ == "__main__":
    main()
