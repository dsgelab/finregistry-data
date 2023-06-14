"""
Kela Reimbursement data preprocessing

Reads Kela Reimbursement data, applies the preprocessing steps below and writes the result to files.
- Parse dates to YYYY-MM-DD
- Rename HETU to FINREGISTRYID
- Uppercase column names
- Remove redundant columns `APVM` and `LPVM` in drug reimbursements
- TODO: use `APVM` and `LPVM` if `ALPV` or `LOPV` are missing
- TODO: replace "Tieto puuttuu" with NAs

Input files: 
- 175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDs
- 81_522_2022_KORVAUSOIKEUDET.csv.finreg_IDs

Output files: 
- reimbursements.csv
- reimbursements.feather
- drug_reimbursements.csv
- drug_reimbursements.feather
"""

import pandas as pd

from finregistry_data.config import (
    KELA_DRUG_REIMBURSEMENTS_DATA_PATH,
    KELA_REIMBURSERMENTS_DATA_PATH,
    KELA_REIMBURSEMENT_OUTPUT_DIR,
)
from finregistry_data.utils import write_data


def preprocess_kela_reimbursements(file):
    """
    Preprocess Kela Reimbursements dataset
    """
    # Read data
    dtypes = {
        "HETU": str,
        "DIAGNOOSI_KOODI": str,
        "KORVAUSOIKEUS_KOODI": str,
        "DIAGNOOSI_SELITE": str,
        "KORVAUSOIKEUS_SELITE": str,
        "korvausoikeus_alpv": str,
        "korvausoikeus_lopv": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes)

    # Parse dates
    # Dates with year 9999 are replaced with NA
    date_cols = ["korvausoikeus_alpv", "korvausoikeus_lopv"]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    # Rename HETU to FINREGISTRYID
    df = df.rename(columns={"HETU": "FINREGISTRYID"})

    # Uppercase column names
    df.columns = df.columns.str.upper()

    return df


def preprocess_kela_drug_reimbursements(file):
    """
    Preprocess Kela Drug Reimbursements dataset
    """
    # Read data
    dtypes = {
        "HETU": str,
        "SK1": str,
        "DIAG": str,
        "APVM": str,
        "LPVM": str,
        "ALPV": str,
        "LOPV": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes)

    # Parse dates
    date_cols = ["APVM", "LPVM"]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    # Rename HETU to FINREGISTRYID
    df = df.rename(columns={"HETU": "FINREGISTRYID"})

    # Drop redundant columns APVM and LPVM
    # Note: could be checked if they contain any information when ALPV and LOPV are missing
    df = df.drop(columns=["APVM", "LPVM"])

    return df


if __name__ == "__main__":
    # Reimbursements
    df = preprocess_kela_reimbursements(KELA_REIMBURSERMENTS_DATA_PATH)
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "reimbursements", "csv")
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "reimbursements", "feather")

    # Drug reimbursements
    df = preprocess_kela_drug_reimbursements(KELA_DRUG_REIMBURSEMENTS_DATA_PATH)
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "drug_reimbursements", "csv")
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "drug_reimbursements", "feather")
