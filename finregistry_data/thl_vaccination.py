"""
THL Vaccination data preprocessing

Applies the following preprocessing steps to the data: 
- merge the two datasets into one
- parse dates
- replace missing (0) and invalid (-1, -2) values with NA 
- drop redundant columns
- replace finnish column names with english column names
"""

import pandas as pd
from config import VACCINATION_PROTECTION_PATH, VACCINATION_REGISTRY_PATH

MISSING_VALUES = [0]
INVALID_VALUES = [-1, -2]


def read_vacc_protection_data(path=VACCINATION_PROTECTION_PATH):
    dtypes = {
        "KAYNTI_ID": int,
        "JARJESTYS": int,
        "ROKOTUSSUOJA": float,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes)
    return df


def read_vacc_registry_data(path=VACCINATION_REGISTRY_PATH):
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
    Invalid dates are returned as missing (NaT).
    Invalid dates include dates with invalid format or far in the future.
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
    Missing values are denoted with empty strings and 0s.
    Invalid values are denoted with negative values (-1, -2).
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


def rename_columns(df):
    d = {
        "KAYNTI_ID": "visit_id",
        "TNRO": "finregistryid",
        "ROKOTE_ANTOPVM": "vaccination_date",
        "LAAKEAINE": "drug",
        "LAAKEAINE_SELITE": "drug_description",
        "ROKOTUSTAPA": "method",
        "PISTOSKOHTA": "injection_site",
        "LAAKEPAKKAUSNRO": "vnr",
        "ROKOTUSSUOJA": "protection",
    }
    df = df.rename(columns=d)
    return df


def preprocess_data():
    df_protection = read_vacc_protection_data(VACCINATION_PROTECTION_PATH)
    df_registry = read_vacc_registry_data(VACCINATION_REGISTRY_PATH)
    df = merge_data(df_registry, df_protection)
    df = parse_dates(df, "ROKOTE_ANTOPVM")
    df = replace_missing_and_invalid_with_na(df)
    df = drop_columns(df)
    df = rename_columns(df)
    return df_protection, df_registry, df

