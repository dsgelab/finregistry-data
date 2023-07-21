"""
SF SES (socioeconomic status) preprocessing

Reads SF SES data, applies the preprocessing steps below and writes the result to files.
- Harmonize column names
- Remove rows with no information apart from `finregistryid`
- Drop duplicated rows

Input files: 
- ammatti_u1442_a.csv.finreg_IDs
- ammatti_u1442_al10.csv.finreg_IDs

Output files: 
- ses_<YYYY-MM-DD>.csv
- ses_<YYYY-MM-DD>.feather
"""

from finregistry_data.config import (
    SF_SES_DATA_PATHS,
    SF_SOCIOECONOMIC_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def read_data(paths):
    """
    Read SES data.

    Args:
        paths (list of str): paths to input data files

    Returns:
        A list of dataframes
    """
    logging.info("Reading data")

    dtypes = {
        "FINREGISTRYID": str,
        "F1": str,
        "vuosi": float,
        "psose": str,
        "sose": str,
    }

    dfs = []

    dfs.append(pd.read_csv(paths[0], sep=",", dtype=dtypes))
    logging.info(f"File 1/2 imported: {dfs[0].shape[0]:,} rows")

    dfs.append(pd.read_csv(paths[1], sep=";", dtype=dtypes))
    logging.info(f"File 2/2 imported: {dfs[1].shape[0]:,} rows")

    return dfs


def merge_data(dfs):
    """
    Merge data into a single dataframe:
    - harmonize column names
    - add missing `psose` to the data update file

    Args:
        dfs (list of dataframes): List of input dataframes

    Returns:
        A combined dataframe with duplicates removed
    """
    logging.info("Merging data")

    # Harmonize column names
    dfs[0] = dfs[0].rename(columns={"FINREGISTRYID": "finregistryid"})
    dfs[1] = dfs[1].rename(columns={"F1": "finregistryid"})

    # Add the missing `pamko` variable
    dfs[1]["psose"] = pd.NA

    # Merge data
    df = pd.concat(dfs, ignore_index=True)
    logging.info(f"{df.shape[0]:,} rows in the merged dataframe")

    return df


def drop_empty_rows(df):
    """
    Drop rows with no information apart from `finregistryid`

    Args:
        df (dataframe): SES dataframe

    Returns:
        SES dataframe with empty rows dropped
    """

    logging.info("Dropping empty rows")

    rows_before_dropping_empty = df.shape[0]
    persons_before_dropping_empty = df["finregistryid"].nunique()

    cols = list(df.columns[df.columns != "finregistryid"])
    df = df.dropna(subset=cols, how="all").reset_index(drop=True)

    rows_after_dropping_empty = df.shape[0]
    persons_after_dropping_empty = df["finregistryid"].nunique()
    diff_rows = rows_before_dropping_empty - rows_after_dropping_empty

    logging.info(f"{diff_rows:,} empty rows dropped")
    logging.info(f"{persons_before_dropping_empty:,} persons before dropping empty")
    logging.info(f"{persons_after_dropping_empty:,} persons after dropping empty")

    return df


def drop_duplicated_rows(df):
    """
    Drop duplicated rows.

    Args:
        df (dataframe): SES dataframe

    Returns:
        SES dataframe with duplicated rows dropped
    """
    logging.info("Dropping duplicates")

    rows_before_dropping_duplicates = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after_dropping_duplicates = df.shape[0]
    diff = rows_before_dropping_duplicates - rows_after_dropping_duplicates
    logging.info(f"{diff:,} rows dropped as duplicates")

    return df


if __name__ == "__main__":
    # Read data
    dfs = read_data(SF_SES_DATA_PATHS)

    # Preprocessing
    df = merge_data(dfs)
    df = drop_empty_rows(df)
    df = drop_duplicated_rows(df)

    # Write data to file
    write_data(df, SF_SOCIOECONOMIC_OUTPUT_DIR, "ses", "csv")
    write_data(df, SF_SOCIOECONOMIC_OUTPUT_DIR, "ses", "feather")
