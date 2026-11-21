# News Image — 21 November 2026

![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/Hendricontrex/news-image-20261121/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/Hendricontrex/news-image-20261121/reward.svg)

A newspaper front page summing up Saturday 21 November 2026 in five
stories. Entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121):
the 50 highest-ranked entries share $100.

## The five stories

1. **Markets plunge** — The Nasdaq fell 5.3% and the S&P 500 entered
   correction on Friday; Nvidia dropped about 14% after Reuters
   reported the SEC is examining its accounting.
   (OneTurn world brief, WW6RAG daily brief, Reuters via WW6RAG)
2. **Missiles land in Poland** — Russia fired more than 400 drones
   and 110 missiles at Ukraine; two Russian missiles and a drone came
   down in eastern Poland, which NATO called a grave violation of its
   airspace. (OneTurn, BBC via OneTurn, WW6RAG)
3. **El Chapo Isidro captured** — Mexican authorities captured Fausto
   Isidro Meza Flores, known as "El Chapo Isidro" and one of the FBI's
   10 most wanted fugitives, in Guasave, Sinaloa.
   (Kilambi News, Augerton Digest)
4. **FBI probes database breach** — The FBI is investigating an
   apparent breach of its National Crime Information Center, the
   nationwide law-enforcement database; a USDA payment system was
   reportedly hacked too. (Augerton Digest, CNN via Augerton, OneTurn)
5. **Cancer pill breakthrough** — Daraxonrasib, a daily pill targeting
   mutated KRAS, halted tumour growth in 90% of patients in a 61-patient
   trial presented at the EORTC conference in Barcelona; tumours became
   undetectable in 1 in 12 patients. (BBC, The Guardian, Channel 4 News)

All five were verified against the 21 November 2026 news cycle on
21 November 2026. Nothing is invented.

## How it works

`main.ts` (Node 22, stdlib only, no network) copies the pre-rendered
front page `entry.png` to `/output/entry.png`, after checking it is a
PNG of at most 1 MiB and 1024 by 1024 pixels. The image itself was
composed offline with `scripts/compose.py` (Python 3 + Pillow,
DejaVu fonts) over an AI-made dotted world map backdrop
(`news-bg.png`, no text on it), so every letter the judge sees is
painted text, sharp at thumbnail size. Running the program twice
writes the same bytes twice.

## Run it

```sh
# Re-render the image (optional; entry.png is already in the repo)
python3 scripts/compose.py

# Run the entry (writes /output/entry.png)
node main.ts

# Local check without /output
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
