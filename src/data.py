"""Loading and cleaning for the Lab 1 dataset (dataset3-AgriculturalProduction).

All cleaning decisions live here so both notebooks use exactly the same data.
The reasoning behind each decision is in docs/step1-dataset-choice.md.
"""
import pandas as pd

from src.overview import DATA_DIR, load_dataset

CSV_PATH = DATA_DIR / "dataset3-AgriculturalProduction" / "archive3" / "Agricultural Production.csv"

RANDOM_STATE = 42
TARGET = "Yield"                      # tonnes per hectare
CATEGORICAL = ["State", "Crop", "Season"]
NUMERIC = ["Year", "Area"]

LEAKY = ["Production"]                # Yield == Production / Area exactly
UNIT_COLUMNS = ["Area Units", "Production Units"]   # constant after the Tonnes filter
HIGH_CARDINALITY = ["District"]       # 728 categories, left out for now
YIELD_UPPER_QUANTILE = 0.999          # above this: physically implausible yields


def year_to_int(series):
    """'1997-98' -> 1997, the year the growing season starts."""
    return series.str.slice(0, 4).astype("int64")


def load_agriculture(path=CSV_PATH, sample_size=40_000, random_state=RANDOM_STATE):
    """Load the CSV, apply the documented cleaning, and optionally take a random sample.

    Returns (df, notes): the cleaned DataFrame with columns CATEGORICAL + NUMERIC + [TARGET],
    and a list of human-readable notes describing how many rows each step removed.
    """
    df = load_dataset(path)
    notes = [f"Loaded {len(df):,} rows x {df.shape[1]} columns"]
    notes.append(f"Fully duplicated rows in the raw file: {int(df.duplicated().sum()):,}")

    def step(mask, reason):
        nonlocal df
        removed = int((~mask).sum())
        df = df[mask]
        notes.append(f"{reason}: removed {removed:,} rows -> {len(df):,} left")

    # One unit for the target: Bales and Nuts yields are not comparable with tonnes/hectare
    step(df["Production Units"] == "Tonnes", "Keep Production Units == 'Tonnes'")
    step(df[TARGET].notna() & df["Area"].notna() & df["Season"].notna(), "Drop missing Yield/Area/Season")
    step(df["Area"] > 0, "Drop Area <= 0")
    # Yield == 0 means nothing was recorded as harvested, not a real yield measurement
    step(df[TARGET] > 0, "Drop Yield == 0")
    upper = df[TARGET].quantile(YIELD_UPPER_QUANTILE)
    step(df[TARGET] <= upper, f"Drop Yield above the {YIELD_UPPER_QUANTILE:.1%} quantile ({upper:.1f} t/ha)")

    df = df.assign(Year=year_to_int(df["Year"]))
    df = df.drop(columns=LEAKY + UNIT_COLUMNS + HIGH_CARDINALITY)
    notes.append(f"Dropped columns: {LEAKY + UNIT_COLUMNS + HIGH_CARDINALITY}")

    if sample_size is not None and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=random_state)
        notes.append(f"Random sample of {sample_size:,} rows (random_state={random_state})")

    df = df[CATEGORICAL + NUMERIC + [TARGET]].reset_index(drop=True)
    return df, notes


def load_raw_tonnes(path=CSV_PATH):
    """Raw rows in tonnes (all columns kept) - used only for the leakage demonstration."""
    df = load_dataset(path)
    return df[df["Production Units"] == "Tonnes"]
