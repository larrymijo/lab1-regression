# Step 1 — Choosing the dataset

**Decision: `dataset3-AgriculturalProduction`, target `Yield` (tonnes per hectare).**

## The five candidates

| Dataset | Files | Rows | Verdict |
|---|---|---|---|
| dataset1-VideoReviews | 3 | 224 / 55,292 / 111,857 | Would need joining files; invisible soft-hyphen characters inside column names; the per-video file has only 224 rows |
| dataset2-SalesTransactions2 | 1 | 536,350 | Only 8 columns; a revenue target would just be `Price × Quantity` (leakage); 1,406 product names as the main feature |
| **dataset3-AgriculturalProduction** | **1** | **345,407** | **Chosen** |
| dataset4-SalesTransactions1 | 4 (`annex1`–`annex4`) | 251 / 878,503 / 55,982 / 251 | Requires joining four files on Item Code and Date before anything else |
| dataset5-AirTravel | 2 (`business`, `economy`) | 93,487 + 206,774 | Clear target (`price`), but every column needs text parsing (`"25,612"`, `"02h 00m"`, `" non-stop "`) |

## Scoring (1 = poor, 3 = good)

| Criterion | VideoReviews | SalesTx2 | Agricultural | SalesTx1 | AirTravel |
|---|---|---|---|---|---|
| Clear numeric target | 2 | 2 | 3 | 2 | 3 |
| Enough rows | 2 | 3 | 3 | 3 | 3 |
| Useful features | 2 | 1 | 3 | 2 | 3 |
| Manageable data quality | 1 | 2 | 3 | 1 | 2 |
| We understand the domain | 2 | 3 | 3 | 2 | 3 |
| No obvious leakage (or easy to remove) | 1 | 1 | 2 | 2 | 3 |
| **Total** | **10** | **12** | **17** | **12** | **17** |

AgriculturalProduction and AirTravel tie on score. **AgriculturalProduction wins on effort**: one file, almost no text parsing (only `Year`), so the lab time goes into modelling and interpretation rather than string cleaning.

## What the dataset contains

Indian crop statistics per **State → District → Crop → Season → Year**, 1997-98 to 2020-21.

| Column | Type | Notes |
|---|---|---|
| `State` | categorical | 36 states |
| `District` | categorical | 728 districts |
| `Crop` | categorical | 52 crops in the tonnes subset (rice, maize, wheat, sugarcane, …) |
| `Year` | text `"1997-98"` | 24 seasons → converted to the start year (1997) |
| `Season` | categorical | Kharif, Rabi, Whole Year, Summer, Winter, Autumn |
| `Area` | numeric | hectares sown |
| `Area Units` | constant | always `Hectare` |
| `Production` | numeric | amount harvested |
| `Production Units` | categorical | `Tonnes` 331,686 · `Bales` 10,794 · `Nuts` 2,927 |
| `Yield` | numeric | **target** |

## The target

**`Yield` = tonnes harvested per hectare sown.** It measures how productive a field was, independent of how big it is. Predicting it tells a planner what harvest to expect per hectare for a given crop, season, place and year.

## Cleaning decisions (implemented in `src/data.py`)

| Decision | Rows affected | Why |
|---|---|---|
| Keep `Production Units == "Tonnes"` | −13,721 | Yields in bales or nuts per hectare are not comparable with tonnes per hectare |
| Drop rows with missing `Yield` / `Area` / `Season` | −33 | Can't use a row without a target; too few to be worth imputing |
| Drop `Yield == 0` | −5,644 | Zero means nothing was recorded as harvested, not a real measurement |
| Drop `Yield` above the 99.9th percentile (113.3 t/ha) | −327 | Physically implausible (the maximum was 9,801 t/ha). High yields are otherwise **kept**: sugarcane really has a median of 55 t/ha |
| `Year "1997-98"` → `1997` | — | Makes the trend over time usable as a number |
| Drop **`Production`** | — | **Leakage**: `Yield == Production / Area` exactly (max difference 5.7 × 10⁻¹⁴). With `Production` and `Area` as features the model would just rebuild the formula |
| Drop `Area Units`, `Production Units` | — | Constant after the filter |
| Drop `District` | — | 728 categories would give ~730 one-hot columns and slow every model down a lot; `State` keeps the geographic signal. Listed as future work |
| Random sample of 40,000 rows (`random_state=42`) | 325,682 → 40,000 | A random forest on all 325k rows takes several minutes per fit on our laptops; 40k rows keeps cross-validation and grid search to a few minutes. Documented in the report |

The raw file has **0 fully duplicated rows**.

**Final features:** `State`, `Crop`, `Season` (one-hot encoded) and `Year`, `Area` (numeric).
