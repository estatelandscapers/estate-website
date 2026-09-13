# Photo processing — notes

Estate Landscapers website photo set · 13 September 2026

**Result:** 52 files, 19.08 MB, 72 of 163 slots filled. Started from 79 files / 131 MB.

---

## Calls I made that you should check

Five project heroes were assigned on inference rather than on something in the filename or
visibly in the shot. If any is the wrong job, rename the file (the `<key>--` part before the
two hyphens is all that matters) or move the key into `photo-map.json`.

| Slot | File I used | Why I chose it — and the doubt |
|---|---|---|
| `project-dural-acreage-landscaping-native-planting-hero` | acreage home, established buffalo lawn, sandstone edging | Only acreage-scale shot in the folder. Your own caption called it "an Estate-built yard being maintained a season after handover" — it may belong on the care pages instead, or be a different job entirely. |
| `project-north-kellyville-boutique-home-landscaping-hero` | grand home, cobblestone driveway, Zoysia Sir Grange | "Boutique home" + Sir Grange + rendered planter matched the North Kellyville brief line. Could equally be the Kellyville or Castle Hill job. |
| `project-north-ryde-duplex-landscaping-hero` | duplex, steppers in white pebble, coloured driveway | It is a duplex front yard. Nothing in the file says North Ryde — it could just as easily be the Caringbah South duplex. |
| `project-caringbah-south-duplex-landscaping-hero` | duplex, sandstone steppers in turf, mulched beds | Same reasoning, same doubt. **If these two are swapped, swap the two `project-…-hero--` prefixes.** |
| `project-rydalmere-new-home-landscaping-hero` | modern new home, lit entry steps | "New home landscaping" matched a new-build frontage. Not confirmed as Rydalmere. |

Two more worth a glance:

- `project-parramatta-museum-turfing-works-hero` is a **during-works** shot (sand pad, turf going down), not a completed one. It is the only Parramatta photo you have, so it is doing hero duty. A finished shot would be the single biggest improvement to that page.
- `project-greater-sydney-public-school-turfing-works-hero` came in at **478 × 354 px** — far below the 1200 px minimum. It will look soft on a project page. Worth re-shooting or finding the original.
- `home-hero` (supervisor and crew checking set-out) was a 1024 × 768 PNG, so it is 1024 px wide rather than 1600. Not upscaled, per the brief.

---

## Photos I could not place

| File | Why |
|---|---|
| `areas-1.jpg` | The "Sydney service area" map graphic. It is a designed asset, not a photograph of a project, so it does not belong in a photo slot. It was filling `areas-hero` through the legacy `areas-1` alias — `areas-hero` now points at a real completed project instead. Keep the map with your design assets if the site uses it elsewhere. |

Everything else in the folder found a slot or was removed for the reason below.

---

## Photos I removed, and why

| File | Why |
|---|---|
| `projects-enfield-park-amenities-landscape-works-4.jpg` | Watermarked "AI-generated content" — not a usable record of the works |
| `projects-enfield-park-amenities-landscape-works-5.jpg` | Watermarked "AI-generated content" — not a usable record of the works |
| `residential-landscape-design-1.jpg` | 3D CGI render, not a photograph of an Estate project (put it back if it is your own design visual) |
| `areas-1.jpg` | "Sydney service area" map graphic, not a project photo — belongs with the site's design assets, not the photo slots |
| `hero-home.jpg` | Portrait crop of the same Moorebank frontage shot kept as project-moorebank-industrial-landscape-works-g1 |
| `home-4--commercial-landscape-construction-nsw.jpg` | Near-duplicate crop of the same Moorebank frontage shot |
| `home-5--Floating Deco batten Front fence with driveway, council crossover, vehicular crossing, kerb, planting, pavers and letterbox at Rouse Hill NSW.jpg` | Letterbox crop of the Rouse Hill hero — the full frame is kept |

Plus 20 exact byte-for-byte duplicates: the same fourteen photographs had been saved under
two or three names each (for example the Museum streetscape shot existed as `commercial-2--…`,
`commercial-commercial-property-1--…` and `project-10--… - Copy`). One copy of each is kept, and
`photo-map.json` points the extra slots at it — no file is duplicated on disk.

---

## Empty slots

90 of the 162 listed keys have no photo. The site shows its placeholder for these. By page:

**Project: Caringbah South Duplex Landscaping** — 7 empty

- `project-caringbah-south-duplex-landscaping-progress`
- `project-caringbah-south-duplex-landscaping-g1`
- `project-caringbah-south-duplex-landscaping-g2`
- `project-caringbah-south-duplex-landscaping-g3`
- `project-caringbah-south-duplex-landscaping-g4`
- `project-caringbah-south-duplex-landscaping-g5`
- `project-caringbah-south-duplex-landscaping-g6`

**Project: Darlinghurst Museum Landscape & Public Domain Works** — 4 empty

- `project-darlinghurst-museum-landscape-public-domain-works-progress`
- `project-darlinghurst-museum-landscape-public-domain-works-g1`
- `project-darlinghurst-museum-landscape-public-domain-works-g2`
- `project-darlinghurst-museum-landscape-public-domain-works-g3`

**Project: Dural Acreage Landscaping & Native Planting** — 7 empty

- `project-dural-acreage-landscaping-native-planting-progress`
- `project-dural-acreage-landscaping-native-planting-g1`
- `project-dural-acreage-landscaping-native-planting-g2`
- `project-dural-acreage-landscaping-native-planting-g3`
- `project-dural-acreage-landscaping-native-planting-g4`
- `project-dural-acreage-landscaping-native-planting-g5`
- `project-dural-acreage-landscaping-native-planting-g6`

**Project: Enfield Park Amenities Landscape Works** — 2 empty

- `project-enfield-park-amenities-landscape-works-progress`
- `project-enfield-park-amenities-landscape-works-g3`

**Project: Ermington Duplex Landscaping & Retaining Wall** — 4 empty

- `project-ermington-duplex-landscaping-retaining-wall-progress`
- `project-ermington-duplex-landscaping-retaining-wall-g1`
- `project-ermington-duplex-landscaping-retaining-wall-g4`
- `project-ermington-duplex-landscaping-retaining-wall-g5`

**Project: Greater Sydney Public School Turfing Works** — 4 empty

- `project-greater-sydney-public-school-turfing-works-progress`
- `project-greater-sydney-public-school-turfing-works-g1`
- `project-greater-sydney-public-school-turfing-works-g2`
- `project-greater-sydney-public-school-turfing-works-g3`

**Project: Kemps Creek Industrial Vertical Green Walls** — 4 empty

- `project-kemps-creek-industrial-vertical-green-walls-progress`
- `project-kemps-creek-industrial-vertical-green-walls-g1`
- `project-kemps-creek-industrial-vertical-green-walls-g2`
- `project-kemps-creek-industrial-vertical-green-walls-g3`

**Project: Moorebank Industrial Landscape Works** — 2 empty

- `project-moorebank-industrial-landscape-works-progress`
- `project-moorebank-industrial-landscape-works-g3`

**Project: Newtown Duplex Raised Planter Landscaping** — 2 empty

- `project-newtown-duplex-raised-planter-landscaping-progress`
- `project-newtown-duplex-raised-planter-landscaping-g5`

**Project: North Kellyville Boutique Home Landscaping** — 7 empty

- `project-north-kellyville-boutique-home-landscaping-progress`
- `project-north-kellyville-boutique-home-landscaping-g1`
- `project-north-kellyville-boutique-home-landscaping-g2`
- `project-north-kellyville-boutique-home-landscaping-g3`
- `project-north-kellyville-boutique-home-landscaping-g4`
- `project-north-kellyville-boutique-home-landscaping-g5`
- `project-north-kellyville-boutique-home-landscaping-g6`

**Project: North Ryde Duplex Landscaping** — 6 empty

- `project-north-ryde-duplex-landscaping-progress`
- `project-north-ryde-duplex-landscaping-g1`
- `project-north-ryde-duplex-landscaping-g2`
- `project-north-ryde-duplex-landscaping-g3`
- `project-north-ryde-duplex-landscaping-g4`
- `project-north-ryde-duplex-landscaping-g5`

**Project: Parramatta Museum Turfing Works** — 4 empty

- `project-parramatta-museum-turfing-works-progress`
- `project-parramatta-museum-turfing-works-g1`
- `project-parramatta-museum-turfing-works-g2`
- `project-parramatta-museum-turfing-works-g3`

**Project: Ropes Crossing Subdivision Landscape & Civil Works** — 4 empty

- `project-ropes-crossing-subdivision-landscape-civil-works-progress`
- `project-ropes-crossing-subdivision-landscape-civil-works-g1`
- `project-ropes-crossing-subdivision-landscape-civil-works-g2`
- `project-ropes-crossing-subdivision-landscape-civil-works-g3`

**Project: Rouse Hill Boutique Home Landscaping** — 7 empty

- `project-rouse-hill-boutique-home-landscaping-progress`
- `project-rouse-hill-boutique-home-landscaping-g1`
- `project-rouse-hill-boutique-home-landscaping-g2`
- `project-rouse-hill-boutique-home-landscaping-g3`
- `project-rouse-hill-boutique-home-landscaping-g4`
- `project-rouse-hill-boutique-home-landscaping-g5`
- `project-rouse-hill-boutique-home-landscaping-g6`

**Project: Rydalmere New Home Landscaping** — 7 empty

- `project-rydalmere-new-home-landscaping-progress`
- `project-rydalmere-new-home-landscaping-g1`
- `project-rydalmere-new-home-landscaping-g2`
- `project-rydalmere-new-home-landscaping-g3`
- `project-rydalmere-new-home-landscaping-g4`
- `project-rydalmere-new-home-landscaping-g5`
- `project-rydalmere-new-home-landscaping-g6`

**Residential landing** — 4 empty

- `residential-5`
- `residential-6`
- `residential-7`
- `residential-8`

**Service area page** — 8 empty

- `areas-eastern-suburbs-hero`
- `areas-hills-district-hero`
- `areas-inner-west-and-city-hero`
- `areas-lower-north-shore-hero`
- `areas-northern-beaches-hero`
- `areas-ryde-and-parramatta-hero`
- `areas-st-george-and-sutherland-hero`
- `areas-upper-north-shore-hero`

**Service page** — 7 empty

- `residential-landscape-drainage-hero`
- `residential-landscaping-baulkham-hills-hero`
- `residential-landscaping-bella-vista-hero`
- `residential-landscaping-castle-hill-hero`
- `residential-landscaping-kellyville-hero`
- `residential-landscaping-north-kellyville-hero`
- `residential-landscaping-rouse-hill-hero`

The pattern worth noticing: **every project has a hero except Dural, and almost none has a
gallery or a progress shot.** Newtown and Enfield are the only projects with more than one
photo. Six good shots per residential project — wide, from the street, turf and beds, the wall,
the paving, one detail — plus one during-works shot each would close roughly 70 of the 90 empty
slots on its own.

Two service heroes are empty because nothing in the folder honestly shows them:
`residential-landscape-drainage-hero` (ag pipe and gravel in an open trench) and the six suburb
pages (Baulkham Hills, Bella Vista, Castle Hill, Kellyville, North Kellyville, Rouse Hill).

The eight `areas-…-hero` region slots are deliberately left empty: rule 4 already puts each
project's hero on its region page, so filling the region hero with the same photo would show it
twice on one page. They want a *different* completed project from that region.

---

## Processing applied to every file

Rotation baked into the pixels first (`ImageOps.exif_transpose`), then a fresh canvas so no EXIF,
GPS or IPTC survives — verified: zero files carry any metadata. Long edge to 1600 px for heroes
and banners, 1200 px for gallery and detail, never upscaled. Saturation ×1.12, contrast ×1.06,
unsharp mask 1.2 / 50% / 2. Progressive JPEG at quality 80 stepping down to 76.

Seventeen files land between 400 and 660 KB rather than under the 400 KB target. Pushing them
under would have meant dropping below quality 76, outside the band the brief specifies, so I held
the quality and let the size run — the largest file is 660 KB, well inside the 1 MB hard limit.
Average across the set is 375 KB. Say the word if you would rather have the smaller files.

`hero-bg.jpg` is byte-for-byte unchanged, as instructed. The `councils/` and `instagram/`
sub-folders were not in the folder you connected — they are untouched wherever they live.
