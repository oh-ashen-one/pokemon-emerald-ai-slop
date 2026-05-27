from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]

PALETTE = [
    (0, 0, 0),
    (24, 24, 32),
    (248, 248, 240),
    (232, 58, 70),
    (252, 180, 54),
    (78, 195, 92),
    (58, 144, 236),
    (150, 86, 214),
    (248, 104, 184),
    (72, 220, 212),
    (126, 84, 48),
    (160, 160, 160),
    (96, 96, 104),
    (250, 236, 124),
    (50, 120, 74),
    (120, 52, 42),
]


MONS = {
    "shroomish": {"primary": 5, "secondary": 13, "accent": 8, "shape": "mushroom"},
    "numel": {"primary": 4, "secondary": 3, "accent": 13, "shape": "camel"},
    "corphish": {"primary": 6, "secondary": 3, "accent": 9, "shape": "crab"},
    "zigzagoon": {"primary": 11, "secondary": 6, "accent": 3, "shape": "video"},
    "poochyena": {"primary": 12, "secondary": 10, "accent": 8, "shape": "dog"},
    "wurmple": {"primary": 8, "secondary": 5, "accent": 13, "shape": "bug"},
    "ralts": {"primary": 2, "secondary": 9, "accent": 7, "shape": "bot"},
    "lotad": {"primary": 14, "secondary": 6, "accent": 13, "shape": "duck"},
    "seedot": {"primary": 10, "secondary": 5, "accent": 8, "shape": "seed"},
    "taillow": {"primary": 6, "secondary": 11, "accent": 3, "shape": "bird"},
}

PEOPLE = {
    "prof_birch.png": {"shirt": 2, "pants": 12, "hair": 10, "accent": 3},
    "mom.png": {"shirt": 8, "pants": 6, "hair": 10, "accent": 13},
    "scientist_1.png": {"shirt": 2, "pants": 11, "hair": 1, "accent": 9},
    "boy_2.png": {"shirt": 5, "pants": 6, "hair": 10, "accent": 13},
    "youngster.png": {"shirt": 4, "pants": 6, "hair": 10, "accent": 3},
    "girl_3.png": {"shirt": 8, "pants": 5, "hair": 10, "accent": 9},
    "mart_employee.png": {"shirt": 6, "pants": 2, "hair": 1, "accent": 4},
    "maniac.png": {"shirt": 7, "pants": 12, "hair": 1, "accent": 8},
    "man_3.png": {"shirt": 11, "pants": 6, "hair": 10, "accent": 13},
    "fat_man.png": {"shirt": 4, "pants": 12, "hair": 10, "accent": 3},
    "twin.png": {"shirt": 13, "pants": 8, "hair": 10, "accent": 5},
    "woman_4.png": {"shirt": 9, "pants": 7, "hair": 10, "accent": 13},
    "ninja_boy.png": {"shirt": 1, "pants": 1, "hair": 12, "accent": 9},
    "brendan/walking.png": {"shirt": 3, "pants": 6, "hair": 1, "accent": 13},
    "brendan/running.png": {"shirt": 3, "pants": 6, "hair": 1, "accent": 13},
    "may/walking.png": {"shirt": 8, "pants": 6, "hair": 10, "accent": 13},
    "may/running.png": {"shirt": 8, "pants": 6, "hair": 10, "accent": 13},
    "ruby_sapphire_brendan/walking.png": {"shirt": 3, "pants": 6, "hair": 1, "accent": 13},
    "ruby_sapphire_may/walking.png": {"shirt": 8, "pants": 6, "hair": 10, "accent": 13},
}


def flat_palette():
    data = []
    for rgb in PALETTE:
        data.extend(rgb)
    return data + [0] * (768 - len(data))


def write_pal(path):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in PALETTE)
    path.write_bytes(("\r\n".join(lines) + "\r\n").encode("ascii"))


def canvas(size):
    im = Image.new("P", size, 0)
    im.putpalette(flat_palette())
    return im


def rect(d, xy, fill, outline=1):
    d.rectangle(xy, fill=fill, outline=outline)


def ellipse(d, xy, fill, outline=1):
    d.ellipse(xy, fill=fill, outline=outline)


def monster(d, box, spec, back=False, frame=0):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx = x0 + w // 2
    base = y0 + h - 8
    p, s, a = spec["primary"], spec["secondary"], spec["accent"]
    wobble = frame % 2

    shape = spec["shape"]
    if shape == "mushroom":
        ellipse(d, (cx - 17, base - 30 - wobble, cx + 17, base - 6), p)
        ellipse(d, (cx - 22, base - 40, cx + 22, base - 18), s)
        rect(d, (cx - 17, base - 31, cx + 15, base - 24), 2)
        rect(d, (cx + 8, base - 38, cx + 15, base - 31), a)
    elif shape == "camel":
        ellipse(d, (cx - 24, base - 32, cx + 18, base - 5), p)
        rect(d, (cx - 8, base - 43, cx + 9, base - 24), a)
        rect(d, (cx - 21, base - 40, cx - 9, base - 28), s)
        rect(d, (cx - 18, base - 5, cx - 12, base), 1)
        rect(d, (cx + 8, base - 5, cx + 14, base), 1)
    elif shape == "crab":
        ellipse(d, (cx - 18, base - 29, cx + 18, base - 7), p)
        ellipse(d, (cx - 33, base - 28, cx - 18, base - 12), s)
        ellipse(d, (cx + 18, base - 28, cx + 33, base - 12), s)
        rect(d, (cx - 9, base - 35, cx - 5, base - 29), 2)
        rect(d, (cx + 5, base - 35, cx + 9, base - 29), 2)
        rect(d, (cx - 3, base - 19, cx + 14, base - 15), a)
    elif shape == "video":
        rect(d, (cx - 24, base - 38, cx + 22, base - 9), p)
        rect(d, (cx - 18, base - 32, cx + 16, base - 15), s)
        d.polygon([(cx - 5, base - 30), (cx - 5, base - 17), (cx + 8, base - 24)], fill=a, outline=1)
        for i in range(5):
            rect(d, (cx - 30 + i * 10, base - 46 + (i % 2) * 5, cx - 24 + i * 10, base - 40 + (i % 2) * 5), a if i % 2 else 12)
    elif shape == "dog":
        ellipse(d, (cx - 23, base - 30, cx + 16, base - 8), p)
        ellipse(d, (cx + 6, base - 40, cx + 27, base - 20), s)
        d.polygon([(cx + 10, base - 38), (cx + 16, base - 50), (cx + 21, base - 37)], fill=a, outline=1)
        rect(d, (cx - 18, base - 8, cx - 12, base), 1)
        rect(d, (cx + 10, base - 8, cx + 16, base), 1)
        rect(d, (cx - 27, base - 23, cx - 21, base - 17), a)
    elif shape == "bug":
        for i in range(4):
            ellipse(d, (cx - 23 + i * 12, base - 26 - i % 2, cx - 6 + i * 12, base - 9), p if i % 2 else s)
        rect(d, (cx - 21, base - 33, cx - 13, base - 26), a)
        rect(d, (cx + 14, base - 34, cx + 22, base - 27), a)
    elif shape == "bot":
        rect(d, (cx - 15, base - 38, cx + 15, base - 11), p)
        rect(d, (cx - 19, base - 45, cx + 19, base - 36), s)
        rect(d, (cx - 8, base - 30, cx - 3, base - 25), a)
        rect(d, (cx + 3, base - 30, cx + 8, base - 25), a)
        rect(d, (cx - 10, base - 19, cx + 10, base - 16), 1)
    elif shape == "duck":
        ellipse(d, (cx - 19, base - 30, cx + 18, base - 7), p)
        ellipse(d, (cx - 8, base - 42, cx + 13, base - 24), s)
        rect(d, (cx + 12, base - 34, cx + 26, base - 29), a)
        rect(d, (cx - 15, base - 44, cx + 18, base - 38), 5)
    elif shape == "seed":
        ellipse(d, (cx - 15, base - 35, cx + 15, base - 7), p)
        d.polygon([(cx - 16, base - 31), (cx, base - 48), (cx + 16, base - 31)], fill=s, outline=1)
        rect(d, (cx - 18, base - 21, cx - 11, base - 15), a)
        rect(d, (cx + 11, base - 23, cx + 18, base - 17), a)
    elif shape == "bird":
        ellipse(d, (cx - 15, base - 32, cx + 14, base - 12), p)
        d.polygon([(cx - 13, base - 26), (cx - 33, base - 19), (cx - 10, base - 14)], fill=s, outline=1)
        d.polygon([(cx + 11, base - 25), (cx + 31, base - 18), (cx + 9, base - 13)], fill=s, outline=1)
        rect(d, (cx + 12, base - 29, cx + 25, base - 24), a)

    if not back:
        rect(d, (cx - 7, base - 25, cx - 4, base - 22), 1)
        rect(d, (cx + 4, base - 25, cx + 7, base - 22), 1)
    else:
        rect(d, (cx - 18, base - 16, cx + 18, base - 12), 12)


def draw_mon_file(path, spec, kind):
    if not path.exists():
        return
    size = Image.open(path).size
    im = canvas(size)
    d = ImageDraw.Draw(im)

    if "overworld" in kind:
        for i, x in enumerate(range(0, size[0], 32)):
            monster(d, (x, 0, x + 32, min(32, size[1])), spec, frame=i)
    elif "icon" in kind:
        for i, y in enumerate(range(0, size[1], 32)):
            monster(d, (0, y, min(32, size[0]), y + 32), spec, frame=i)
    elif "front" in kind:
        frame_h = 64
        for i, y in enumerate(range(0, size[1], frame_h)):
            monster(d, (0, y, size[0], min(y + frame_h, size[1])), spec, frame=i)
    elif "back" in kind:
        monster(d, (0, 0, size[0], size[1]), spec, back=True)
    else:
        monster(d, (0, 0, size[0], size[1]), spec)

    im.save(path)


def draw_person_file(path, style):
    if not path.exists():
        return
    size = Image.open(path).size
    im = canvas(size)
    d = ImageDraw.Draw(im)
    frame_w = 16
    skin = 13
    for i, x in enumerate(range(0, size[0], frame_w)):
        step = (i % 3) - 1
        cx = x + frame_w // 2
        ellipse(d, (cx - 4, 2, cx + 4, 10), skin)
        rect(d, (cx - 5, 1, cx + 5, 5), style["hair"])
        rect(d, (cx - 5, 10, cx + 5, 20), style["shirt"])
        rect(d, (cx - 7, 12, cx - 5, 18), style["accent"])
        rect(d, (cx + 5, 12, cx + 7, 18), style["accent"])
        rect(d, (cx - 5, 20, cx - 1, 29 + step), style["pants"])
        rect(d, (cx + 1, 20, cx + 5, 29 - step), style["pants"])
        rect(d, (cx - 6, 29 + step, cx - 1, 31 + step), 1)
        rect(d, (cx + 1, 29 - step, cx + 6, 31 - step), 1)
        rect(d, (cx - 2, 6, cx - 1, 7), 1)
        rect(d, (cx + 2, 6, cx + 3, 7), 1)
    im.save(path)


def main():
    for mon, spec in MONS.items():
        base = ROOT / "graphics" / "pokemon" / mon
        for png in base.glob("*.png"):
            if png.name.startswith("footprint"):
                continue
            draw_mon_file(png, spec, png.stem)
        for pal_name in [
            "normal.pal",
            "normal_gba.pal",
            "shiny.pal",
            "shiny_gba.pal",
            "overworld_normal.pal",
            "overworld_shiny.pal",
        ]:
            pal = base / pal_name
            if pal.exists():
                write_pal(pal)

    people_dir = ROOT / "graphics" / "object_events" / "pics" / "people"
    for rel, style in PEOPLE.items():
        draw_person_file(people_dir / rel, style)


if __name__ == "__main__":
    main()
