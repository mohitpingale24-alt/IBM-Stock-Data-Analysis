# SpaceX Falcon 9 Applied Data Science Capstone

This folder contains an executed reconstruction of the IBM capstone, its source datasets, Python files, and the final presentation. The original stock-analysis notebook remains at the repository root.

## Final presentation

- [Submission PDF](reports/Data%20Science%20Capstone%20Project%20Report.pdf)
- [Editable PowerPoint](reports/SpaceX%20Falcon%209%20Capstone%20Presentation.pptx)

## Executed notebooks

1. [API / course snapshot collection](notebooks/01_data_collection_api.ipynb)
2. [Web scraping](notebooks/02_web_scraping.ipynb)
3. [Data wrangling](notebooks/03_data_wrangling.ipynb)
4. [EDA visualizations](notebooks/04_eda_visualizations.ipynb)
5. [Ten SQL queries](notebooks/05_eda_sql.ipynb)
6. [Folium maps](notebooks/06_folium_maps.ipynb)
7. [Plotly Dash](notebooks/07_plotly_dash.ipynb)
8. [Predictive analysis](notebooks/08_predictive_analysis.ipynb)

## Run

From this folder:

```bash
python -m pip install -r requirements.txt
python src/train_and_analyze.py
python src/dashboard.py
```

The dashboard runs locally on port 8050. Open notebooks in Jupyter and run all cells. The notebooks use retained inputs so their analysis does not require a working external API.

## Evidence boundaries

These are newly executed reconstructions, not copies of previously unshared learner notebooks. The live community SpaceX API timed out during preparation. Notebook 01 explicitly uses IBM's published API-derived CSV and includes its source and checksum. `src/collect_api.py` is an optional live collector that reports failures honestly.

Notebook 02 parses separately retrieved Wikipedia HTML from the 2010–2019 launch list, including Falcon Heavy. It does not replace the course modeling data. Wikipedia text remains attributable to its contributors and is subject to its applicable license. Source: https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2010%E2%80%932019), retrieved 27 October 2026.

The 90-row EDA/modeling snapshot, 101-row SQL snapshot and 56-row geographic/dashboard snapshot are intentionally separate. Source URLs and SHA-256 checksums are in `data/sources.json`. Original IBM template artwork and course datasets remain attributable to their owners. Maps retain OpenStreetMap attribution.

Class 1 includes successful ocean landings. Unknown/no-attempt outcomes join Class 0, so this is not a pure reusable-booster recovery target. Map proximity coordinates are illustrative sample points, not verified nearest-feature distances.

## Reconstructed model results

Stratified train/test split 72/18, seed 42. Five-fold stratified CV tunes training-only preprocessing and each model. Tree test accuracy is 15/18 (83.3%). KNN has the highest mean CV accuracy (89.0%) and test accuracy 14/18 (77.8%). SVM is nearly tied on CV. This small historical sample does not establish production forecasting performance. Prior payload imputation, repeated booster history and potentially retrospective ReusedCount require further validation.

## Rubric navigation in the 50-page PDF

Executive summary 3; introduction 4; methodology 6–15; EDA figures 18–23; SQL 24–33; Folium 35–37; Dash 39–41; classification 43–44; conclusions 45; reproducibility and sources 46–49. Repository URLs appear on slides 2, 46 and 49.
