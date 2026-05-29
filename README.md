# Pokemon Emerald: AI Slop

`Pokemon Emerald: AI Slop` is a public ROM hack project built on top of
[`pokeemerald-expansion`](https://github.com/rh-hideout/pokeemerald-expansion).
The goal is a shippable 10-15 minute YouTube demo slice with visible AI-era
nonsense: rewritten early-game dialogue, altered starter choices, tuned early
trainers, light encounter changes, and a few custom-flavored moves.

This repository contains source code only. It does not include any commercial
ROMs, generated `.gba` files, save files, or copyrighted game dumps.

## Play it now

Play in your browser: <https://aislop-web-production.up.railway.app/>

## Current v0.1 Direction

- YouTube demo slice from the bedroom all the way to RUSTBORO CITY. The player
  arrives at Rustboro; Rustboro itself and anything past it are out of scope.
- Starter trio replaces Shroomish, Numel, and Corphish with Promptrot,
  Tokenburn, and Slopjet, each with an AI-themed signature move (Prompt Rot,
  Token Burn, Slop Jet) learned at level 1.
- Ten early species replacements cover Promptrot, Tokenburn, Slopjet, Badvid,
  Bootdog, Bugfixme, Chatbot, Dataduck, Seedbug, and Jpegull.
- Every talkable NPC, sign, and trainer from the start through Petalburg Woods
  has custom AI Slop dialogue (Birch's unsafe prototype lab, vibe coders,
  growth-hacker onboarding, rival balance tests, Team Aqua "blocking the
  deploy", and so on).
- Trainer classes, items, abilities, and common early moves are reskinned in the
  AI Slop voice (e.g. Bug Catcher -> Bug Reporter, Potion -> Hotfix, Run Away ->
  Rage Quit, Tackle -> Vibe Check). Nurse and Mart text reskinned too.
- A few existing music tracks are reused for vibe (Petalburg Woods, Oldale,
  Route 102). No new audio is added.
- GPT-generated source art and converted custom pixel sprites cover the
  first-slice Pokemon and visible overworld people. Source assets live under
  [`docs/ai-slop/gpt-generated`](docs/ai-slop/gpt-generated).
- No full dex or full-map rebuild for v0.1.

## Demo Boundary

This project is intentionally not trying to replace all of Hoenn right now. The
recordable path is:

1. Bedroom and Mom intro.
2. Player/rival setup in Littleroot.
3. Birch rescue and starter choice.
4. First battle with Badvid.
5. Oldale onboarding and early NPC jokes.
6. Route 103 rival balance-test battle.
7. Back through Route 102 to Petalburg City (gym intro + Wally tutorial).
8. Route 104, Mr. Briney, and the flower shop.
9. Petalburg Woods and the Team Aqua run-in.
10. Arrival at RUSTBORO CITY.

Rustboro City interiors/gym and anything past Rustboro should be treated as out
of scope unless it directly improves footage for the demo path above.

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
