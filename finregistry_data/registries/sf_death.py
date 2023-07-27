"""
SF Causes of Death preprocessing

Reads the data, applies the preprocessing steps below and writes the result to files.
- Merge corresponding files
- Drop duplicated rows 
- Reformat dates 
- TODO: Impute mid-year date (July 1st) for rows with only year available

The original data contains two types of files: tutkimus ("study") and vuosi ("year"). 
Only tutkimus files are preprocessed as tutkimus contains all information included
in vuosi, apart from some differences in variables for a small portion of FinRegistry IDs.

Input files: 
- thl2019_1776_ksyy_tutkimus.csv.finreg_IDs
- thl2021_2196_ksyy_tutkimus.csv.finreg_IDs
- (thl2019_1776_ksyy_vuosi.csv.finreg_IDs)
- (thl2021_2196_ksyy_vuosi.csv.finreg_IDs)

Output files: 
- death_<YYYY-MM-DD>.csv / .feather
"""

import pandas as pd
import logging

from finregistry_data.config import (
    SF_DEATH_TUTKIMUS_DATA_PATHS,
    SF_DEATH_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

logging.basicConfig(level=logging.INFO)


def read_data(paths):
    """
    Read causes of death data.

    Args:
        paths (list): List of file paths

    Returns:
        List of dataframes
    """
    dfs = []
    for path in paths:
        df = pd.read_csv(path, sep=";")
        dfs.append(df)
        logging.info(f"{path} read: {df.shape[0]:,} rows")
    return dfs


def merge_data(dfs):
    """
    Merge data. Duplicated rows are removed.

    Args:
        dfs (list): list of dataframes to be merged

    Returns:
        Merged dataframe
    """
    df = pd.concat(dfs, axis=0)
    n_before = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    n_duplicates = n_before - df.shape[0]
    logging.info(f"{n_duplicates:,} duplicated rows dropped")
    return df


def format_dates(df, date_cols):
    """
    Format dates to YYYY-MM-DD.

    Args:
        df (DataFrame): dataset
        date_cols (list): list of date column names

    Returns:
        Dataset with columns formatted
    """
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col]).dt.date
    return df


if __name__ == "__main__":
    # Read data
    logging.info("Reading data")
    dfs = read_data(SF_DEATH_TUTKIMUS_DATA_PATHS)

    # Merge data from different years
    logging.info("Merging data from different years")
    df = merge_data(dfs)

    # Format date columns
    logging.info("Formatting dates")
    df = format_dates(df, ["KPV"])

    # change TNRO to FINREGISTRYID
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    # Write the output to file
    logging.info("Writing data")
    write_data(df, SF_DEATH_OUTPUT_DIR, "death", "csv")
    write_data(df, SF_DEATH_OUTPUT_DIR, "death", "feather")

