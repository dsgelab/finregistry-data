"""
THL Vaccination data preprocessing

Applies the following preprocessing steps to the data: 
- replace missing values (0 or empty) with NA 
- TODO: replace invalid values (negative values) with NA 
- TODO: replace finnish column names with english column names 
- TODO: merge the two datasets into one
- TODO: parse dates

"""

import pandas as pd
from config import VACCINATION_PROTECTION_PATH, VACCINATION_REGISTRY_PATH


def read_vacc_protection_data(path=VACCINATION_PROTECTION_PATH):
    dtypes = {
        "KAYNTI_ID": int,
        "JARJESTYS": float,
        "ROKOTUSSUOJA": float,
        "LR_JARJESTYS": float,
    }
    na_values = [0]
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes, na_values=na_values)
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
        "ROKOTE_JARJESTYS": float,
        "LR_JARJESTYS": float,
    }
    na_values = [0]
    df = pd.read_csv(path, sep=";", header=0, dtype=dtypes, na_values=na_values)
    return df


def main():
    df_vacc_protection = read_vacc_protection_data(VACCINATION_PROTECTION_PATH)
    df_vacc_registry = read_vacc_registry_data(VACCINATION_REGISTRY_PATH)
    print(df_vacc_protection.head)
    print(df_vacc_registry.head)

