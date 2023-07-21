"""
Kela Reimbursement data preprocessing

Reads Kela Reimbursement data, applies the preprocessing steps below and writes the result to files.
- Parse dates to YYYY-MM-DD
- Rename HETU to FINREGISTRYID
- Uppercase column names
- Combine date columns in 175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDs
- Harmonize ICD code formats (remove dots from ICD codes)
- Concat the data into one file

Input files: 
- 175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDs
- 81_522_2022_KORVAUSOIKEUDET.csv.finreg_IDs

Output files: 
- reimbursements.csv
- reimbursements.feather
"""

import pandas as pd
import numpy as np

from finregistry_data.config import (
    KELA_REIMBURSEMENTS_175_DATA_PATH,
    KELA_REIMBURSEMENTS_81_DATA_PATH,
    KELA_REIMBURSEMENT_OUTPUT_DIR,
)
from finregistry_data.utils import write_data


def preprocess_reimbursements_81(file):
    """
    Preprocess Kela Reimbursements 81_522_2022_KORVAUSOIKEUDET.csv.finreg_IDs dataset
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

    # Uppercase column names
    df.columns = df.columns.str.upper()

    # Rename columns
    df = df.rename(columns={"HETU": "FINREGISTRYID"})

    # Remove dots from ICD codes
    df["DIAGNOOSI_KOODI"] = df["DIAGNOOSI_KOODI"].str.replace(".", "", regex=False)

    return df


def preprocess_reimbursements_175(file):
    """
    Preprocess Kela Reimbursements 175_522_2020_LAAKEKORVAUSOIKEUDET.csv.finreg_IDs dataset
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

    # Parse APVM and LPVM with format YYYYMM
    # Use 15th as the date as exact dates are missing
    for date_col in ["APVM", "LPVM"]:
        df[date_col] = df[date_col].astype(str) + "15"
        df[date_col] = pd.to_datetime(
            df[date_col], format="%Y%m%d", errors="coerce"
        ).dt.date

    # Parse ALPV & LOPV with format YYYY-MM-DD
    for date_col in ["ALPV", "LOPV"]:
        df[date_col] = pd.to_datetime(
            df[date_col], format="%Y-%m-%d", errors="coerce"
        ).dt.date

    # Merge APVM with ALPV and LOPV with LPVM
    # Use APVM/LPVM by default and insert ALPV/LOPV if APVM/LPVM is missing
    df["ALPV"] = np.where(df["ALPV"].isnull(), df["APVM"], df["ALPV"])
    df["LOPV"] = np.where(df["LOPV"].isnull(), df["LPVM"], df["LPVM"])

    # Drop redundant columns APVM and LPVM
    df = df.drop(columns=["APVM", "LPVM"])

    # Rename columns
    df = df.rename(
        columns={
            "HETU": "FINREGISTRYID",
            "SK1": "KORVAUSOIKEUS_KOODI",
            "DIAG": "DIAGNOOSI_KOODI",
            "ALPV": "KORVAUSOIKEUS_ALPV",
            "LOPV": "KORVAUSOIKEUS_LOPV",
        }
    )

    # Add missing columns as NAs
    df["DIAGNOOSI_SELITE"] = pd.NA
    df["KORVAUSOIKEUS_SELITE"] = pd.NA

    # Remove dots from ICD codes
    df["DIAGNOOSI_KOODI"] = df["DIAGNOOSI_KOODI"].str.replace(".", "", regex=False)

    return df


def concat_data(df1, df2):
    """
    Concat data into a single dataframe and drop duplicated values
    """
    cols = [
        "FINREGISTRYID",
        "DIAGNOOSI_KOODI",
        "DIAGNOOSI_SELITE",
        "KORVAUSOIKEUS_KOODI",
        "KORVAUSOIKEUS_SELITE",
        "KORVAUSOIKEUS_ALPV",
        "KORVAUSOIKEUS_LOPV",
    ]
    df = pd.concat([df1[cols], df2[cols]], ignore_index=True)
    df = df.drop_duplicates(
        subset=[
            "FINREGISTRYID",
            "KORVAUSOIKEUS_ALPV",
            "KORVAUSOIKEUS_LOPV",
            "DIAGNOOSI_KOODI",
            "KORVAUSOIKEUS_KOODI",
        ],
        keep="first",
    )
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    df1 = preprocess_reimbursements_81(KELA_REIMBURSEMENTS_81_DATA_PATH)
    df2 = preprocess_reimbursements_175(KELA_REIMBURSEMENTS_175_DATA_PATH)
    df = concat_data(df1, df2)
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "reimbursements", "csv")
    write_data(df, KELA_REIMBURSEMENT_OUTPUT_DIR, "reimbursements", "feather")
