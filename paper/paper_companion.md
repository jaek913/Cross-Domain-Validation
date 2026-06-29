# Cross-Domain Validation — Plain-English Companion

*A plain-language walkthrough of the paper "Cross-Domain Validation of a Moving-Average Divergence Framework in Atmospheric Science, Hydrology, Solar Physics, and Epidemiology." This companion is for understanding, not advice: nothing here is a recommendation to trade, invest, or make health decisions. It explains what the paper does and what it found, in everyday terms.*

## The one-sentence version

A set of moving-average tools that had only ever been tested on financial markets turns out to correctly describe the known physical behavior of weather, rivers, sunspots, and flu — and the same single measurement (how a series correlates with its own past) explains how the tools behave in every one of those domains.

## Why bother testing market tools on rivers and flu?

Markets are a bad place to *prove* a method works, because nobody knows the "true" rules generating market prices. If a tool seems to work on prices, you can't check it against the real mechanism, because the real mechanism is hidden.

Nature is different. We already know — from physics — how these systems behave:

- **Weather** (daily temperature, once you remove the seasons) barely "remembers" yesterday. It snaps back to normal fast.
- **Rivers** remember much longer, because water is physically stored in snowpack, soil, and reservoirs and released slowly.
- **Sunspots** swing up and down on an ~11-year cycle — they oscillate rather than settle.
- **Flu** in an outbreak just takes off; during the climb there is no force pulling it back to a baseline.

So if a market tool, applied with no special tuning, reproduces *this* known ordering and behavior, that's strong outside evidence that the tool is measuring something real — not just curve-fitting to markets.

## The main tools, in plain terms

**1. A "who's chasing whom" meter.** A moving average is a smoothed line that trails a bumpy series. Sometimes the smoothed line chases the series (the series leads); sometimes the series snaps back to the smoothed line (the line leads). The paper measures the balance with a number called the **filter-share**. A high filter-share means "the smooth line is always chasing" — typical of something with no memory (like a coin-flip walk). A low filter-share means "the series keeps returning to the line" — typical of something that reverts.

When you line the domains up by this meter, they fall in exactly the order physics predicts: weather (chases least — snaps back) → rivers (in between) → flu (chases most — runs away). A synthetic "pure randomness" series sits right where theory says it should, as a control.

**2. A "two speeds of choppiness" signal.** Instead of asking "is this system getting jumpier?" at one timescale (the standard early-warning approach), the paper compares a *fast* measure of choppiness to a *slow* one. The difference (the "divergence") is a richer signal — and the older one-speed method is just a special case of it. In each domain the signal carries the sign the physics implies; in flu it even points the opposite way from the old one-speed indicator, exactly because a runaway outbreak isn't a "slowing down" situation.

**3. A rule that predicts the sign from memory.** There's a clean mathematical rule (borrowed, not newly invented here) that says: whether the fast-minus-slow signal predicts the future with a plus or a minus sign is decided entirely by how the series correlates with its own past at near versus far time-lags. The paper tests this rule on 25 pre-registered predictions across five systems and it holds on **every single statistically solid one** — including two cases where the sign was predicted to *flip*, and it flipped. (One subtlety the paper is careful about: one of those flips is often misdescribed as the correlation "crossing zero." It isn't — it flips because the near-lag memory dips below the far-lag memory while both stay positive. The paper states this precisely.)

## The useful payoff: spotting flu earlier

Standard flu surveillance waits for the case rate to cross a line. The divergence tool watches the *change in slope* instead, so it fires earlier — on average about eight weeks earlier than the level-based method, across nearly thirty seasons — and it does this with no disease model, no fitted parameters, and nothing but the public flu data. The same trick, applied to each flu subtype, flags which strain is taking over at the same time. This is a genuinely useful lead time for public health.

## What the paper honestly reports as *not* working

Good science reports the misses, and this paper has three worth highlighting:

- **Peaks, not onsets.** The same tool that's great at catching the *start* of a flu season is **not** good at calling the *peak*. A trailing average structurally can't lead its own turning point, and the paper says so plainly.
- **A "spread across regions" peak detector failed.** The authors guessed that watching the flu curves of the ten U.S. regions might catch the national peak early. They pre-registered the test — and it failed. What looked like an early signal turned out to be regional *noise*, not real lead; a fair national-only comparison actually lagged. They report the negative result rather than dressing it up, and they did a follow-up confirming there's no reliable "early region" to exploit.
- **A big correction to the earlier work.** In the river analysis, an earlier headline ("one river shows the signal, the other doesn't") turned out to come from accidentally computing the two rivers differently — including one setup that peeked at information it shouldn't have. Done consistently, *both* rivers show the signal, and the more seasonal river is actually the stronger one. The paper corrects this openly.

## The honesty machinery behind the numbers

Every number in the paper is produced by a committed computer script running on public data whose exact version is locked by a fingerprint, and an automatic checker re-runs everything and confirms each number matches before the paper is considered done. The one piece of mathematics the paper leans on is verified three independent ways — a written proof, a symbolic computer check, and a numerical stress test — and all three agree. Anything that didn't reproduce is flagged, not quietly fixed.

## The test that hasn't happened yet

The strongest claim is a *dated, public prediction*: for the 2026–27 flu season, the early-detection tool should fire at least six weeks before standard surveillance. Anyone can check this against public CDC data when the season arrives. If it doesn't happen, the practical claim is wrong — and the paper says so in advance. That's the difference between a story fit to old data and a real prediction.

---

*Plain-English companion. For education, not advice. All data are public (CDC FluView, NOAA GHCN-Daily, USGS NWIS, SIDC/SILSO). The technical paper, the analysis code, and the verification record contain the full detail.*
