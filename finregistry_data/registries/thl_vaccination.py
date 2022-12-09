"""
THL Vaccination data preprocessing

Reads THL Vaccination data, applies the preprocessing steps below and writes the data to files.
- merge the two datasets into one
- parse dates
- replace missing (0) and invalid (-1, -2) values with NA 
- drop redundant columns
- TODO: create column COVID

Input files: 
- thl2196_rokotussuoja.csv
- thl2196_rokoterekisteri.csv.finreg_IDs

Output files: 
- vaccination_<YYYY-MM-DD>.csv
- vaccination_<YYYY-MM-DD>.feather
"""

import numpy as np
import pandas as pd
from re import IGNORECASE
from finregistry_data.config import (
    VACCINATION_PROTECTION_DATA_PATH,
    VACCINATION_REGISTRY_DATA_PATH,
    THL_VACCINATION_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

import logging

logging.basicConfig(level=logging.INFO)

MISSING_VALUES = ["0"]
INVALID_VALUES = ["-1", "-2"]


def read_vacc_protection_data(path=VACCINATION_PROTECTION_DATA_PATH):
    """Read vaccination protection data"""
    dtypes = {
        "KAYNTI_ID": int,
        "JARJESTYS": int,
        "ROKOTUSSUOJA": float,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes)
    logging.info(f"Vaccination protection dataset loaded: {df.shape[0]:,} rows")
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
        "LAAKEPAKKAUSNRO": str,
        "ROKOTE_JARJESTYS": int,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes)
    logging.info(f"Vaccination registry dataset loaded: {df.shape[0]:,} rows")
    return df


def merge_data(df_registry, df_protection):
    """
    Merge the vaccination registry dataset with the vaccination protection dataset.
    The ROKOTUSSUOJA values are grouped in lists for each KAYNTI_ID, LR_JARJESTYS pair.
    The resulting dataset contains all rows from the vaccination registry datasets.
    """
    logging.info(f"Merging datasets")
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
    logging.info(f"Parsing date column {date_col}")
    df[date_col] = pd.to_datetime(
        df[date_col], format="%d.%m.%Y %H:%M", errors="coerce"
    )
    df.loc[df[date_col].dt.year > 2100, date_col] = pd.NaT
    df[date_col] = df[date_col].dt.date
    return df


def replace_missing_and_invalid_with_na(df):
    """Replace missing and invalid values with NA"""
    logging.info("Replacing missing and invalid values")
    d = dict.fromkeys(
        ["LAAKEAINE", "ROKOTUSTAPA", "PISTOSKOHTA", "LAAKEPAKKAUSNRO"],
        MISSING_VALUES + INVALID_VALUES,
    )
    df = df.replace(d, pd.NA)
    return df


def drop_columns(df):
    logging.info("Dropping columns")
    drop = ["ROKOTE_JARJESTYS", "LR_JARJESTYS"]
    df = df.drop(columns=drop)
    return df


def add_covid_indicator(df):
    """
    Add column `COVID` to indicate rows with COVID vaccination.

    `COVID` is True if any of the following applies:
    - `LAAKEAINE_SELITE` contains "cov", "cor", "kor" "mod", "astra", "co19", "cvid" or "cominarty"  but does not contain "dukoral", "ticovac" or "vesiro"
    - `LAAKEAINE` is "J07BX03"
    - `VACCINE_PROTECTION` contains 29 
    """
    logging.info("Adding COVID")

    LAAKEAINE_INCL = "cov|cor|kor|mod|astra|co19|cvid|cominarty"
    LAAKEAINE_EXCL = "dukoral|ticovac|vesiro"
    LAAKEAINE_COVID = "J07BX03"
    PROTECTION_COVID = 29.0

    df["COVID"] = False

    df.loc[
        df["LAAKEAINE_SELITE"].str.contains(LAAKEAINE_INCL, flags=IGNORECASE, na=False),
        "COVID",
    ] = True
    df.loc[
        df["LAAKEAINE_SELITE"].str.contains(LAAKEAINE_EXCL, flags=IGNORECASE, na=False),
        "COVID",
    ] = False

    df.loc[df["LAAKEAINE"] == LAAKEAINE_COVID, "COVID"] = True

    mask = df["ROKOTUSSUOJA"].apply(
        lambda x: PROTECTION_COVID in x if x is not np.NaN else False
    )
    df.loc[mask, "COVID"] = True

    return df


def preprocess_data(df):
    """Apply the preprocessing pipeline"""
    df = parse_dates(df, "ROKOTE_ANTOPVM")
    df = parse_dates(df, "KAYNTI_ALKOI")
    df = replace_missing_and_invalid_with_na(df)
    df = drop_columns(df)
    df = add_covid_indicator(df)
    return df


if __name__ == "__main__":
    df_registry = read_vacc_registry_data(VACCINATION_REGISTRY_DATA_PATH)
    df_protection = read_vacc_protection_data(VACCINATION_PROTECTION_DATA_PATH)
    df = merge_data(df_registry, df_protection)
    df = preprocess_data(df)
    write_data(df, THL_VACCINATION_OUTPUT_DIR, "vaccination", "csv")
    write_data(df, THL_VACCINATION_OUTPUT_DIR, "vaccination", "feather")

