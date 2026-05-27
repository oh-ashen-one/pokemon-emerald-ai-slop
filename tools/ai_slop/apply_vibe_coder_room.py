#!/usr/bin/env python3

from pathlib import Path
import struct

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
TILESET_DIR = ROOT / "data/tilesets/secondary/brendans_mays_house"
TILES_PNG = TILESET_DIR / "tiles.png"
METATILES_BIN = TILESET_DIR / "metatiles.bin"
ATTRIBUTES_BIN = TILESET_DIR / "metatile_attributes.bin"
PALETTE_15 = TILESET_DIR / "palettes/15.pal"
SOURCE_PNG = ROOT / "docs/ai-slop/gpt-generated/rooms/vibe-coder-bedroom-map-source.png"
BRENDAN_ROOM_MAP = ROOT / "data/layouts/LittlerootTown_BrendansHouse_2F/map.bin"
PREVIEW_PNG = ROOT / "docs/ai-slop/gpt-generated/rooms/vibe-coder-room-layout-preview.png"

SECONDARY_TILE_BASE = 512
ROOM_METATILE_BASE = 0x2C4
ROOM_WIDTH = 9
ROOM_HEIGHT = 8
ROOM_PIXEL_SIZE = (ROOM_WIDTH * 16, ROOM_HEIGHT * 16)

# The original room's upper bits carry the map's elevation/collision metadata.
BASE_ROOM_VALUES = [
    0x0652, 0x0654, 0x0650, 0x0654, 0x0656, 0x0687, 0x060B, 0x060C, 0x060D,
    0x065A, 0x065B, 0x0655, 0x0665, 0x0402, 0x068F, 0x0613, 0x0214, 0x0615,
    0x3262, 0x3263, 0x3278, 0x3266, 0x325D, 0x3278, 0x3206, 0x3205, 0x3207,
    0x327B, 0x327C, 0x327D, 0x3201, 0x3298, 0x3299, 0x3299, 0x329A, 0x3201,
    0x0283, 0x3284, 0x0285, 0x3201, 0x32A0, 0x32A1, 0x32A1, 0x32A2, 0x3201,
    0x428B, 0x068C, 0x428D, 0x0201, 0x32A0, 0x32A1, 0x32A1, 0x32A2, 0x3201,
    0x0204, 0x3201, 0x0201, 0x3201, 0x32A8, 0x32A9, 0x32A9, 0x32AA, 0x3201,
    0x3204, 0x3201, 0x3201, 0x3201, 0x3201, 0x3201, 0x3201, 0x3201, 0x3201,
]

# TRUE means solid. The clear path runs from the lower room into the top-right
# exit, while the bed, desk, trash, laundry, and room edges are blocked.
COLLISION = [
    "#########",
    "#######.#",
    "######..#",
    "#####...#",
    "##....###",
    "##....###",
    "#.....###",
    "#.....###",
]


def load_words(path):
    data = path.read_bytes()
    return list(struct.unpack("<" + "H" * (len(data) // 2), data))


def save_words(path, words):
    path.write_bytes(struct.pack("<" + "H" * len(words), *words))


def crop_room_source():
    source = Image.open(SOURCE_PNG).convert("RGB")
    xs, ys = [], []
    for y in range(source.height):
        for x in range(source.width):
            r, g, b = source.getpixel((x, y))
            if not (r > 245 and g > 245 and b > 245):
                xs.append(x)
                ys.append(y)
    if not xs:
        raise RuntimeError("room source has no non-white pixels")
    bbox = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return source.crop(bbox)


def make_room_image():
    # Downscale once for composition, then quantize. Eight source colors plus a
    # transparent index keeps the final 8x8 tile count inside the free secondary
    # tileset space while preserving the generated room as a coherent image.
    room = crop_room_source()
    room = room.resize((72, 64), Image.Resampling.BICUBIC)
    room = room.resize(ROOM_PIXEL_SIZE, Image.Resampling.NEAREST)
    quantized = room.quantize(colors=8, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return quantized


def palette_from_image(image):
    raw = image.getpalette()[:45]
    colors = [(255, 0, 255)]
    colors.extend(tuple(raw[i:i + 3]) for i in range(0, len(raw), 3))
    while len(colors) < 16:
        colors.append((0, 0, 0))
    return colors[:16]


def write_jasc_palette(path, palette):
    lines = ["JASC-PAL", "0100", "16"]
    lines.extend(f"{r} {g} {b}" for r, g, b in palette)
    path.write_text("\r\n".join(lines) + "\r\n", encoding="ascii", newline="")


def remap_room_to_palette(image):
    out = Image.new("P", image.size, 0)
    raw = image.getpalette()[:45]
    source_colors = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    index_map = {i: i + 1 for i in range(len(source_colors))}
    flat = []
    palette = [(255, 0, 255)] + source_colors
    while len(palette) < 16:
        palette.append((0, 0, 0))
    for color in palette:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    out.putpalette(flat)
    px_in = image.load()
    px_out = out.load()
    for y in range(image.height):
        for x in range(image.width):
            px_out[x, y] = index_map[px_in[x, y]]
    return out


def used_secondary_tiles(words):
    used = set()
    for word in words:
        tile = word & 0x03FF
        if SECONDARY_TILE_BASE <= tile < SECONDARY_TILE_BASE + 512:
            used.add(tile)
    return used


def ensure_tilesheet_capacity(tiles):
    if tiles.height < 256:
        expanded = Image.new("P", (128, 256), 0)
        expanded.putpalette(tiles.getpalette())
        expanded.paste(tiles, (0, 0))
        return expanded
    return tiles


def tile_xy(abs_tile_id):
    local = abs_tile_id - SECONDARY_TILE_BASE
    return (local % 16) * 8, (local // 16) * 8


def write_room_tiles(room_image, metatile_words):
    tiles = ensure_tilesheet_capacity(Image.open(TILES_PNG))
    if tiles.mode != "P":
        raise RuntimeError(f"expected indexed tileset PNG, got {tiles.mode}")

    used = used_secondary_tiles(metatile_words)
    free_tiles = [tile for tile in range(SECONDARY_TILE_BASE, SECONDARY_TILE_BASE + 512) if tile not in used]

    tile_to_abs = {}
    for y in range(0, ROOM_PIXEL_SIZE[1], 8):
        for x in range(0, ROOM_PIXEL_SIZE[0], 8):
            key = room_image.crop((x, y, x + 8, y + 8)).tobytes()
            if key not in tile_to_abs:
                if not free_tiles:
                    raise RuntimeError("not enough free secondary tile slots for converted room")
                tile_to_abs[key] = free_tiles.pop(0)

    for y in range(0, ROOM_PIXEL_SIZE[1], 8):
        for x in range(0, ROOM_PIXEL_SIZE[0], 8):
            tile = room_image.crop((x, y, x + 8, y + 8))
            abs_tile = tile_to_abs[tile.tobytes()]
            tx, ty = tile_xy(abs_tile)
            tiles.paste(tile, (tx, ty))

    tiles.save(TILES_PNG)
    return tile_to_abs


def metatile_index(global_id):
    return global_id - 0x200


def make_room_metatiles(room_image, tile_to_abs):
    words = load_words(METATILES_BIN)
    attrs = load_words(ATTRIBUTES_BIN)

    first_new_index = metatile_index(ROOM_METATILE_BASE)
    words = words[: first_new_index * 8]
    attrs = attrs[:first_new_index]

    while len(words) // 8 < first_new_index:
        words.extend([0] * 8)
        attrs.append(0)

    def entry(px, py):
        key = room_image.crop((px, py, px + 8, py + 8)).tobytes()
        return (15 << 12) | tile_to_abs[key]

    for y in range(ROOM_HEIGHT):
        for x in range(ROOM_WIDTH):
            px, py = x * 16, y * 16
            words.extend([
                entry(px, py),
                entry(px + 8, py),
                entry(px, py + 8),
                entry(px + 8, py + 8),
                0, 0, 0, 0,
            ])
            attrs.append(4096 if COLLISION[y][x] == "#" else 0)

    save_words(METATILES_BIN, words)
    save_words(ATTRIBUTES_BIN, attrs)


def patch_room_map():
    cells = []
    for i, base in enumerate(BASE_ROOM_VALUES):
        new_id = ROOM_METATILE_BASE + i
        cells.append((base & ~0x03FF) | new_id)
    BRENDAN_ROOM_MAP.write_bytes(struct.pack("<72H", *cells))


def render_preview(room_image):
    preview = room_image.convert("RGB")
    PREVIEW_PNG.parent.mkdir(parents=True, exist_ok=True)
    preview.save(PREVIEW_PNG)


def main():
    room_quantized = make_room_image()
    room = remap_room_to_palette(room_quantized)
    palette = palette_from_image(room_quantized)
    write_jasc_palette(PALETTE_15, palette)

    base_metatiles = load_words(METATILES_BIN)[: metatile_index(ROOM_METATILE_BASE) * 8]
    tile_to_abs = write_room_tiles(room, base_metatiles)
    make_room_metatiles(room, tile_to_abs)
    patch_room_map()
    render_preview(room)


if __name__ == "__main__":
    main()
