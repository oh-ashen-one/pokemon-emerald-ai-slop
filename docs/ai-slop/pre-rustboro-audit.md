# Pre-Rustboro Demo Audit

Scope: from a fresh save through the moment the player reaches Rustboro City. Rustboro City itself is not included.

This audit is for casting/customization planning. Counts are based on the current map event data under `data/maps/` and land encounters in `src/data/wild_encounters.json`.

## People

Recommended personalization target: **80 unique person/persona slots** before Rustboro.

This merges obvious repeat appearances into one person, such as Mom, Birch, Rival, Wally, Wally's dad, Wally's mom, Norman, and Mr. Briney. If we count every repeated map object appearance separately, the number is higher, but for real-life-person casting this 80-person list is the useful one.

| Segment | Count | People / roles |
| --- | ---: | --- |
| Littleroot start, rival house, lab, Route 101 | 11 | Mom, Rival's mom, Rival's sibling, Rival, Littleroot twin, Littleroot fat man, Littleroot boy, Birch, lab aide, Route 101 youngster, Route 101 boy |
| Oldale Town and optional Oldale interiors | 13 | Oldale girl, outside mart employee, footprints man, Pokemon Center nurse, Pokemon Center gentleman, Pokemon Center boy, Pokemon Center girl, mart clerk, mart woman, mart boy, House 1 woman, House 2 woman, House 2 man |
| Route 103 / Route 102 | 7 | Route 103 boy, Route 102 little boy, Youngster Calvin, Bug Catcher Rick, Lass Tiana, Route 102 boy, Youngster Allen |
| Petalburg City, gym intro, and optional Petalburg interiors | 22 | Wally's mom, Wally, Petalburg boy, Petalburg gentleman, Wally's dad, gym boy, Scott, Norman, gym guide, Profile Man, Petalburg Pokemon Center nurse, Petalburg Pokemon Center fat man, Petalburg Pokemon Center youngster, Petalburg Pokemon Center woman, Petalburg mart clerk, Petalburg mart man, Petalburg mart boy, Petalburg mart woman, House 1 woman, House 1 man, House 2 woman, House 2 school kid |
| Route 104, Briney's house, and Pretty Petal Flower Shop | 20 | Route 104 bug catcher NPC, Route 104 girl 1, Lass Haley, Route 104 boy 1, Route 104 woman, Route 104 girl 2, Mr. Briney, Fisherman Ivan, north-route expert woman, White Herb florist, Twin Gina, Twin Mia, Rich Boy Winston, Lady Cindy, Youngster Billy, Route 104 boy 2, Fisherman Darian, flower shop owner, Wailmer Pail girl, random berry girl |
| Petalburg Woods | 7 | Aqua grunt, Devon employee, woods boy 1, Bug Catcher Lyle, Bug Catcher James, woods boy 2, woods girl |

Critical-path-only note: a straight video walkthrough that does not enter optional houses/shops will see fewer than 80 people. The 80 count is the useful upper bound if the goal is "every talkable person available before Rustboro can be personalized."

## Pokemon

Catchable/scripted pre-Rustboro species count: **15 unique species**.

Battle-visible pre-Rustboro species count: **17 unique species** if trainer-only Pokemon are included.

No fishing, surfing, Rock Smash, or post-Rustboro areas are included because those are outside the first-slice route.

### Catchable / scripted species

| Species slot | Current AI Slop identity | Where it appears |
| --- | --- | --- |
| `SPECIES_ZIGZAGOON` | Badvid | Birch rescue, Route 101, Route 102, Route 103, Wally tutorial |
| `SPECIES_POOCHYENA` | Bootdog | Route 101, Route 102, Route 103, Route 104, Petalburg Woods |
| `SPECIES_WURMPLE` | Bugfixme | Route 101, Route 102, Route 104, Petalburg Woods |
| `SPECIES_SHROOMISH` | Promptrot | Starter option, Route 101, Route 102, Petalburg Woods |
| `SPECIES_NUMEL` | Tokenburn | Starter option, Route 101 |
| `SPECIES_CORPHISH` | Slopjet | Starter option, Route 102 |
| `SPECIES_LOTAD` | Dataduck | Route 102 |
| `SPECIES_RALTS` | Chatbot | Route 102, Wally tutorial |
| `SPECIES_SEEDOT` | Seedbug | Route 102 |
| `SPECIES_TAILLOW` | Jpegull | Route 103, Route 104, Petalburg Woods |
| `SPECIES_MARILL` | Stock gap | Route 104 |
| `SPECIES_WINGULL` | Stock gap | Route 104 |
| `SPECIES_SILCOON` | Stock gap | Petalburg Woods |
| `SPECIES_CASCOON` | Stock gap | Petalburg Woods |
| `SPECIES_SLAKOTH` | Stock gap | Petalburg Woods |

Current custom coverage: **10 / 15 catchable/scripted species**.

Remaining catchable/scripted stock gaps: **5**.

- `SPECIES_MARILL`
- `SPECIES_WINGULL`
- `SPECIES_SILCOON`
- `SPECIES_CASCOON`
- `SPECIES_SLAKOTH`

### Trainer-only battle-visible additions

These can appear in trainer battles before Rustboro even though they are not normally catchable on the no-rod/no-surf path.

| Species slot | Current AI Slop identity | Where it appears |
| --- | --- | --- |
| `SPECIES_MAGIKARP` | Stock gap | Route 104 fishermen / early trainers |
| `SPECIES_NINCADA` | Stock gap | Bug Catcher James in Petalburg Woods |

Current custom coverage if trainer-only battle species are included: **10 / 17 battle-visible species**.

Remaining battle-visible stock gaps: **7**.

- `SPECIES_MARILL`
- `SPECIES_WINGULL`
- `SPECIES_SILCOON`
- `SPECIES_CASCOON`
- `SPECIES_SLAKOTH`
- `SPECIES_MAGIKARP`
- `SPECIES_NINCADA`

