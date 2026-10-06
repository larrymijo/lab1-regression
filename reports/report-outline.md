# Lab 1 report — outline

DA380A Machine Learning · Group 28 · Lab 1: Regression Models

The PDF should **interpret and compare** the models, not repeat the code. Numbers come from `notebooks/lab1_regression.ipynb`. Aim for 3–5 pages with 2–4 figures.

## 1. Introduction (½ page)
- Dataset: `dataset3-AgriculturalProduction`, Indian crop statistics 1997-98 to 2020-21.
- Target: `Yield`, tonnes harvested per hectare sown. Why it is useful to predict.
- Why this dataset over the other four (one sentence; details in `docs/step1-dataset-choice.md`).

## 2. Data and preparation (1 page)
- Raw size 345,407 × 10. Kept tonnes only (−13,721), removed `Yield == 0` (−5,644) and implausible yields above the 99.9th percentile, 113.3 t/ha (−327). 325,682 usable rows; random sample of 40,000 for training time.
- **Leakage:** `Yield == Production / Area` exactly → `Production` removed. Mention the demonstration (section 7.4 of the notebook): R² ≈ … with it, which is meaningless.
- Features: `State`, `Crop`, `Season` (one-hot), `Year`, `Area` (log + standardised). `District` left out (728 categories).
- Outliers: the IQR rule flags ~15% of rows, but they are real high-yield crops (sugarcane ≈ 56 t/ha) → kept.
- 80/20 split; 5-fold cross-validation on the training set for comparison and tuning.
- Figure: yield distribution or yield per crop boxplot.

## 3. Required question 1 — compare the models with MAE, RMSE and R²
Table from notebook section 5/6:

| Model | MAE (t/ha) | RMSE (t/ha) | R² |
|---|---|---|---|
| Dummy (mean) | … | … | … |
| Linear Regression | … | … | … |
| Ridge (tuned) | … | … | … |
| Random Forest | … | … | … |
| Random Forest (tuned) | … | … | … |

Explain in the problem's terms: "on average the forest is off by … tonnes per hectare", why RMSE is much larger than MAE (a few large errors on high-yield crops), what R² means here. Include the effect of tuning (before/after).

## 4. Required question 2 — most influential features
- Method: permutation importance on the test set (works for both models, on the original columns).
- Ranking: … (expected: Crop far ahead, then Season / State, Area and Year small).
- Compare with the Ridge coefficients. Figure: permutation importance bar chart.

## 5. Required question 3 — strengths and weaknesses
Use the table in notebook section 7.5: accuracy, interpretability, training time, extrapolation (negative predictions from the linear model), coping with the skewed target, preprocessing needs. Mention residual plot findings and which crops have the largest errors.

## 6. Required question 4 — recommendation
Which model and why, backed by the test numbers. Limitations: sample instead of full data, no `District`, skewed target. Improvements: log target, District with rare-category grouping, gradient boosting, full data.

## 7. Conclusion (3–4 sentences)
