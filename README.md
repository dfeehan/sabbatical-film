# sabbatical-film

A self-directed film curriculum for the 2026–27 sabbatical year: 42 weeks, 85 core
films, organized into 13 thematic units.

## The idea

Rather than alternating "important" films with "enjoyable" ones, the plan runs
**short units of 3–4 weeks** built around a single director, movement, or genre
problem. Films inside a unit talk to each other — an influence, a rebuttal, a
second attempt at the same problem — so each one makes the next more legible and
more fun. Most canonical films are difficult only because they're watched cold.

Two core films per week, plus one optional extension. Four weeks carry an extra
short film (14–32 min) to cover avant-garde and documentary work.

## Files

| File | What it is |
|---|---|
| [`sabbatical-film-syllabus.md`](sabbatical-film-syllabus.md) | The schedule. 42 dated weeks, 24 Aug 2026 – 4 Jul 2027, with a note on why each pairing works and one reading per unit. |
| [`where-to-watch.md`](where-to-watch.md) | US streaming availability for all 85 films — what's on the Criterion Channel, what's free via Kanopy/Tubi, what needs renting, and the year's total cost. |
| [`syllabus-comparison.md`](syllabus-comparison.md) | How this plan compares to eleven real university film syllabi (194 screenings, 147 distinct films), with the overlap analysis that produced the final round of additions. |
| `notes/` | Viewing notes go here. |

### Generated formats

| File | What it is |
|---|---|
| [`index.html`](index.html) | **Browsable version.** All three documents in one self-contained page with a sidebar for jumping between units. Open it in any browser — no server needed. Works offline, respects dark mode, prints cleanly. |
| `sabbatical-film-syllabus.pdf` | The syllabus, typeset (14 pp., letter). |
| `where-to-watch.pdf` | Availability guide, typeset (8 pp.). |
| `syllabus-comparison.pdf` | Comparison, typeset (5 pp.). |
| `build/` | Scripts that regenerate the HTML and PDFs from the Markdown. |

The Markdown files are the source of truth. After editing any of them, run:

```bash
./build/build.sh
```

which rebuilds all four generated files. Requires `pandoc`, `xelatex`
(`brew install pandoc` and MacTeX or `brew install --cask basictex`), and `python3`.

## The units

| # | Unit | Weeks | Dates |
|---|---|---|---|
| 1 | The Grammar | 1–3 | 24 Aug – 13 Sep 2026 |
| 2 | The Studio System | 4–7 | 14 Sep – 11 Oct 2026 |
| 3 | Silents & the Avant-Garde | 8–10 | 12 Oct – 1 Nov 2026 |
| 4 | Italy: Rubble to Ennui | 11–13 | 2 – 22 Nov 2026 |
| 5 | The French New Wave | 14–16 | 23 Nov – 13 Dec 2026 |
| — | *holiday break* | — | 14 Dec – 3 Jan 2027 |
| 6 | Japan | 17–20 | 4 – 31 Jan 2027 |
| 7 | The Northern Interior | 21–23 | 1 – 21 Feb 2027 |
| 8 | New Hollywood | 24–27 | 22 Feb – 21 Mar 2027 |
| 9 | Hong Kong & Taiwan | 28–30 | 22 Mar – 11 Apr 2027 |
| 10 | Off the Usual Axis | 31–33 | 12 Apr – 2 May 2027 |
| 11 | Germany & the Political Film | 34–36 | 3 – 23 May 2027 |
| 12 | Cinema Now | 37–39 | 24 May – 13 Jun 2027 |
| 13 | Capstone: Cinema as Pure Form | 40–42 | 14 Jun – 4 Jul 2027 |

## How to use it

1. **One film per sitting, no phone.** These were built for uninterrupted
   attention and collapse without it.
2. **Write 3–4 sentences after each one**, before reading anything about it.
   Put them in `notes/`.
3. **Read the criticism after, never before.** One piece, ten minutes.

Optional scaffolding: Bordwell & Thompson, *Film Art: An Introduction*,
chapters 4–6, read during Unit 1.

## Costs

Criterion Channel carries 50 of the 85. A library card for Kanopy covers 20 more
for free. Budget roughly **$130 for the year** all in. See
[`where-to-watch.md`](where-to-watch.md) for the breakdown.

Streaming rights rotate constantly — re-check each unit about a month before
starting it.
