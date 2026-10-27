# Replaying the industrial optimization case plot

This package reproduces Figure 7 in the v13 review (unchanged from v12; Figure 8 in v10). Filenames use the final v13 numbering; the preserved internal plotting function name fig8 reflects the original source script.

## Scope and source

The plot shows the reported point estimates for compounds 2 and 5 from Table 1 of Rich et al., *Machine Learning ADME Models in Practice: Four Guidelines from a Successful Lead Optimization Case Study*, DOI [10.1021/acsmedchemlett.4c00290](https://doi.org/10.1021/acsmedchemlett.4c00290), PMCID PMC11318014. The article states CC BY 4.0. The five source compounds are retained in the data files to document the selection context.

The original plotting function reads structured JSON data. The CSV is a parallel export for inspection, not the input originally used by the plotting function. The JSON retains the source table locator, source XML fingerprint, all five compounds, and the limits of the comparison. No original local filesystem path is included.

The extracted `figure07_replay.py` preserves the original `canvas`, `save` and `fig8` plotting functions. Changes are limited to input/output paths, running the English figure only, and the explicitly documented portable font substitution. This is a plotting replay: it does not train a model, rerun the experiments, estimate missing uncertainty, or isolate the incremental benefit of AI. The source table supplies no replicate counts or errors for these plotted values. Papp and projected human dose are not plotted.

## Run

This review package uses Matplotlib's bundled DejaVu Sans font for the English replay; no operating-system font path is required. This explicit portability change affects typography, not plotted point values. The original Arial-based byte identity reported below is a historical check, not a promise of pixel identity for this portable version. From the directory where output is wanted, run:

```text
python path/to/figure07_replay.py
```

The script reads `figure07_plot_data.json` beside the script and writes PNG, SVG and PDF into `figure07_replay_outputs` under the working directory. It does not modify the manuscript or supplied TIFF.

## Executed check

On 2026-10-11, replay with Python 3.12, Matplotlib 3.10.8, Pillow 11.3.0 and NumPy 1.26.4 produced a 4320 × 2490 pixel English PNG identical to the supplied v10 PNG by both file SHA-256 and decoded RGB comparison. The PNG SHA-256 was `0524dd5f49240670125dfaec547b2610c744c8b9c0632fa7823f66daee0cee1e`. Rendering with other library versions or fonts may change pixels without changing the plotted point values. This result establishes the local replay of the supplied plot, not scientific validation of the source study.

The original figure and this extraction were prepared with Codex-assisted Python/Matplotlib. This software is distributed under the target repository's existing MIT licence; the cited source-derived data retain their documented attribution and terms.

In v14, the industrial measurements also appear in Figure 4(d–f); the legacy filename remains unchanged to preserve provenance.
