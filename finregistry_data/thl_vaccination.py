"""
THL Vaccination data preprocessing

Reads THL Vaccination data, applies the preprocessing steps below and writes the data to files.
- merge the two datasets into one
- parse dates
- replace missing (0) and invalid (-1, -2) values with NA 
- drop redundant columns

Input files: 
- thl2196_rokotussuoja.csv
- thl2196_rokoterekisteri.csv.finreg_IDs

Output files: 
- vaccination_<YYYY-MM-DD>.csv
- vaccination_<YYYY-MM-DD>.feather

TODO: move writing to utils
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from config import (
    VACCINATION_PROTECTION_DATA_PATH,
    VACCINATION_REGISTRY_DATA_PATH,
    THL_VACCINATION_OUTPUT_DIR,
)

MISSING_VALUES = [0]
INVALID_VALUES = [-1, -2]


def read_vacc_protection_data(path=VACCINATION_PROTECTION_DATA_PATH):
    """Read vaccination protection data"""
    dtypes = {
        "KAYNTI_ID": int,
        "JARJESTYS": int,
        "ROKOTUSSUOJA": float,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes)
    return df


def read_vacc_registry_data(path=VACCINATION_REGISTRY_DATA_PATH):
    """Read vaccination registry data"""
    dtypes = {
        "KAYNTI_ID": int,
        "TNRO": str,
        "ROKOTE_ANTOPVM": str,
        "LAAKEAINE": str,
        "LAAKEAINE_SELITE": str,
        "ROKOTUSTAPA": str,
        "PISTOSKOHTA": str,
        "LAAKEPAKKAUSNRO": float,
        "ROKOTE_JARJESTYS": int,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes)
    return df


def merge_data(df_registry, df_protection):
    """
    Merge the vaccination registry dataset with the vaccination protection dataset.
    The ROKOTUSSUOJA values are grouped in lists for each KAYNTI_ID, LR_JARJESTYS pair.
    The resulting dataset contains all rows from the vaccination registry datasets.
    """
    df_protection = (
        df_protection.groupby(["KAYNTI_ID", "LR_JARJESTYS"])["ROKOTUSSUOJA"]
        .agg(list)
        .reset_index()
    )
    df = df_registry.merge(df_protection, how="left", on=["KAYNTI_ID", "LR_JARJESTYS"])
    return df


def parse_dates(df, date_col):
    """
    Parse dates from dd.mm.yyyy hh:mm to yyyy-mm-dd.
    Invalid dates (invalid format, future dates) are returned as missing (NaT).
    """
    df[date_col] = pd.to_datetime(
        df[date_col], format="%d.%m.%Y %H:%M", errors="coerce"
    )
    df.loc[df[date_col].dt.year > 2100] = pd.NaT
    df[date_col] = df[date_col].dt.date
    return df


def replace_missing_and_invalid_with_na(df):
    """
    Replace missing and invalid values with NA
    """
    d = dict.fromkeys(
        ["LAAKEAINE", "ROKOTUSTAPA", "PISTOSKOHTA", "LAAKEPAKKAUSNRO"],
        MISSING_VALUES + INVALID_VALUES,
    )
    df = df.replace(d, pd.NA)
    return df


def drop_columns(df):
    drop = ["ROKOTE_JARJESTYS", "LR_JARJESTYS"]
    df = df.drop(columns=drop)
    return df


def write_data(df, outputdir, format="csv"):
    """Write data to a csv or feather file"""
    today = datetime.today().strftime("%Y-%m-%d")
    outputdir = Path(outputdir)
    if format == "csv":
        filename = "vaccination_" + today + ".csv"
        df.to_csv(outputdir / filename, sep=";", index=False)
    elif format == "feather":
        filename = "vaccination_" + today + ".feather"
        df.to_feather(outputdir / filename)
    else:
        print("Invalid file format")


def preprocess_data(df):
    """Apply the preprocessing pipeline"""
    df = merge_data(df_registry, df_protection)
    df = parse_dates(df, "ROKOTE_ANTOPVM")
    df = replace_missing_and_invalid_with_na(df)
    df = drop_columns(df)
    return df


if __name__ == "__main__":
    df_registry = read_vacc_registry_data(VACCINATION_REGISTRY_DATA_PATH)
    df_protection = read_vacc_protection_data(VACCINATION_PROTECTION_DATA_PATH)
    df = merge_data(df_registry, df_protection)
    df = preprocess_data(df)
    write_data(df, THL_VACCINATION_OUTPUT_DIR, "csv")
    write_data(df, THL_VACCINATION_OUTPUT_DIR, "feather")

