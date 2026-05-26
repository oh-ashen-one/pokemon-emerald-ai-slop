# Pokemon Emerald: AI Slop

`Pokemon Emerald: AI Slop` is a public ROM hack project built on top of
[`pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion).
The goal is a shippable, funny Emerald rebalance with visible AI-era nonsense:
rewritten early-game dialogue, altered starter choices, tuned early trainers,
light encounter changes, and a few custom-flavored moves.

This repository contains source code only. It does not include any commercial
ROMs, generated `.gba` files, save files, or copyrighted game dumps.

## Current v0.1 Direction

- Existing-sprite starter trio: Shroomish, Numel, and Corphish.
- Early route identity pass for Route 101 and Route 102.
- Rival and early trainer tuning around the new starter trio.
- Dialogue rewrite pass for the opening bedroom/rival sequence.
- No custom sprites, new music, or major map work for v0.1.

## Building

Follow the upstream macOS setup in [`INSTALL.md`](INSTALL.md). The short version
is that the build expects Xcode Command Line Tools, `libpng`, `pkg-config`, and
devkitARM from devkitPro.

Once the toolchain is installed:

```sh
make
```

The generated ROM, when the build succeeds, is `pokeemerald.gba`. That file is
intentionally ignored by Git.

## Upstream

This hack tracks Rom Hacking Hideout's expansion base as the `RHH` remote:

```sh
git remote add RHH https://github.com/rh-hideout/pokeemerald-expansion.git
git fetch RHH
```

Periodic upstream updates should be merged deliberately after a clean local
build.

## Credits

Based on RHH's `pokeemerald-expansion`:
<https://github.com/rh-hideout/pokeemerald-expansion/>

`pokeemerald-expansion` is built on pret's `pokeemerald` decompilation:
<https://github.com/pret/pokeemerald/>

Please keep upstream credits intact when distributing builds, patches, or
videos derived from this project.
