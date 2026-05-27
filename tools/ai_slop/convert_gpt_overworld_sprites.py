#!/usr/bin/env python3

from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/ai-slop/gpt-generated/characters/overworld-walking-reference.png"
OUT_PREVIEW = ROOT / "docs/ai-slop/gpt-generated/characters/final-rom-overworld-walking-sprites.png"

MAGENTA = (255, 0, 255)


ROLE_GROUPS = {
    # row, group of three poses in that row
    "vibe_coder_boy": (0, 0),
    "actual_coder_girl": (0, 1),
    "mom": (0, 2),
    "prototype_lab_lead": (1, 0),
    "lab_aide": (1, 1),
    "mart_employee": (1, 2),
    "footprints_man": (2, 0),
    "route_kid": (2, 1),
    "littleroot_vibe_coder": (2, 2),
}

OUTPUTS = {
    "vibe_coder_boy": {
        "paths": [
            "graphics/object_events/pics/people/brendan/walking.png",
            "graphics/object_events/pics/people/brendan/running.png",
        ],
        "custom_palette": [
            MAGENTA,
            (255, 213, 180),
            (230, 164, 132),
            (132, 82, 65),
            (31, 35, 42),
            (50, 57, 70),
            (82, 90, 106),
            (14, 18, 22),
            (94, 80, 56),
            (148, 123, 82),
            (58, 105, 74),
            (97, 156, 99),
            (205, 205, 205),
            (123, 123, 132),
            (255, 255, 255),
            (0, 0, 0),
        ],
        "palettes": [
            "graphics/object_events/palettes/brendan.pal",
            "graphics/object_events/palettes/brendan_reflection.pal",
        ],
    },
    "actual_coder_girl": {
        "paths": [
            "graphics/object_events/pics/people/may/walking.png",
            "graphics/object_events/pics/people/may/running.png",
        ],
        "custom_palette": [
            MAGENTA,
            (255, 213, 180),
            (230, 164, 132),
            (132, 82, 65),
            (70, 43, 28),
            (119, 74, 45),
            (74, 115, 57),
            (115, 164, 82),
            (236, 236, 220),
            (57, 65, 65),
            (32, 41, 49),
            (205, 205, 205),
            (132, 132, 132),
            (82, 82, 82),
            (255, 255, 255),
            (0, 0, 0),
        ],
        "palettes": [
            "graphics/object_events/palettes/may.pal",
            "graphics/object_events/palettes/may_reflection.pal",
        ],
    },
    "mom": {
        "paths": ["graphics/object_events/pics/people/mom.png"],
        "palette": "graphics/object_events/palettes/npc_4.pal",
    },
    "prototype_lab_lead": {
        "paths": ["graphics/object_events/pics/people/prof_birch.png"],
        "palette": "graphics/object_events/palettes/npc_3.pal",
    },
    "lab_aide": {
        "paths": ["graphics/object_events/pics/people/scientist_1.png"],
        "palette": "graphics/object_events/palettes/npc_3.pal",
    },
    "mart_employee": {
        "paths": ["graphics/object_events/pics/people/mart_employee.png"],
        "palette": "graphics/object_events/palettes/npc_1.pal",
    },
    "oldale_girl": {
        "source_role": "actual_coder_girl",
        "paths": ["graphics/object_events/pics/people/girl_3.png"],
        "palette": "graphics/object_events/palettes/npc_2.pal",
    },
    "footprints_man_maniac": {
        "source_role": "footprints_man",
        "paths": ["graphics/object_events/pics/people/maniac.png"],
        "palette": "graphics/object_events/palettes/npc_4.pal",
    },
    "footprints_man_route": {
        "source_role": "footprints_man",
        "paths": ["graphics/object_events/pics/people/man_3.png"],
        "palette": "graphics/object_events/palettes/npc_2.pal",
    },
    "littleroot_fat_man": {
        "source_role": "footprints_man",
        "paths": ["graphics/object_events/pics/people/fat_man.png"],
        "palette": "graphics/object_events/palettes/npc_1.pal",
    },
    "route_kid_youngster": {
        "source_role": "route_kid",
        "paths": ["graphics/object_events/pics/people/youngster.png"],
        "palette": "graphics/object_events/palettes/npc_1.pal",
    },
    "route_kid_boy": {
        "source_role": "route_kid",
        "paths": ["graphics/object_events/pics/people/boy_1.png"],
        "palette": "graphics/object_events/palettes/npc_3.pal",
    },
    "route_kid_twin": {
        "source_role": "route_kid",
        "paths": ["graphics/object_events/pics/people/twin.png"],
        "palette": "graphics/object_events/palettes/npc_2.pal",
    },
    "littleroot_vibe_coder": {
        "paths": [
            "graphics/object_events/pics/people/boy_2.png",
            "graphics/object_events/pics/people/woman_4.png",
        ],
        "palette": "graphics/object_events/palettes/npc_1.pal",
    },
}


def load_jasc_palette(path):
    lines = (ROOT / path).read_text(encoding="ascii").splitlines()
    return [tuple(map(int, line.split())) for line in lines[3:19]]


def write_jasc_palette(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette)
    (ROOT / path).write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def reflection_palette(palette):
    reflected = [palette[0]]
    reflected.extend((r // 2, g // 2, b // 2) for r, g, b in palette[1:])
    return reflected


def non_green_mask(image):
    px = image.load()
    mask = set()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a and not (g > 170 and r < 90 and b < 90):
                mask.add((x, y))
    return mask


def find_pose_boxes(image):
    mask = non_green_mask(image)
    seen = set()
    boxes = []
    for pt in list(mask):
        if pt in seen:
            continue
        q = deque([pt])
        seen.add(pt)
        xs, ys = [], []
        while q:
            x, y = q.popleft()
            xs.append(x)
            ys.append(y)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) in mask and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny))
        if len(xs) > 100:
            boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))

    boxes.sort(key=lambda b: ((b[1] + b[3]) // 2, b[0]))
    rows = [boxes[:9], boxes[9:18], boxes[18:27]]
    return [sorted(row, key=lambda b: b[0]) for row in rows]


def crop_pose(image, box):
    crop = image.crop(box).convert("RGBA")
    px = crop.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b, a = px[x, y]
            if g > 170 and r < 90 and b < 90:
                px[x, y] = (0, 0, 0, 0)
    return crop.crop(crop.getbbox())


def fit_pose(pose, size=(16, 32), max_height=29):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    sprite = pose.copy()
    sprite.thumbnail((size[0] - 1, max_height), Image.Resampling.LANCZOS)
    x = (size[0] - sprite.width) // 2
    y = size[1] - sprite.height - 1
    canvas.alpha_composite(sprite, (x, y))
    return canvas


def make_back(front):
    back = front.copy()
    px = back.load()
    for y in range(4, 18):
        for x in range(3, 13):
            r, g, b, a = px[x, y]
            if a > 0:
                if r > 155 and g > 105 and b > 80:
                    px[x, y] = (max(25, r // 3), max(20, g // 3), max(18, b // 3), a)
                else:
                    px[x, y] = (max(15, int(r * 0.72)), max(15, int(g * 0.72)), max(15, int(b * 0.72)), a)
    return back


def foot_shift(frame, direction):
    shifted = frame.copy()
    lower = frame.crop((0, 22, 16, 32))
    erase = Image.new("RGBA", (16, 10), (0, 0, 0, 0))
    shifted.paste(erase, (0, 22))
    shifted.alpha_composite(ImageChops.offset(lower, direction, 0), (0, 22))
    return shifted


def make_sheet(poses):
    front = fit_pose(poses[0])
    side_a = fit_pose(poses[1])
    side_b = fit_pose(poses[2])
    side_idle = Image.blend(side_a, side_b, 0.35)
    back = make_back(front)

    frames = [
        front,
        back,
        ImageOpsMirror(side_idle),
        foot_shift(front, -1),
        foot_shift(front, 1),
        foot_shift(back, -1),
        foot_shift(back, 1),
        ImageOpsMirror(side_a),
        ImageOpsMirror(side_b),
    ]
    sheet = Image.new("RGBA", (144, 32), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.alpha_composite(frame, (i * 16, 0))
    return sheet


def ImageOpsMirror(image):
    return ImageChops.offset(image.transpose(Image.Transpose.FLIP_LEFT_RIGHT), 0, 0)


def nearest_index(color, palette):
    r, g, b = color
    candidates = range(1, 16)
    return min(candidates, key=lambda i: (r - palette[i][0]) ** 2 + (g - palette[i][1]) ** 2 + (b - palette[i][2]) ** 2)


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


def save_sheet(sheet, path, palette):
    out = quantize_to_palette(sheet, palette)
    out.save(ROOT / path, transparency=0, bits=4)


def main():
    source = Image.open(SOURCE).convert("RGBA")
    boxes = find_pose_boxes(source)
    role_poses = {}
    for role, (row, group) in ROLE_GROUPS.items():
        role_poses[role] = [crop_pose(source, boxes[row][group * 3 + i]) for i in range(3)]

    previews = []
    for role, config in OUTPUTS.items():
        source_role = config.get("source_role", role)
        sheet = make_sheet(role_poses[source_role])
        if "custom_palette" in config:
            palette = config["custom_palette"]
            for palette_path in config.get("palettes", []):
                if palette_path.endswith("_reflection.pal"):
                    write_jasc_palette(palette_path, reflection_palette(palette))
                else:
                    write_jasc_palette(palette_path, palette)
        else:
            palette = load_jasc_palette(config["palette"])

        for path in config["paths"]:
            save_sheet(sheet, path, palette)
        previews.append((role, quantize_to_palette(sheet, palette).convert("RGBA")))

    preview = Image.new("RGB", (520, len(previews) * 52 + 24), (244, 241, 232))
    draw = ImageDraw.Draw(preview)
    for i, (role, sheet) in enumerate(previews):
        y = 12 + i * 52
        preview.paste(sheet.resize((288, 64), Image.Resampling.NEAREST), (12, y), sheet.resize((288, 64), Image.Resampling.NEAREST))
        draw.text((316, y + 18), role, fill=(20, 20, 20))
    preview.save(OUT_PREVIEW)


if __name__ == "__main__":
    main()
