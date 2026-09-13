# Using video instead of a photo

Any photo slot will take a video, and the home page hero will take one too.
Drop the file in, push, done — no code changes.

## The two places

**Home page hero.** Name the file `hero-bg.mp4` and put it in
`public/assets/img/` beside `hero-bg.jpg`. The still stays as the poster: it
shows instantly, then the clip fades in over it once it has loaded.

**Any photo slot.** Use the slot's filename from the photo sheet, with `.mp4`
instead of `.jpg` — e.g. `projects-ermington-duplex-landscaping-retaining-wall-2.mp4`.
Add a still with the same name (`...-2.jpg`) and it becomes the poster.

## What the file should be

| | |
|---|---|
| Format | MP4, H.264 video, **no audio track** |
| Length | 6–12 seconds, looping cleanly |
| Size | **Under 3 MB.** Hard ceiling 25 MB (Cloudflare rejects the deploy above that; the build will skip anything over 20 MB) |
| Width | 1600px is plenty; 1920px maximum |
| Frame rate | 24–30fps |
| Poster still | Always include one — it is what most visitors see first, and what some see only |

Silent is not a preference, it is a requirement: browsers only allow autoplay
when a video is muted, and an audio track just adds weight.

## What happens automatically

- Plays muted, looping, inline — never fullscreen-hijacks a phone.
- Loads **only when it scrolls into view**, and pauses when it leaves.
- Skipped entirely for visitors who ask for reduced motion, are on a metered or
  slow connection, or have data-saver on. They see the poster still. Nothing
  downloads.
- The poster is what search engines and social previews use.

## Making the file

Easiest: send me the raw clip and I will cut, mute, resize and compress it.

To do it yourself — **HandBrake** (free, Windows): Preset *Web → Vimeo YouTube
720p30*, Audio tab → remove the track, Video tab → Constant Quality around RF 26,
Dimensions → width 1600. That usually lands a 10-second clip near 2 MB.

## Where video earns its place

Drone flyover of a finished yard, a wall going up, an excavator working, turf
being rolled. Movement should show something a still cannot. A static scene with
a slightly wobbling camera is worse than the photo — it costs load time and
attention for nothing.
