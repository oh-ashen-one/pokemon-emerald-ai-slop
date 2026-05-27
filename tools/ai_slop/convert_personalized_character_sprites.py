#!/usr/bin/env python3

from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "docs" / "ai-slop" / "gpt-generated" / "characters"
TRAINER_SOURCE = SOURCE_DIR / "personalized-trainer-source.png"
OVERWORLD_SOURCE = SOURCE_DIR / "personalized-overworld-reference.png"

MAGENTA = (255, 0, 255)

TRAINER_SOURCES = {
    "vibe-coder-boy": {
        "index": 0,
        "source": "vibe-coder-boy-source.png",
        "front": "graphics/trainers/front_pics/brendan.png",
        "back": "graphics/trainers/back_pics/brendan.png",
        "trainer_pal": "graphics/trainers/palettes/brendan.pal",
    },
    "actual-coder-girl": {
        "index": 1,
        "source": "actual-coder-girl-source.png",
        "front": "graphics/trainers/front_pics/may.png",
        "back": "graphics/trainers/back_pics/may.png",
        "trainer_pal": "graphics/trainers/palettes/may.pal",
    },
    "prototype-lab-lead": {
        "index": 2,
        "source": "prototype-lab-lead-source.png",
        "intro": "graphics/birch_speech/birch.png",
    },
}

OVERWORLD_ROLES = {
    "vibe_coder_boy": 0,
    "actual_coder_girl": 1,
    "prototype_lab_lead": 2,
    "mom": 3,
    "nurse": 4,
    "mart_employee": 5,
}

OVERWORLD_OUTPUTS = {
    "vibe_coder_boy": {
        "paths": [
            "graphics/object_events/pics/people/brendan/walking.png",
            "graphics/object_events/pics/people/brendan/running.png",
        ],
        "max_height": 25,
        "palette_paths": [
            "graphics/object_events/palettes/brendan.pal",
            "graphics/object_events/palettes/brendan_reflection.pal",
        ],
    },
    "actual_coder_girl": {
        "paths": [
            "graphics/object_events/pics/people/may/walking.png",
            "graphics/object_events/pics/people/may/running.png",
        ],
        "max_height": 25,
        "palette_paths": [
            "graphics/object_events/palettes/may.pal",
            "graphics/object_events/palettes/may_reflection.pal",
        ],
    },
    "prototype_lab_lead": {
        "paths": ["graphics/object_events/pics/people/prof_birch.png"],
        "max_height": 27,
        "fixed_palette": "graphics/object_events/palettes/npc_3.pal",
    },
    "mom": {
        "paths": ["graphics/object_events/pics/people/mom.png"],
        "max_height": 27,
        "fixed_palette": "graphics/object_events/palettes/npc_4.pal",
    },
    "nurse": {
        "paths": ["graphics/object_events/pics/people/nurse.png"],
        "max_height": 27,
        "fixed_palette": "graphics/object_events/palettes/npc_1.pal",
    },
    "mart_employee": {
        "paths": ["graphics/object_events/pics/people/mart_employee.png"],
        "max_height": 27,
        "fixed_palette": "graphics/object_events/palettes/npc_1.pal",
    },
}


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


def find_components(image, min_pixels):
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
        raise ValueError("source image became empty after background removal")
    return rgba.crop(bbox)


def crop_box(image, box, padding=18):
    x0, y0, x1, y1, _ = box
    crop = image.crop((
        max(0, x0 - padding),
        max(0, y0 - padding),
        min(image.width, x1 + padding),
        min(image.height, y1 + padding),
    ))
    return remove_green(crop)


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


def quantize_rgba(image, colors=15):
    hard_mask = image.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    rgb = Image.new("RGB", image.size, MAGENTA)
    rgb.paste(image.convert("RGB"), mask=hard_mask)
    quantized = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    raw = quantized.getpalette()[: colors * 3]
    palette = [tuple(raw[i : i + 3]) for i in range(0, len(raw), 3)]
    final_palette = [MAGENTA] + [color for color in palette if not is_magenta_key(color)][:15]
    final_palette.extend([(0, 0, 0)] * (16 - len(final_palette)))

    out = Image.new("P", image.size, 0)
    flat = []
    for color in final_palette:
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
    return out, final_palette


def write_jasc_palette(path, palette):
    palette = sanitize_palette(palette)
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette[:16])
    path.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def load_jasc_palette(path):
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) < 19 or lines[0] != "JASC-PAL":
        raise ValueError(f"unsupported palette format: {path}")
    count = int(lines[2])
    palette = [tuple(map(int, line.split())) for line in lines[3 : 3 + count]]
    palette.extend([(0, 0, 0)] * (16 - len(palette)))
    return palette[:16]


def reflection_palette(palette):
    return [palette[0]] + [(r // 2, g // 2, b // 2) for r, g, b in palette[1:]]


def is_magenta_key(color):
    r, g, b = color
    return r > 220 and g < 80 and b > 220


def sanitize_palette(palette):
    cleaned = list(palette[:16])
    cleaned.extend([(0, 0, 0)] * (16 - len(cleaned)))
    for i in range(1, 16):
        if is_magenta_key(cleaned[i]):
            cleaned[i] = cleaned[i - 1] if not is_magenta_key(cleaned[i - 1]) else (8, 8, 8)
    return cleaned


def save_indexed(image, path):
    indexed, palette = quantize_rgba(image)
    indexed.save(path, transparency=0, bits=4)
    return palette


def nearest_index(color, palette):
    r, g, b = color
    return min(
        range(1, 16),
        key=lambda i: (r - palette[i][0]) ** 2 + (g - palette[i][1]) ** 2 + (b - palette[i][2]) ** 2,
    )


def quantize_to_palette(rgba, palette):
    out = Image.new("P", rgba.size, 0)
    flat = []
    for color in palette:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    out.putpalette(flat)
    opx = out.load()
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = px[x, y]
            if a < 96:
                opx[x, y] = 0
            else:
                opx[x, y] = nearest_index((r, g, b), palette)
    return out


def fit_pose(pose, size=(16, 32), max_height=27):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    sprite = pose.copy()
    sprite.thumbnail((size[0] - 1, max_height), Image.Resampling.LANCZOS)
    canvas.alpha_composite(sprite, ((size[0] - sprite.width) // 2, size[1] - sprite.height - 1))
    return canvas


def foot_shift(frame, direction, foot_y=25, stride=1):
    shifted = frame.copy()
    lower = frame.crop((0, foot_y, 16, 32))
    shifted.paste(Image.new("RGBA", (16, 32 - foot_y), (0, 0, 0, 0)), (0, foot_y))

    # Move only the feet/ankles, not the whole lower body. Shifting from the
    # knees down made tall generated sprites tear apart in-game.
    step = ImageChops.offset(lower, direction * stride, 0)
    shifted.alpha_composite(step, (0, foot_y))
    return shifted


def body_bob(frame, amount):
    return ImageChops.offset(frame, 0, amount)


def side_stride(frame, direction, foot_y=24):
    shifted = frame.copy()
    foot = frame.crop((0, foot_y, 16, 32))
    shifted.paste(Image.new("RGBA", (16, 32 - foot_y), (0, 0, 0, 0)), (0, foot_y))
    shifted.alpha_composite(ImageChops.offset(foot, direction, 0), (0, foot_y))
    return shifted


def make_overworld_sheet(poses, max_height=27, run=False):
    front = fit_pose(poses[0], max_height=max_height)
    back = fit_pose(poses[1], max_height=max_height)
    side = fit_pose(poses[2], max_height=max_height)
    left = ImageOps.mirror(side)
    stride = 1
    foot_y = 26 if max_height <= 25 else 25

    front_step_a = foot_shift(front, -1, foot_y=foot_y, stride=stride)
    front_step_b = foot_shift(front, 1, foot_y=foot_y, stride=stride)
    back_step_a = foot_shift(back, -1, foot_y=foot_y, stride=stride)
    back_step_b = foot_shift(back, 1, foot_y=foot_y, stride=stride)
    left_step = side_stride(left, -1, foot_y=foot_y - 1)
    right_step = side_stride(side, 1, foot_y=foot_y - 1)

    if run:
        front_step_a = body_bob(front_step_a, 1)
        front_step_b = body_bob(front_step_b, 1)
        back_step_a = body_bob(back_step_a, 1)
        back_step_b = body_bob(back_step_b, 1)
        left_step = body_bob(left_step, 1)
        right_step = body_bob(right_step, 1)

    frames = [
        front,
        back,
        left,
        front_step_a,
        front_step_b,
        back_step_a,
        back_step_b,
        left_step,
        right_step,
    ]
    sheet = Image.new("RGBA", (144, 32), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.alpha_composite(frame, (i * 16, 0))
    return sheet


def save_sheet(sheet, path, palette):
    out = quantize_to_palette(sheet, palette)
    out.save(ROOT / path, transparency=0, bits=4)
    return out


def split_trainer_sources():
    image = Image.open(TRAINER_SOURCE).convert("RGBA")
    boxes = sorted(find_components(image, min_pixels=5000), key=lambda b: b[0])
    if len(boxes) != 3:
        raise ValueError(f"expected 3 trainer subjects, found {len(boxes)}")

    sources = {}
    for label, config in TRAINER_SOURCES.items():
        subject = crop_box(image, boxes[config["index"]], padding=24)
        output = SOURCE_DIR / config["source"]
        subject.save(output)
        sources[label] = subject
    return sources


def convert_trainer_sprites(sources):
    previews = []
    for label, config in TRAINER_SOURCES.items():
        front = fit_subject(sources[label], (64, 64), scale=0.95, y_bias=2)
        if "intro" in config:
            save_indexed(front, ROOT / config["intro"])
        else:
            palette = save_indexed(front, ROOT / config["front"])
            save_indexed(make_back_sheet(front), ROOT / config["back"])
            write_jasc_palette(ROOT / config["trainer_pal"], palette)
        previews.append((label, front))

    preview = Image.new("RGB", (560, 220), (244, 241, 232))
    draw = ImageDraw.Draw(preview)
    for i, (label, sprite) in enumerate(previews):
        x = 24 + i * 180
        large = sprite.resize((128, 128), Image.Resampling.NEAREST)
        preview.paste(large, (x + 24, 16), large)
        draw.text((x, 160), label, fill=(20, 20, 20))
    preview.save(SOURCE_DIR / "final-rom-personalized-character-sprites.png")


def grouped_overworld_boxes(image):
    boxes = find_components(image, min_pixels=500)
    rows = []
    for box in sorted(boxes, key=lambda b: (b[1] + b[3]) / 2):
        center_y = (box[1] + box[3]) / 2
        for row in rows:
            if abs(row["center_y"] - center_y) < 110:
                row["boxes"].append(box)
                row["center_y"] = sum((b[1] + b[3]) / 2 for b in row["boxes"]) / len(row["boxes"])
                break
        else:
            rows.append({"center_y": center_y, "boxes": [box]})

    rows = sorted(rows, key=lambda row: row["center_y"])
    if len(rows) != 6 or any(len(row["boxes"]) != 3 for row in rows):
        counts = [len(row["boxes"]) for row in rows]
        raise ValueError(f"expected 6 rows of 3 overworld poses, got {counts}")
    return [sorted(row["boxes"], key=lambda b: b[0]) for row in rows]


def derive_palette(sheet, extra_sheets=()):
    composite = Image.new("RGBA", (sheet.width, sheet.height * (1 + len(extra_sheets))), (0, 0, 0, 0))
    composite.alpha_composite(sheet, (0, 0))
    for i, extra in enumerate(extra_sheets, start=1):
        composite.alpha_composite(extra, (0, sheet.height * i))
    _, palette = quantize_rgba(composite)
    return palette


def convert_overworld_sprites():
    image = Image.open(OVERWORLD_SOURCE).convert("RGBA")
    boxes = grouped_overworld_boxes(image)
    role_poses = {
        role: [crop_box(image, boxes[row][i], padding=8) for i in range(3)]
        for role, row in OVERWORLD_ROLES.items()
    }
    role_sheets = {
        role: make_overworld_sheet(
            poses,
            max_height=OVERWORLD_OUTPUTS.get(role, {}).get("max_height", 27),
        )
        for role, poses in role_poses.items()
    }
    role_run_sheets = {
        role: make_overworld_sheet(
            poses,
            max_height=OVERWORLD_OUTPUTS.get(role, {}).get("max_height", 27),
            run=True,
        )
        for role, poses in role_poses.items()
    }

    previews = []
    for role, config in OVERWORLD_OUTPUTS.items():
        sheet = role_sheets[role]
        if "fixed_palette" in config:
            palette = load_jasc_palette(ROOT / config["fixed_palette"])
        else:
            palette = derive_palette(sheet)

        for palette_path in config.get("palette_paths", []):
            palette_to_write = reflection_palette(palette) if palette_path.endswith("_reflection.pal") else palette
            write_jasc_palette(ROOT / palette_path, palette_to_write)

        indexed = None
        for path in config["paths"]:
            if path.endswith("/running.png"):
                indexed = save_sheet(role_run_sheets[role], path, palette)
            else:
                indexed = save_sheet(sheet, path, palette)
        previews.append((role, indexed.convert("RGBA")))

    preview = Image.new("RGB", (560, len(previews) * 52 + 24), (244, 241, 232))
    draw = ImageDraw.Draw(preview)
    for i, (role, sheet) in enumerate(previews):
        y = 12 + i * 52
        large = sheet.resize((288, 64), Image.Resampling.NEAREST)
        preview.paste(large, (12, y), large)
        draw.text((316, y + 18), role, fill=(20, 20, 20))
    preview.save(SOURCE_DIR / "final-rom-personalized-overworld-sprites.png")


def main():
    trainer_sources = split_trainer_sources()
    convert_trainer_sprites(trainer_sources)
    convert_overworld_sprites()


if __name__ == "__main__":
    main()
