"""
THL Social Assistance data processing 

Reads THL Social Assistance data, applies the preprocessing steps below, and writes the result to a file.
- Fix data types 
- Rename TNRO to FINREGISTRYID
- TODO: combine the two files into one

Input files: 
- 3214_FinRegistry_puolisontoitu_MattssonHannele07122020.csv.finreg_IDs
- 3214_FinRegistry_toitu_MattssonHannele07122020.csv.finreg_IDs

Output files:
- provision<YYYY-MM-DD>.csv
- provision_<YYYY-MM-DD>.feather
- spouse_provision_<YYYY-MM-DD>.csv
- spouse_provision_<YYYY-MM-DD>.feather
"""

import pandas as pd

from finregistry_data.config import (
    THL_SOCIAL_ASSISTANCE_PROVISION_DATA_PATH,
    THL_SOCIAL_ASSISTANCE_SPOUSE_PROVISION_DATA_PATH,
    THL_SOCIAL_ASSISTANCE_OUTPUT_DIR,
)
from finregistry_data.utils import write_data


def preprocess_provision(file):
    """Preprocess THL Provision (toitu)"""
    dtypes = {
        "TNRO": str,
        "TILASTOVUOSI": int,
        "KUNTA": str,
        "KUNTA_NIMI_FI": str,
        "MAAKUNTA_KOODI": str,
        "MAAKUNTA_NIMI_FI": str,
        "TAMMI": int,
        "HELMI": int,
        "MAALIS": int,
        "HUHTI": int,
        "TOUKO": int,
        "KESA": int,
        "HEINA": int,
        "ELO": int,
        "SYYS": int,
        "LOKA": int,
        "MARRAS": int,
        "JOULU": int,
        "TUKIKUUKAUSIA": int,
        "VARS_TOIMEENTULOTUKI_EUR": float,
        "VARS_TOIMEENTULOTUKI_KK": float,
        "EHKAISEVA_TOIMEENTULOTUKI_EUR": float,
        "EHKAISEVA_TOIMEENTULOTUKI_KK": float,
        "PERUS_TOIMEENTULOTUKI_EUR": float,
        "PERUS_TOIMEENTULOTUKI_KK": float,
        "TAYD_TOIMEENTULOTUKI_EUR": float,
        "TAYD_TOIMEENTULOTUKI_KK": float,
        "KUNT_TOIMINTARAHA_EUR": float,
        "KUNT_MATKAKORVAUS_EUR": float,
        "KUNT_TOIMEENTULOTUKI_KK": float,
        "LAPSIA": int,
        "MIES": int,
        "NAINEN": int,
        "SOSIOEKOASEMA": str,
        "KUUKAUDET_YHT": int,
        "MAX_MAKSUKUUKAUSI": int,
        "OSALLISTUNUT": str,
    }

    df = pd.read_csv(file, sep=";", dtype=dtypes)

    # Rename TNRO to FINREGISTRYID
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})

    return df


def preprocess_spouse_provision(file):
    dtypes = {
        "TNRO": str,
        "HAKIJA": str,
        "TILASTOVUOSI": int,
        "KUNTA": str,
        "KUNTA_NIMI_FI": str,
        "MAAKUNTA_KOODI": str,
        "MAAKUNTA_NIMI_FI": str,
        "TAMMI": int,
        "HELMI": int,
        "MAALIS": int,
        "HUHTI": int,
        "TOUKO": int,
        "KESA": int,
        "HEINA": int,
        "ELO": int,
        "SYYS": int,
        "LOKA": int,
        "MARRAS": int,
        "JOULU": int,
        "TUKIKUUKAUSIA": int,
        "VARS_TOIMEENTULOTUKI_EUR": float,
        "VARS_TOIMEENTULOTUKI_KK": float,
        "EHKAISEVA_TOIMEENTULOTUKI_EUR": float,
        "EHKAISEVA_TOIMEENTULOTUKI_KK": float,
        "PERUS_TOIMEENTULOTUKI_EUR": float,
        "PERUS_TOIMEENTULOTUKI_KK": float,
        "TAYD_TOIMEENTULOTUKI_EUR": float,
        "TAYD_TOIMEENTULOTUKI_KK": float,
        "KUNT_TOIMINTARAHA_EUR": float,
        "KUNT_MATKAKORVAUS_EUR": float,
        "KUNT_TOIMEENTULOTUKI_KK": float,
        "LAPSIA": int,
        "MIES": int,
        "NAINEN": int,
        "SOSIOEKOASEMA": str,
        "KUUKAUDET_YHT": int,
        "MAX_MAKSUKUUKAUSI": int,
        "OSALLISTUNUT": str
    }

    df = pd.read_csv(file, sep=";", dtype=dtypes)

    # Rename TNRO to FINREGISTRYID
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})

    return df

if __name__ == "__main__":
    # Provisions
    df = preprocess_provision(THL_SOCIAL_ASSISTANCE_PROVISION_DATA_PATH)
    write_data(df, THL_SOCIAL_ASSISTANCE_OUTPUT_DIR, "provision", "csv")
    write_data(df, THL_SOCIAL_ASSISTANCE_OUTPUT_DIR, "provision", "feather")

    # Spouse's provisions
    df = preprocess_spouse_provision(THL_SOCIAL_ASSISTANCE_SPOUSE_PROVISION_DATA_PATH)
    write_data(df, THL_SOCIAL_ASSISTANCE_OUTPUT_DIR, "spouse_provision", "csv")
    write_data(df, THL_SOCIAL_ASSISTANCE_OUTPUT_DIR, "spouse_provision", "feather")
