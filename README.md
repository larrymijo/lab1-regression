# Lab 1 — Regression Models

**DA380A Machine Learning · Högskolan Kristianstad · HT2026**
Group: 28 · Members: Lawrence Arciniegas, Gunnar Arias

Practise the complete regression workflow: explore a dataset, prepare it, train at least two
regression models, evaluate them with MAE / RMSE / R², tune them with cross-validation, and
recommend the best model.

## Key dates

| Date | What |
|---|---|
| Thu 8 Oct 2026 | Lab session |
| ~15 Oct 2026 | Deadline (one week after the session; exact time on Canvas) |

**Deliverables:** one documented notebook + one PDF report, uploaded to Canvas.

## Dataset

| | |
|---|---|
| Chosen dataset | `dataset3-AgriculturalProduction` — see [docs/step1-dataset-choice.md](docs/step1-dataset-choice.md) |
| Target variable | `Yield` |
| What the target represents | Tonnes harvested per hectare sown, per state, crop, season and year (India, 1997–2020) |

Candidates: `dataset1-VideoReviews`, `dataset2-SalesTransactions2`,
`dataset3-AgriculturalProduction`, `dataset4-SalesTransactions1`, `dataset5-AirTravel`.

## How to run

1. Put the Canvas datasets in `data/`, keeping the folder names (`data/dataset3-AgriculturalProduction/archive3/Agricultural Production.csv`).
2. Open `notebooks/lab1_regression.ipynb`, select the `.venv` kernel, and **Run All**.
3. A full run takes several minutes (cross-validation and grid search on the random forest). Lower `SAMPLE_SIZE` in the setup cell while experimenting.

Cleaning lives in `src/data.py`, dataset comparison helpers in `src/overview.py`.

## Setup

Requires Python 3.10+.

```bash
git clone <repo-url>
cd lab1-regression
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
nbstripout --install --attributes .gitattributes
```

1. Download the datasets from Canvas and put them in `data/`, keeping the folder names (they are not committed).
2. Open the folder in VS Code, select the `.venv` interpreter, open a notebook in `notebooks/`.

## Project structure

| Folder | Contents |
|---|---|
| `data/` | Datasets from Canvas (git-ignored) |
| `docs/` | Planning and decisions |
| `notebooks/` | Jupyter notebooks, numbered in workflow order |
| `reports/` | The PDF report |
| `src/` | Reusable Python helpers |

## Plan

- [x] **Step 0 — Setup:** repo, virtual environment, dependencies
- [x] **Step 1 — Choose dataset:** compare all five, pick one, define and explain the target
- [ ] **Step 2 — Explore:** structure, missing values, duplicates, outliers, target distribution, relationships, observations
- [ ] **Step 3 — Prepare & split:** clean, define X / y, 80/20 train-test split, preprocessing pipeline
- [ ] **Step 4 — Models:** baseline + at least two regressors, compared with 5-fold CV on the training set
- [ ] **Step 5 — Evaluate:** MAE, RMSE, R² on the same test set
- [ ] **Step 6 — Tune:** GridSearchCV with 5-fold CV, before/after comparison
- [ ] **Step 7 — Interpret:** feature importance, strengths/weaknesses, recommendation
- [ ] **Report:** PDF answering the four required questions
- [ ] **Submit** notebook + PDF on Canvas

## Workflow rules

- Don't commit directly to `main` after setup: use a branch per task and open a pull request.
- Only one person edits a given notebook at a time.
- The test set is not used until the final evaluation (Step 5).
- `random_state=42` everywhere so results are reproducible.

## Use of AI tools

AI tools may be used for ideas, explanations and debugging, but not to copy work directly.
Every group member must be able to explain all code and text submitted.