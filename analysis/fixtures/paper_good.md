# Fixture: GOOD paper (verify.py --selftest expects this to pass reconciliation)

## Methods

We apply the divergence operator D = SMA_4 - SMA_12 to weekly national % weighted
ILI on the continuous series, following the cited persistence-sign rule
(Kim 2026d \cite{kim2026d}). All values in this fixture are already rendered
(no curly-brace tokens remain), exactly as the manuscript will be after render_claims.py.

## Results

Divergence onset leads the seasonal peak by 14.148 weeks on average (floor 5 wk),
and Theorem 8b gives 13 of 13 significant predictions correct with 0 wrong.

This fixture is intentionally complete: both required sections are present, the
required citation key kim2026d appears, and no unrendered token survives.
