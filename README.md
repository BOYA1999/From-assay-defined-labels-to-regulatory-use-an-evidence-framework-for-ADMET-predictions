# ADMET evidence framework: reproduction materials

Reproduction materials accompanying *From assay-defined labels to regulatory use: an evidence framework for ADMET predictions*.

The [reproducibility directory](reproducibility/) contains selected source-derived inputs, frozen secondary calculations, figure source data, plotting scripts, expected outputs and file hashes. A matching archive is provided in [archives/](archives/). No manuscript or submission correspondence is included.

These checks support traceability of the review's calculations. They do not retrain the cited models, independently validate the original studies or resolve the source-correspondence limits documented in the package.

## Run

```text
cd reproducibility
python second_verification/replay.py
python -m pip install -r requirements.txt
python draw_figures.py
python build_figure04.py
python figure07_replay.py
```

See [the package README](reproducibility/README.md) for exact inputs, dependencies, expected outputs, optional source extraction and interpretation limits.

## Rights and attribution

Author-created code follows the repository's existing [MIT licence](LICENSE). Third-party source-derived materials retain the source-specific terms and attributions stated in the [rights notice](reproducibility/LICENSE_STATUS.md), source manifests and per-dataset README files. The MIT licence does not replace those source terms. No source article PDFs, original workbooks or raw DeepDelta SMILES are redistributed.

This GitHub repository is the source location. A Zenodo DOI or journal-publication claim is not implied.

Archive SHA-256: `246294417a797d31e3cbd483ba48389a3af3ad175e1f1b21c2a06bfff7b6c6dd`.
