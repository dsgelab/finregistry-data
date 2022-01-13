"""
THL Vaccination data preprocessing

Applies the following preprocessing steps to the data: 
- merge the two datasets into one
- TODO: replace missing values (0 or empty) with NA 
- TODO: replace invalid values (negative values) with NA 
- TODO: replace finnish column names with english column names
- TODO: parse dates
- TODO: drop redundant columns
"""

from os import register_at_fork
import pandas as pd
from config import VACCINATION_PROTECTION_PATH, VACCINATION_REGISTRY_PATH


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


def preprocess_data():
    df_protection = read_vacc_protection_data(VACCINATION_PROTECTION_PATH)
    df_registry = read_vacc_registry_data(VACCINATION_REGISTRY_PATH)
    df = merge_data(df_registry, df_protection)
    return df_protection, df_registry, df

