"""
DVV data preprocessing

Reads DVV living history, marriage history, and relatives data, applies the preprocessing steps below and writes the result to a file.
- Set column names 
- Parse dates

Input files: 
- Tulokset_1900-1959_tutkhenk_asuinhist.txt.finreg_IDs
- Tulokset_1960-1979_tutkhenk_asuinhist.txt.finreg_IDs
- Tulokset_1980-2010_tutkhenk_asuinhist.txt.finreg_IDs
- Tulokset_1900-1959_tutkhenk_aviohist.txt.finreg_IDs
- Tulokset_1960-1979_tutkhenk_aviohist.txt.finreg_IDs
- Tulokset_1980-2010_tutkhenk_aviohist.txt.finreg_IDs
- Tulokset_1900-1959_tutkhenk_ja_sukulaiset.txt.finreg_IDs
- Tulokset_1960-1979_tutkhenk_ja_sukulaiset.txt.finreg_IDs
- Tulokset_1980-2010_tutkhenk_ja_sukulaiset.txt.finreg_IDs

Output files: 
- living_history.csv, living_history.feather
- marriages.csv, marriages.feather
- relatives.csv, relatives.feather
"""

import pandas as pd

from finregistry_data.config import (
    DVV_LIVING_HISTORY_DATA_PATHS,
    DVV_MARRIAGES_DATA_PATHS,
    DVV_RELATIVES_DATA_PATHS,
    DVV_OUTPUT_DIR,
)
from finregistry_data.utils import write_data


def preprocess_living_history(file):
    """
    Preprocess DVV Living History data
    """
    # Read data
    df = pd.read_csv(file, sep=";", dtype=str, header=None, encoding="latin-1")

    # Set column names
    cols = [
        "FINREGISTRYID",
        "RESIDENCE_TYPE",
        "START_OF_RESIDENCE",
        "END_OF_RESIDENCE",
        "MUNICIPALITY",
        "MUNICIPALITY_NAME",
        "BUILDING_ID",
        "RESIDENCE_CODE",
        "POST_CODE",
        "LATITUDE",
        "LONGITUDE",
    ]
    df.columns = cols

    # Parse dates
    date_cols = ["START_OF_RESIDENCE", "END_OF_RESIDENCE"]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="%Y%m%d")

    return df


def preprocess_marriages(file):
    """
    Preprocess DVV Marriages dataset
    """
    # Read data
    df = pd.read_csv(file, sep=";", dtype=str, header=None, encoding="latin-1")

    # Set column names
    cols = [
        "FINREGISTRYID",
        "CURRENT_MARITAL_STATUS",
        "SPOUSE_ID",
        "SPOUSE_NOT_IN_SYSTEM",
        "ORDER_NO",
        "START_DATE",
        "END_DATE",
        "ENDING_REASON",
    ]
    df.columns = cols

    # Parse dates
    date_cols = ["START_DATE", "END_DATE"]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="%Y%m%d")

    return df


def preprocess_relatives(file):
    """
    Preprocess DVV Relatives dataset
    """
    # Read data
    df = pd.read_csv(file, sep=";", dtype=str, header=None, encoding="latin-1")

    # Set column names
    cols = [
        "FINREGISTRYID",
        "RELATIONSHIP",
        "HOW_KINSHIP_HAS_FORMED",
        "RELATIVE_ID",
        "RELATIVE_BIRTH_DATE",
        "RELATIVE_DEATH_DATE",
        "SEX",
        "MOTHER_TONGUE",
        "COUNTRY_OF_RESIDENCE",
        "COUNTRY_NAME",
        "EMIGRATION_DATE",
        "HOME_TOWN",
        "MUNICIPALITY_NAME",
    ]
    df.columns = cols

    # Parse dates
    date_cols = ["RELATIVE_BIRTH_DATE", "RELATIVE_DEATH_DATE", "EMIGRATION_DATE"]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="%Y%m%d")

    return df


if __name__ == "__main__":
    from tqdm import tqdm 

    # Living history
    df = []
    for file in tqdm(DVV_LIVING_HISTORY_DATA_PATHS):
        df.append(preprocess_living_history(file))
    df = pd.concat(df, axis=0, ignore_index=True)
    write_data(df, DVV_OUTPUT_DIR, "living_history", "csv")
    write_data(df, DVV_OUTPUT_DIR, "living_history", "feather")

    # Marriages
    df = []
    for file in tqdm(DVV_MARRIAGES_DATA_PATHS):
        df.append(preprocess_marriages(file))
    df = pd.concat(df, axis=0, ignore_index=True)
    write_data(df, DVV_OUTPUT_DIR, "marriages", "csv")
    write_data(df, DVV_OUTPUT_DIR, "marriages", "feather")

    # Relatives
    df = []
    for file in tqdm(DVV_RELATIVES_DATA_PATHS):
        df.append(preprocess_relatives(file))
    df = pd.concat(df, axis=0, ignore_index=True)
    write_data(df, DVV_OUTPUT_DIR, "relatives", "csv")
    write_data(df, DVV_OUTPUT_DIR, "relatives", "feather")
