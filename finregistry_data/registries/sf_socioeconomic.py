"""
SF Socioeconomics preprocessing

Reads SF Education, Occupation and Socioeconomics data, applies the preprocessing steps below and writes the result to files.
- Harmonize column names
- Remove rows with no information apart from `finregistryid`
- Drop duplicated rows
- Merge files into a single dataset

Input files: 
- tutkinto_u1442_a.csv.finreg_IDs
- tutkinto_u1442_al10_osa1.csv.finreg_IDs
- tutkinto_u1442_al10_osa2.csv.finreg_IDs
- ammatti_u1442_a.csv.finreg_IDs
- ammatti_u1442_al10.csv.finreg_IDs
- sose_u1442_a.csv.finreg_IDs
- sose_u1442_al10.csv.finreg_IDs

Output files: 
- socioeconomics_<YYYY-MM-DD>.csv
- socioeconomics_<YYYY-MM-DD>.feather
"""


from finregistry_data.config import (
    SF_EDUCATION_DATA_PATHS,
    SF_OCCUPATION_DATA_PATHS,
    SF_SES_DATA_PATHS,
    SF_SOCIOECONOMIC_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

import pandas as pd
import logging

from csv import Sniffer
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def read_data(paths, dtypes={}, rename_dict={}):
    """
    Read data

    Args:
        paths (list of str): paths to input data files
        dtypes (dict): data types for each column
        rename_dict (dict): rename columns

    Returns:
        A dataframe
    """
    # Read data
    dfs = []
    for path in tqdm(paths, desc="Importing data"):

        # Find delimiter in the file
        with open(path, "r", encoding="latin1") as f:
            dialect = Sniffer().sniff(f.readline())
            sep = dialect.delimiter

        # Read data
        df = pd.read_csv(path, sep=sep, encoding="latin1", dtype=dtypes)

        dfs.append(df)

    # Harmonize column names
    for i in range(len(dfs)):
        dfs[i] = dfs[i].rename(columns=rename_dict)
        dfs[i].columns = dfs[i].columns.str.upper()

    # Concatenate dataframes
    df = pd.concat(dfs, ignore_index=True)

    logging.info(f"{df.shape[0]:,} rows imported")

    return df


def drop_empty_rows(df):
    """
    Drop rows with no information apart from `FINREGISTRYID`

    Args:
        df (pd.DataFrame): dataframe

    Returns:
        A dataframe with empty rows dropped
    """
    n_before = df.shape[0]
    cols = [col for col in df.columns if col != "FINREGISTRYID"]
    df = df.dropna(subset=cols, how="all").reset_index(drop=True)
    n_after = df.shape[0]
    logging.info(
        f"Dropped {n_before - n_after:,} rows with no information apart from `FINREGISTRYID`"
    )

    return df


def drop_duplicated_rows(df):
    """
    Drop duplicated rows

    Args:
        df (pd.DataFrame): dataframe
    """
    n_before = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    n_after = df.shape[0]
    logging.info(f"Dropped {n_before - n_after:,} duplicated rows")

    return df


def preprocess_education(paths):
    """
    Preprocess education data
    """
    # Data types
    dtypes = {
        "FINREGISTRYID": str,
        "F1": str,
        "vuosi": float,
        "ututku": str,
        "iscfi2013": str,
        "kaste_t2": str,
        "snimi": str,
    }

    # Rename dictionary
    rename_dict = {"F1": "finregistryid"}

    # Read data
    df = read_data(paths, dtypes, rename_dict)

    # Drop rows with no information apart from `finregistryid`
    df = drop_empty_rows(df)

    # Drop duplicated rows
    df = drop_duplicated_rows(df)

    return df


def preprocess_occupation(paths):
    """
    Preprocess occupation data
    """
    # Data types
    dtypes = {
        "FINREGISTRYID": str,
        "F1": str,
        "vuosi": float,
        "pamko": str,
        "ammattikoodi": str,
    }

    # Rename dictionary
    rename_dict = {"F1": "finregistryid"}

    # Read data
    df = read_data(paths, dtypes, rename_dict)

    # Drop rows with no information apart from `finregistryid`
    df = drop_empty_rows(df)

    # Drop duplicated rows
    df = drop_duplicated_rows(df)

    return df


def preprocess_ses(paths):
    """
    Preprocess SES data

    Args:
        paths (list of str): paths to input data files
    """
    # Data types
    dtypes = {
        "FINREGISTRYID": str,
        "F1": str,
        "vuosi": float,
        "psose": str,
        "sose": str,
    }

    # Rename dictionary
    rename_dict = {"F1": "finregistryid"}

    # Read data
    df = read_data(paths, dtypes, rename_dict)

    # Drop rows with no information apart from `finregistryid`
    df = drop_empty_rows(df)

    # Drop duplicated rows
    df = drop_duplicated_rows(df)

    return df


def merge_data(dfs):
    """
    Merge data

    Args:
        dfs (list of pd.DataFrame): dataframes to merge
    """
    df = dfs[0]
    for df_ in dfs[1:]:
        df = pd.merge(df, df_, on=["FINREGISTRYID", "VUOSI"], how="outer")

    logging.info(f"{df.shape[0]:,} rows after merging data")
    logging.info(f"{df['FINREGISTRYID'].nunique():,} unique `FINREGISTRYID`")

    return df


if __name__ == "__main__":
    # Read data
    education = preprocess_education(SF_EDUCATION_DATA_PATHS)
    occupation = preprocess_occupation(SF_OCCUPATION_DATA_PATHS)
    ses = preprocess_ses(SF_SES_DATA_PATHS)

    # Merge data
    df = merge_data([education, occupation, ses])
    del education, occupation, ses

    # Write data
    write_data(df, SF_SOCIOECONOMIC_OUTPUT_DIR, "socioeconomics", "csv")
    write_data(df, SF_SOCIOECONOMIC_OUTPUT_DIR, "socioeconomics", "feather")
