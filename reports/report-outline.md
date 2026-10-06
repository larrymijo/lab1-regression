# Lab 1 report — outline with results

DA380A Machine Learning · Group 28 · Lab 1: Regression Models

The PDF should **interpret and compare** the models, not repeat the code. Every number below comes from `notebooks/lab1_regression.ipynb` (the section is given in brackets). Aim for 3–5 pages with 2–4 figures. Write it in your own words: you must be able to explain every sentence.

## 1. Introduction (½ page)
- Dataset: `dataset3-AgriculturalProduction` — Indian crop statistics per state, district, crop, season and year, 1997-98 to 2020-21.
- Target: `Yield` = tonnes harvested per hectare sown. Useful for planning: what harvest per hectare to expect for a crop, place, season and year.
- Why this dataset: one file, a clear numeric target, a mix of categorical and numeric features, and almost no text parsing (details in `docs/step1-dataset-choice.md`).

## 2. Data and preparation (1 page)
- Raw data: 345,407 rows × 10 columns, 0 duplicated rows, little missing data. [1.2]
- Kept only rows measured in tonnes (−13,721), dropped missing values (−33), `Yield == 0` (−5,644) and impossible yields above the 99.9th percentile, 113.3 t/ha (−327; the raw maximum was 9,801). → 325,682 usable rows; random sample of **40,000** to keep training time reasonable. [1.4]
- **Leakage:** `Yield == Production / Area` exactly. A linear regression on log(Production) and log(Area) gets **R² = 1.0000** with coefficients +1 and −1 — it just rediscovers the formula. `Production` is therefore removed. [1.3, 7.4]
- Features: `State`, `Crop`, `Season` (one-hot encoded), `Year`, `Area` (log + standardised) → 94 columns after preprocessing. `District` left out (728 categories). [2, 3]
- Target is strongly right-skewed (skew 4.96). The IQR rule flags 14.6% of rows, but they are real high-yield crops (sugarcane median 56 t/ha) → kept. [1.5, 1.6]
- 80/20 split (32,000 / 8,000 rows); 5-fold cross-validation on the training set for comparison and tuning. [3]
- Suggested figure: yield per crop boxplot [1.6].

## 3. Question 1 — compare the models with MAE, RMSE and R²

Test set (8,000 rows) [5, 6]:

| Model | MAE (t/ha) | RMSE (t/ha) | R² |
|---|---|---|---|
| Dummy (mean) | 5.55 | 11.51 | 0.000 |
| Linear Regression | 2.47 | 5.46 | 0.775 |
| Ridge (tuned, α = 1) | 2.47 | 5.46 | 0.775 |
| Random Forest | 0.97 | 3.11 | 0.927 |
| Random Forest (tuned) | 0.98 | 3.09 | 0.928 |

Cross-validation (training set): Linear Regression R² 0.758 ± 0.023, Random Forest R² 0.914 ± 0.015. [4]

Points to make:
- The forest's MAE is 61% lower and its RMSE 43% lower than linear regression's.
- RMSE is 2–3 times MAE for both models → a minority of large errors on high-yield crops dominates RMSE.
- Linear Regression: train R² 0.762 ≈ test 0.775 → **underfitting**; predicts **negative yields for 1,571 of 8,000 test rows (≈ 20%)**. [5]
- Random Forest: train R² 0.988 vs test 0.927 → some **overfitting**, but CV and test agree, so the result is stable. [5]
- On ordinary yields (≤ 5 t/ha, ≈ 85% of rows): MAE 0.37 t/ha for the forest vs 1.48 for Ridge. [7.3]
- Tuning: Ridge unchanged (regularisation can't fix underfitting). Forest: CV RMSE 3.439 → 3.402 (−1.1%), and each fit about 3.4 times faster (≈ 33 s vs ≈ 113 s) with `max_features = 0.3`. Larger leaves (`min_samples_leaf = 4`) made it worse. [6]
- Suggested figure: predicted vs actual for both models [5].

## 4. Question 2 — most influential features
- Method: **permutation importance** on the test set — shuffle one column at a time and measure how much RMSE gets worse. Works for both models and on the original columns. [7.1]

| Feature | Random Forest (tuned) | Ridge (tuned) |
|---|---|---|
| Crop | 11.79 | 9.92 |
| State | 3.39 | 0.34 |
| Season | 1.29 | 0.01 |
| Year | 0.82 | 0.04 |
| Area | 0.54 | 0.03 |

(Increase in RMSE in t/ha when the column is shuffled.)
- Crop dominates both models. The forest also uses State and Season, through interactions (the same crop yields differently in different states and seasons) — that explains most of the accuracy gap.
- Ridge coefficients agree: the largest positive effects are sugarcane (+50.7), banana (+25.6), tapioca, potato, onion. [7.2]
- Suggested figure: permutation importance bar chart [7.1].

## 5. Question 3 — strengths and weaknesses
Use the table in notebook section 7.5. Main points:
- **Linear / Ridge:** fast, interpretable (one coefficient per feature), but underfits, can't model interactions, struggles with the skewed target, predicts impossible negative yields.
- **Random Forest:** much more accurate, captures interactions and non-linear effects, never predicts outside the training range; but slower, harder to interpret, overfits somewhat.
- Where both struggle: high-yield crops. Forest MAE per crop: sugarcane 9.9, banana 7.1, dry ginger 6.7 t/ha. [7.3]

## 6. Question 4 — recommendation
- Recommend the **tuned Random Forest**: test MAE 0.98 t/ha, RMSE 3.09 t/ha, R² 0.928, vs R² 0.775 for Ridge. [7.6]
- Limitations: 40,000-row sample, no `District`, raw (skewed) target.
- Improvements: full data, `District` with rare districts grouped, predict log(Yield), try gradient boosting.

## 7. Conclusion (3–4 sentences)
What you did, the main result, which model won and why, one improvement.
