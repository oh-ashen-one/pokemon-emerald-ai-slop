#!/usr/bin/env python3

from pathlib import Path
import struct

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
TILESET_DIR = ROOT / "data/tilesets/secondary/brendans_mays_house"
TILES_PNG = TILESET_DIR / "tiles.png"
METATILES_BIN = TILESET_DIR / "metatiles.bin"
ATTRIBUTES_BIN = TILESET_DIR / "metatile_attributes.bin"
BRENDAN_ROOM_MAP = ROOT / "data/layouts/LittlerootTown_BrendansHouse_2F/map.bin"
PREVIEW_PNG = ROOT / "docs/ai-slop/gpt-generated/rooms/vibe-coder-room-layout-preview.png"

SECONDARY_TILE_BASE = 512
NEW_METATILE_BASE = 0x2C4
NEW_TILE_BASE = 592


def metatile_index(global_id):
    return global_id - 0x200


def tile_rect(abs_tile_id):
    local_id = abs_tile_id - SECONDARY_TILE_BASE
    x = (local_id % 16) * 8
    y = (local_id // 16) * 8
    return x, y, x + 8, y + 8


def write_tile(tiles, abs_tile_id, drawer):
    x0, y0, x1, y1 = tile_rect(abs_tile_id)
    tile = Image.new("P", (8, 8), 0)
    tile.putpalette(tiles.getpalette())
    draw = ImageDraw.Draw(tile)
    drawer(draw)
    tiles.paste(tile, (x0, y0, x1, y1))


def rect(draw, xy, color):
    draw.rectangle(xy, fill=color)


def line(draw, xy, color, width=1):
    draw.line(xy, fill=color, width=width)


def ellipse(draw, xy, color):
    draw.ellipse(xy, fill=color)


def make_dirty_tiles(tiles):
    # Every custom tile is transparent around the prop so layer 2 can sit on top
    # of the existing bedroom floor.
    tile_drawers = [
        # 592-595: open pizza box with cans.
        lambda d: (rect(d, (1, 2, 7, 7), 13), rect(d, (2, 3, 6, 6), 15), line(d, (2, 6, 6, 3), 9)),
        lambda d: (rect(d, (0, 3, 6, 7), 13), rect(d, (1, 4, 5, 6), 10), ellipse(d, (3, 5, 4, 6), 15)),
        lambda d: (rect(d, (2, 0, 4, 6), 6), rect(d, (2, 0, 4, 1), 4), rect(d, (5, 2, 6, 6), 14)),
        lambda d: (rect(d, (0, 0, 6, 4), 12), line(d, (0, 0, 6, 4), 1), rect(d, (4, 3, 7, 6), 9)),
        # 596-599: cable nest and laptop.
        lambda d: (rect(d, (1, 1, 7, 5), 12), rect(d, (2, 2, 6, 4), 13), line(d, (2, 4, 6, 6), 1)),
        lambda d: (line(d, (0, 6, 3, 2, 7, 6), 12), line(d, (1, 1, 7, 1), 1), rect(d, (5, 4, 7, 6), 10)),
        lambda d: (line(d, (0, 2, 4, 6, 7, 3), 12), ellipse(d, (1, 1, 4, 4), 1), ellipse(d, (4, 3, 7, 6), 1)),
        lambda d: (line(d, (0, 5, 2, 1, 5, 4, 7, 1), 12), rect(d, (0, 6, 3, 7), 15), rect(d, (4, 5, 6, 7), 6)),
        # 600-603: laundry pile.
        lambda d: (ellipse(d, (1, 2, 7, 7), 5), ellipse(d, (0, 4, 4, 7), 6), rect(d, (3, 1, 6, 4), 14)),
        lambda d: (ellipse(d, (0, 1, 7, 7), 4), rect(d, (1, 2, 6, 5), 12), line(d, (1, 5, 6, 2), 1)),
        lambda d: (ellipse(d, (0, 0, 6, 5), 7), rect(d, (2, 3, 7, 7), 15), line(d, (1, 3, 6, 6), 2)),
        lambda d: (ellipse(d, (1, 0, 7, 6), 6), rect(d, (0, 3, 4, 7), 8), line(d, (0, 7, 7, 1), 1)),
        # 604-607: trash bag, crumpled paper, takeout.
        lambda d: (ellipse(d, (1, 1, 7, 7), 12), rect(d, (3, 0, 5, 2), 1), line(d, (2, 3, 6, 6), 2)),
        lambda d: (ellipse(d, (0, 3, 4, 7), 4), ellipse(d, (4, 2, 7, 5), 5), rect(d, (5, 5, 7, 7), 15)),
        lambda d: (rect(d, (1, 2, 7, 6), 13), line(d, (1, 2, 7, 6), 1), rect(d, (2, 3, 5, 4), 9)),
        lambda d: (ellipse(d, (1, 2, 7, 7), 12), rect(d, (0, 5, 3, 7), 15), line(d, (1, 1, 6, 6), 1)),
        # 608-623: four dirty rug/stain pieces.
        lambda d: (ellipse(d, (1, 2, 7, 7), 10), ellipse(d, (0, 5, 3, 7), 7), rect(d, (5, 1, 7, 3), 8)),
        lambda d: (ellipse(d, (0, 1, 6, 7), 10), rect(d, (1, 4, 7, 6), 7), ellipse(d, (5, 0, 7, 2), 15)),
        lambda d: (ellipse(d, (2, 0, 7, 7), 7), rect(d, (0, 3, 4, 6), 10), ellipse(d, (1, 1, 3, 3), 8)),
        lambda d: (ellipse(d, (0, 0, 6, 6), 7), rect(d, (3, 4, 7, 7), 10), ellipse(d, (5, 2, 7, 4), 15)),
        lambda d: (rect(d, (0, 0, 7, 7), 10), ellipse(d, (1, 2, 5, 7), 7), ellipse(d, (5, 1, 7, 4), 8)),
        lambda d: (rect(d, (0, 0, 7, 7), 10), ellipse(d, (0, 1, 6, 6), 7), rect(d, (5, 5, 7, 7), 8)),
        lambda d: (rect(d, (0, 0, 7, 7), 10), ellipse(d, (2, 0, 7, 6), 7), ellipse(d, (0, 5, 3, 7), 8)),
        lambda d: (rect(d, (0, 0, 7, 7), 10), ellipse(d, (0, 0, 6, 5), 7), rect(d, (4, 5, 7, 7), 8)),
        # 624-627: floor keyboard and bugged prompt notes.
        lambda d: (rect(d, (0, 3, 7, 6), 2), line(d, (1, 4, 6, 4), 4), line(d, (1, 5, 6, 5), 4)),
        lambda d: (rect(d, (1, 2, 7, 5), 12), line(d, (2, 3, 6, 3), 10), line(d, (2, 4, 5, 4), 14)),
        lambda d: (rect(d, (2, 1, 6, 5), 11), line(d, (2, 1, 6, 5), 1), rect(d, (0, 5, 3, 7), 15)),
        lambda d: (rect(d, (0, 2, 5, 6), 15), line(d, (0, 2, 5, 6), 1), rect(d, (5, 0, 7, 3), 11)),
    ]

    for offset, drawer in enumerate(tile_drawers):
        write_tile(tiles, NEW_TILE_BASE + offset, drawer)


def load_words(path):
    data = path.read_bytes()
    return list(struct.unpack("<" + "H" * (len(data) // 2), data))


def save_words(path, words):
    path.write_bytes(struct.pack("<" + "H" * len(words), *words))


def layer_entry(abs_tile_id, palette):
    return (palette << 12) | abs_tile_id


def make_metatile(base_floor, tile_ids, palette=8):
    return base_floor[:4] + [layer_entry(t, palette) for t in tile_ids]


def extend_metatiles():
    words = load_words(METATILES_BIN)
    attrs = load_words(ATTRIBUTES_BIN)
    first_new_index = metatile_index(NEW_METATILE_BASE)
    # Keep the tool re-runnable while developing the room.
    words = words[: first_new_index * 8]
    attrs = attrs[:first_new_index]

    base_floor = words[metatile_index(0x201) * 8 : metatile_index(0x201) * 8 + 8]
    floor_attr = attrs[metatile_index(0x201)]

    while len(words) // 8 < first_new_index:
        words.extend(base_floor)
        attrs.append(floor_attr)

    tile_groups = [
        [592, 593, 594, 595],  # pizza/cans
        [596, 597, 598, 599],  # cables/laptop
        [600, 601, 602, 603],  # laundry
        [604, 605, 606, 607],  # trash
        [608, 609, 612, 613],  # dirty rug top-left
        [610, 611, 614, 615],  # dirty rug top-right
        [616, 617, 620, 621],  # dirty rug bottom-left
        [618, 619, 622, 623],  # dirty rug bottom-right
        [624, 625, 626, 627],  # keyboard/prompt notes
    ]

    for group in tile_groups:
        words.extend(make_metatile(base_floor, group))
        attrs.append(floor_attr)

    save_words(METATILES_BIN, words)
    save_words(ATTRIBUTES_BIN, attrs)


def patch_room_map():
    raw = BRENDAN_ROOM_MAP.read_bytes()
    cells = list(struct.unpack("<72H", raw))

    placements = {
        (3, 3): 0x2C4,  # pizza/cans near the desk path
        (8, 3): 0x2C5,  # cable nest by the wall
        (3, 5): 0x2C6,  # laundry heap
        (1, 6): 0x2C7,  # trash near the bed
        (4, 4): 0x2C8,
        (5, 4): 0x2C9,
        (4, 5): 0x2CA,
        (5, 5): 0x2CB,
        (6, 6): 0x2CC,  # keyboard/prompt notes
    }

    for (x, y), metatile in placements.items():
        i = y * 9 + x
        cells[i] = (cells[i] & ~0x03FF) | metatile

    BRENDAN_ROOM_MAP.write_bytes(struct.pack("<72H", *cells))


def render_preview():
    tiles = Image.open(TILES_PNG)
    palettes = []
    for path in sorted((TILESET_DIR / "palettes").glob("*.pal")):
        lines = path.read_text().splitlines()[3:]
        palettes.append([tuple(map(int, line.split())) for line in lines[:16]])
    metatile_words = load_words(METATILES_BIN)

    raw = BRENDAN_ROOM_MAP.read_bytes()
    cells = list(struct.unpack("<72H", raw))
    preview = Image.new("RGB", (9 * 16, 8 * 16), palettes[0][0])

    def draw_entry(entry, ox, oy, transparent):
        tile_id = entry & 0x03FF
        palette_id = (entry >> 12) & 0x0F
        if tile_id < SECONDARY_TILE_BASE:
            return
        local_id = tile_id - SECONDARY_TILE_BASE
        sx = (local_id % 16) * 8
        sy = (local_id // 16) * 8
        hflip = bool(entry & 0x0400)
        vflip = bool(entry & 0x0800)
        for py in range(8):
            for px in range(8):
                tx = 7 - px if hflip else px
                ty = 7 - py if vflip else py
                color_index = tiles.getpixel((sx + tx, sy + ty))
                if transparent and color_index == 0:
                    continue
                preview.putpixel((ox + px, oy + py), palettes[palette_id][color_index])

    for y in range(8):
        for x in range(9):
            gid = cells[y * 9 + x] & 0x3FF
            i = metatile_index(gid) * 8
            if i < 0 or i + 8 > len(metatile_words):
                continue
            entries = metatile_words[i : i + 8]
            ox, oy = x * 16, y * 16
            for layer_start, transparent in ((0, False), (4, True)):
                draw_entry(entries[layer_start], ox, oy, transparent)
                draw_entry(entries[layer_start + 1], ox + 8, oy, transparent)
                draw_entry(entries[layer_start + 2], ox, oy + 8, transparent)
                draw_entry(entries[layer_start + 3], ox + 8, oy + 8, transparent)

    PREVIEW_PNG.parent.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW_PNG)


def main():
    tiles = Image.open(TILES_PNG)
    if tiles.mode != "P":
        raise RuntimeError(f"Expected indexed PNG, got {tiles.mode}")
    make_dirty_tiles(tiles)
    tiles.save(TILES_PNG)
    extend_metatiles()
    patch_room_map()
    render_preview()


if __name__ == "__main__":
    main()
