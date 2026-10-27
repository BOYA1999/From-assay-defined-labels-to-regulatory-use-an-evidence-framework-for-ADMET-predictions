# Secondary verification of selected source records

Prepared for the v13 review on 11 October 2026. This directory makes four previously completed checks traceable and executable. It does not add a new benchmark, train a model or reconstruct an unresolved original analysis. Figure 7 has its separate CSV, JSON, script and README one directory above.

## Contents and execution

`data/` contains six CSV files: raw-string equality hashes and the seed-0 folds for HepClear; PPB observations/predictions and source-labelled summaries; the seven-drug biliary inputs; and Nature source columns and field mappings. `source_manifest.json` gives the original URLs, versions, SHA-256 fingerprints and source rights statements. `frozen_nature_checks.json` preserves the previously recorded valid/excluded rows and finite-pair results, without transferring the earlier exploratory p-values into this package.

Run the supplied data with Python 3.10 or later; the replay uses only the standard library:

```text
python path/to/second_verification/replay.py
```

It writes `replay_outputs/results.json` and `replay_outputs/nature_masks.csv` in the current directory. `expected_outputs/` contains the executed results. All fixed-count, PPB-summary, biliary-correlation and Nature-frozen-result checks passed using Python 3.12.0 on 11 October 2026. The mask CSV identifies every included and excluded source row for every Nature endpoint/model combination. A replay match is a check of these calculations, not a confirmation of the studies' overall validity.

For an independent source-to-CSV check, obtain the four original files listed in `source_manifest.json`, keep the recorded filenames in one folder and run:

```text
python path/to/second_verification/extract_inputs.py path/to/originals
```

This writes `extracted_inputs/` in the current directory, verifies all four source fingerprints before extraction, and prints the six CSV fingerprints for comparison with `expected_outputs/results.json`. Source extraction was executed with NumPy 1.26.4, openpyxl 3.1.5 and xlrd 2.0.2. These packages are not redistributed. The script does not download files, run source-repository software or change the supplied inputs. A different remote version must not be silently substituted for a fingerprinted snapshot.

## Fixed rules and their interpretation

**DeepDelta / HepClear — DOI 10.1186/s13321-023-00769-x.** The pinned source contains 881 records and 775 different raw SMILES strings. Identity is exact string equality after ordinary CSV decoding, without trimming, canonicalisation, salt removal, tautomer merging or stereochemical changes. The CSV stores SHA-256 equality labels instead of redistributing the raw structures. The seed-0 row assignment implements the published `KFold(10, shuffle=True, random_state=0)` rule through the same NumPy RandomState permutation and fold sizes; its assignments were independently compared with scikit-learn 1.8.0. The ten train/test intersections contain 19, 19, 21, 16, 18, 21, 21, 21, 21 and 11 distinct raw strings. Only seed 0 is included in this identity audit; the original study used five repeats. These intersections show that record separation does not guarantee chemical-identity separation. They do not quantify any effect on predictive performance.

**PPB — DOI 10.1016/j.ejps.2024.106946.** The official SI sheets `25 new measurements_set`, `PFC_test_set` and `PFC99_test_set` supply 25, 63 and 36 rows, respectively. Observed values are in C for the first sheet and F for the others; seven prediction columns begin at D and H, respectively, with every other column used. The exports retain exact worksheet row/cell locators, the observations, all seven predictions and the 21 source-labelled R² summaries. Squared Pearson correlation is calculated as corr(observed,predicted)²; predictive R² is 1−Σ(observed−predicted)²/Σ(observed−mean(observed))². RMSE uses percentage-point units. All 21 source summaries match Pearson r² within 10⁻¹², whereas the article's Eq. (4) specifies predictive R². The two definitions are therefore kept distinct. No statistical or model-performance correction is substituted into the review.

**Biliary study — DOI 10.1038/s42003-023-05216-z.** For the `Figure 5d, 5e` sheet, JFC uses E3:E23 and HUM181001B E27:E47, with three consecutive replicate entries per drug. Seven arithmetic means and sample SDs are checked against the cached F/G values. The seven means are paired with J3:J9 in the recorded drug order. Pearson correlation is calculated without transformation or rounding, with seven drugs as the unit rather than 21 replicate wells. The resulting r values are 0.969373983314 and 0.942444673678; the article reports 0.969 and 0.966. This replay preserves that already disclosed discrepancy. The correspondence to the authors' original analysis remains unresolved; the second computed value is not a correction of the published value. No new filters or transformations were tried in preparing v13.

**Nature study — DOI 10.1038/s41586-026-11013-5.** `Fig 4` rows 229–485 and the supplied transformed columns are used exactly as recorded in `nature_field_mapping.csv`; source summary cells are given there separately. Finite numerical pairs are retained, including zero and negative values. Blank/non-numerical/non-finite entries are excluded per pair. There is no imputation, rounding, deduplication, recalculation of the supplied transformation or search for extra filters. Spearman rho is Pearson correlation of average ranks. All 16 calculations and retained row sets match the frozen checks. The export contains 257 source rows representing 254 different analogue identifiers and 18 parent identifiers; these are different counting units. Shared parents also preclude treating the pairs as independent evidence for platform comparisons. Differences from the source summaries document the result of this specific rule only: final publication masks, exclusions and version/column correspondence remain unresolved. The review uses the study to describe an experimental comparison setting, not to rank platforms from these replays.

## Attribution and rights

The PPB numerical extracts are from Han et al., *The state-of-the-art machine learning model for plasma protein binding prediction: Computational modeling with OCHEM and experimental validation* (2024). The biliary extracts are from Arakawa et al., *Induction of open-form bile canaliculus formation by hepatocytes for evaluation of biliary drug excretion* (2023). The Nature extracts are from *Development of a random background to understand ligand optimization* (2026). Their source articles state [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); extraction, conversion to CSV and the review's calculations are the changes made here. DOIs, source files and snapshot fingerprints are retained in the manifest. No full article or source workbook is included.

DeepDelta's article is open access under CC BY 4.0. Its repository separately states a Duke University software licensing arrangement (GPLv2 for non-commercial academic use or a custom commercial licence); see the pinned licence link in the manifest. This directory contains an independent record-counting implementation and derived equality hashes, not redistributed repository source code or benchmark SMILES. The original dataset provenance remains that of the cited source and repository. The independent author-created code follows the target repository's existing MIT licence; third-party materials retain their source-specific terms. See the package-level LICENSE_STATUS.md.
