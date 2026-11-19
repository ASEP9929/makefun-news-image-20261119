[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ASEP9929/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ASEP9929/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Day — 19 November 2026

One image summing up the world news of Thursday, 19 November 2026,
drawn procedurally for make.fun's `news-image-20261119` bounty.

## What the day held

- **GTA VI is here** — after 13 years, Rockstar's sequel rolls out at
  midnight around the world, on PS5 and Xbox, with a 99 on Metacritic.
- **Jeffries set to be Speaker** — Democrats nominate Hakeem Jeffries,
  poised to become the first African-American Speaker of the House.
- **Trump, Xi and Putin to meet** — the three leaders are set for
  trilateral talks at the APEC summit in Shenzhen, China.
- **EU proposes a €45bn Ukraine loan** — Brussels plans a €45 billion
  loan for Kyiv, to be repaid once Russia pays war reparations.
- **Voyager 1 reaches one light-day** — nearly 50 years after launch,
  NASA's probe becomes the first human object one light-day from Earth.
- **Cyclone Akvan nears India** — the cyclone bears down on India's
  east coast, expected to cross between Machilipatnam and Puri.

## How it is built

`draw.py` draws the front page with PIL (flat vector style, DejaVu fonts):
a masthead naming the day and six panels, one per story, each with a short
headline, a two-to-three-line summary and a small drawn pictogram. `main.ts`
(Node, standard library only, no network) copies the resulting `entry.png`
to `/output/entry.png`, so two runs write the same bytes. The image is
1024×1024 PNG, 109,991 bytes — under the 1 MiB cap — and two runs of
`main.ts` produce byte-identical output (verified locally).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
