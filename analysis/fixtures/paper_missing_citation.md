# Fixture: MISSING-CITATION paper (verify.py --selftest expects reconciliation to go RED)

## Methods

We apply the divergence operator D = SMA_4 - SMA_12 to weekly national % weighted
ILI on the continuous series, following the cited persistence-sign rule. The
required citation key has been removed from this fixture on purpose.

## Results

Divergence onset leads the seasonal peak by 14.148 weeks on average (floor 5 wk),
and Theorem 8b gives 13 of 13 significant predictions correct with 0 wrong.

Both sections are present and no token survives, but the citation is absent, so
the reconciliation must fail on the missing key.
