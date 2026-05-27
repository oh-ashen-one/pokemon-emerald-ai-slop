# AI Slop — Testing Handout

Quick reference for picking this back up in a fresh session: how to build/run, and
exactly what to verify in-game. Scope of the whole project is **start of game →
arriving at Rustboro City** (Rustboro itself and beyond are out of scope).

---

## Build & run (this machine)

Use the cached toolchain (NOT Homebrew's `arm-none-eabi-gcc` 16 — it's missing
newlib and will fail with "stdint.h: No such file or directory"):

```sh
cd ~/pokemon-emerald-ai-slop
make TOOLCHAIN="/Users/darkeatermidir/.cache/pokemon-rom-hack-toolchains/arm-gnu-toolchain-14.3.rel1-darwin-arm64-arm-none-eabi" -j$(sysctl -n hw.ncpu)

# run it
/opt/homebrew/bin/mgba ~/pokemon-emerald-ai-slop/pokeemerald.gba
```

- Output ROM: `pokeemerald.gba` (~32 MB). First build ~10–15 min; incremental builds are quick.
- Saves: mGBA writes `pokeemerald.sav` next to the ROM, so an existing save reloads after a rebuild.
- Repo: `oh-ashen-one/pokemon-emerald-ai-slop` (public). Build artifacts are git-ignored.

---

## PRIORITY — verify the two sprite bug fixes

These were just fixed; confirm them first.

- [ ] **Player facing.** Walk left, right, and up. The character faces the way it's
      moving with no random left/right flicker. (Fix: player walking/running sheets +
      palettes reverted to stock.)
- [ ] **Rival's-house glitch.** Enter the friend/rival's house. The garbled
      "placeholder"-looking sprite that was in the top-left should be gone.
      **This fix is a best-guess** (reverted the rival's sibling `ninja_boy` to the
      stock sprite). If the glitch is STILL there: screenshot it standing right next
      to it and note which character it's near, so the exact object can be pinned down.

---

## Content QA checklist (start → Rustboro)

Everything below should read as "AI Slop," not stock Hoenn.

**Dialogue** (every talkable NPC, sign, and trainer)
- [ ] Littleroot, Route 101, Oldale, Route 103 (already done earlier)
- [ ] Route 102, Petalburg City + interiors, Petalburg Gym first visit (Wally tutorial + Norman intro)
- [ ] Route 104 + Mr. Briney + flower shop, Petalburg Woods (Team Aqua run-in)

**Trainer class names** (shown in battle banner)
- [ ] Youngster→Script Kid · Bug Catcher→Bug Reporter · Lass→Intern · Twins→Pair Coders
- [ ] Fisherman→Log Fisher · Rich Boy→VC Kid · Lady→Investor · PokéFan→Fanboy · Aroma Lady→DevRel
- [ ] Rival battle shows "Balance QA" (Route 103 rival fight)

**Items** (bag + marts + pickups)
- [ ] Potion→Hotfix · Super Potion→Patch · Antidote→Linter · Paralyze Heal→Unblocker
- [ ] Burn Heal→Cooldown · Ice Heal→Defroster · Awakening→Wake Lock · Full Heal→Full Restart
- [ ] Repel→Rate Limiter · Escape Rope→Git Revert · Oran Berry→Cache Berry · Fresh Water→Cold Brew
- [ ] Themed descriptions read correctly (Poké/Great Ball reflavored too)

**Abilities** (summary screen / switch-in) — 24 renamed, e.g.
- [ ] Run Away→Rage Quit · Pickup→Web Scrape · Quick Feet→Hot Path · Synchronize→State Sync
- [ ] Effect Spore→Side Effects · Hyper Cutter→Hard Fork · Guts→Crunch Mode

**Moves** (battle + move menu)
- [ ] Renamed early moves: Ember→Flame War · Leech Seed→Tech Debt · Stun Spore→Deadlock · Mega Drain→Bulk Scrape (+ more)
- [ ] Starters know their signature move at Lv1: Promptrot→Prompt Rot · Tokenburn→Token Burn · Slopjet→Slop Jet

**Heal/shop text**
- [ ] Pokémon Center nurse talks about "known-good build / redeploy"
- [ ] Mart clerk talks about "the funnel / provisioning"

**Music swaps** (existing tracks reused)
- [ ] Petalburg Woods = eerie Abandoned Ship theme
- [ ] Oldale Town = Fallarbor theme
- [ ] Route 102 = a distinct route remix

**Starters / custom species**
- [ ] Promptrot / Tokenburn / Slopjet selectable; custom dex names + entries
- [ ] Wild + trainer Pokémon show custom names (Badvid, Bootdog, Bugfixme, Chatbot, Dataduck, Seedbug, Jpegull)

---

## Known caveats / watch-list

- The rival-house fix (A2) is unconfirmed — see PRIORITY above.
- Trainer classes, items, abilities, moves, and nurse/mart text are **global** (game-wide),
  but only the start→Rustboro path is in scope, so only judge them there.
- The "cameo" NPC sprites (friends added in an earlier commit) may have the same kind of
  bad side-facing frames as the player did. We deliberately only fixed the two flagged
  sprites — others were left as-is.
- The Route 103 sign and README were updated from "demo ends at Route 103" to the new
  start→Rustboro scope.

---

## Next up (not started)

- **Playable-in-browser website** (legal-safe): EmulatorJS + a `.bps` patch the visitor
  applies to their **own** Emerald ROM client-side (do NOT host the ROM). Needs patch
  tooling added + a vanilla Emerald ROM available locally to generate the patch. Keep
  pret/`pokeemerald` + RH-Hideout credits visible. Full plan was approved previously.

## Reminders

- **Scope:** start → Rustboro City only. Don't build content past Rustboro.
- **Legal:** never distribute the built `.gba` (it's a Nintendo-copyrighted derivative).
  Distribute a patch + have users bring their own ROM.
