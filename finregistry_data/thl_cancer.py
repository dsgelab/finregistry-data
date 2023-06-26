"""
THL Cancer data preprocessing

Reads THL Cancer data, applies the preprocessing steps below and writes the result to a file.
- Rename `FINREGISTRYID` to `finregistryid`
- Parse dates

Input files: 
- fcr_data.csv.finreg_IDs

Output files: 
- cancer.txt, cancer.feather
"""

import pandas as pd
import logging

from finregistry_data.config import (
    THL_CANCER_DATA_PATH,
    THL_CANCER_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

logging.basicConfig(level=logging.INFO)


def read_data(path=THL_CANCER_DATA_PATH):
    """
    Read the data into a Pandas DataFrame.
    Column `FINREGISTRYID` is renamed to `finregistryid`.

    Args:
        path (str): File path to THL Cancer dataset

    Returns: 
        df (DataFrame): Cancer dataset
    """
    dtypes = {
        "FINREGISTRYID": str,
        "gen_henk_id": str,
        "gen_case_id": str,
        "sex": str,
        "dg_date": str,
        "dg_age": float,
        "topo": str,
        "morpho": str,
        "beh": str,
        "later": str,
        "basis": str,
        "stage": str,
        "ex_date": str,
        "dg_munic_staty": str,
        "dg_uni_staty": str,
        "dg_hosp_staty": str,
        "cancertype": str,
        "cancertype_icd10": str,
        "status_close": str,
        "multi": str,
    }
    df = pd.read_csv(path, sep=";", dtype=dtypes, decimal=",")
    logging.info(f"Cancer dataset loaded: {df.shape[0]:,} rows")

    df = df.rename({"FINREGISTRYID": "finregistryid"})
    df.columns= df.columns.str.upper()
    return df


def parse_dates(df, date_cols):
    """
    Parse dates. Invalid dates, e.g. dates too far into the future, are returned as NaT.

    Args:
        df (DataFrame): dataset with date cols
        date_cols (list of str): names for date cols

    Returns: 
        df (DataFrame): dataset with dates parsed to YYYY-MM-DD
    """
    df[date_cols] = df[date_cols].apply(
        lambda x: pd.to_datetime(x, format="%Y-%m-%d", errors="coerce").dt.date
    )
    logging.info(f"Date columns parsed")
    return df


if __name__ == "__main__":
    df = read_data()
    df = parse_dates(df, ["dg_date", "ex_date"])
    logging.info("Writing cancer dataset to a file")
    write_data(df, THL_CANCER_OUTPUT_DIR, "cancer", "csv")
    write_data(df, THL_CANCER_OUTPUT_DIR, "cancer", "feather")
