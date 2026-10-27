# Local replay check

Repository: https://github.com/BOYA1999/From-assay-defined-labels-to-regulatory-use-an-evidence-framework-for-ADMET-predictions

This document records local replay checks; it does not assert journal acceptance or a DOI.

Checked on 2026-10-27 using Python 3.12.14, NumPy 2.5.4, Matplotlib 3.11.2 and Pillow 13.0.0. Dependencies were supplied by an installed local runtime; this was not an independent clean-machine test.

- All four replay/plot commands completed successfully.
- All frozen result fields agree with the original expected results within absolute tolerance 1e-12; Python-version metadata is excluded from the scientific comparison. Maximum absolute numerical difference: 0.0.
- Nature mask CSV is byte-identical to the expected mask.
- Figure 4 decoded RGB pixels are identical to the prepared v14 PNG (2130 x 1560); its 20 plotted values are in the accompanying CSV.
- Legacy industrial data are unchanged. The portable font differs explicitly from the historical Arial-based renderer; no legacy pixel-identity claim is made.
- Figures 2, 3 and 5 are explanatory diagrams, not fitted results.

Measured elapsed times on the preparation machine:

- `second_verification/replay.py`: 0.092 seconds.
- `draw_figures.py`: 1.42 seconds.
- `build_figure04.py`: 0.956 seconds.
- `figure07_replay.py`: 0.754 seconds.

These checks reproduce supplied calculations and rendering; they do not independently validate the cited studies. Original-source extraction was not rerun.

Figure 4 readability update: 7.1 x 5.2 inches; minimum labels 8.2 pt, equivalent to 7.39 pt at 6.4-inch Word width. All 20 values remain unchanged; compact replay is RGB-identical to the updated v14 PNG.

## Final GitHub package check (27 October 2026)

The package was invoked from a different working directory. The five commands below all completed successfully; draw_figures.py also invokes the current draw_figure5.py. Frozen numerical values match exactly apart from Python-version metadata, and Nature masks are byte-identical. The new nonsequential Figure 5 replay is RGB-identical to the visually checked final figure. Original numerical inputs and known interpretation limits remain unchanged. No independent-source extraction or model training was run.

- `second_verification/replay.py`: 0.09 seconds.
- `draw_figures.py`: 1.833 seconds.
- `draw_figure5.py`: 0.668 seconds.
- `build_figure04.py`: 0.785 seconds.
- `figure07_replay.py`: 0.748 seconds.
