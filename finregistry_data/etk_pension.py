"""
ETK Pension data preprocessing

Reads ETK Pension data, applies the preprocessing steps below and writes the result to a file.
- Set column names to lowercase 
- Parse dates
- Set data types (feather)
- drop redundant columns

Input files: 
- etk_elake1990_2021.csv.finreg_IDs
- etk_palkaton2005_2021.csv.finreg_IDs
- etk_vuansiot2005_2021.csv.finreg_IDs

Output files: 
- elake.csv, elake.feather
- palkaton.csv, palkaton.feather
- vuansiot.csv, vuansiot.feather
"""

import pandas as pd
import logging

from finregistry_data.config import (
    ETK_PENSION_ELAKE_DATA_PATH,
    ETK_PENSION_PALKATON_DATA_PATH,
    ETK_PENSION_VUANSIOT_DATA_PATH,
    ETK_PENSION_OUTPUT_DIR,
)
from finregistry_data.utils import write_data


def read_data(
    elake_path=ETK_PENSION_ELAKE_DATA_PATH,
    palkaton_path=ETK_PENSION_PALKATON_DATA_PATH,
    vuansiot_path=ETK_PENSION_VUANSIOT_DATA_PATH,
):
    """
    Read the three datasets into Pandas DataFrames.
    
    Numeric categorical variables are read as strings.
    Column names are set to lowercase.

    Args:
        elake_path (str): File path to elake dataset
        palkaton_path (str): File path to palkaton dataset
        vuansiot_path (str): File path to vuansiot dataset

    Returns: 
        (elake, palkaton, vuansiot): tuple of DataFrames.
    """
    elake = pd.read_csv(
        elake_path, sep=";", dtype={"psyy": str, "dryhma1": str, "dryhma2": str}
    )
    logging.info(f"Elake dataset loaded: {elake.shape[0]:,} rows")

    palkaton = pd.read_csv(palkaton_path, sep=";", dtype={"etuuslaji": str})
    logging.info(f"Palkaton dataset loaded: {palkaton.shape[0]:,} rows")

    vuansiot = pd.read_csv(vuansiot_path)
    logging.info(f"Vuansiot dataset loaded: {vuansiot.shape[0]:,} rows")

    return (elake, palkaton, vuansiot)


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
        lambda x: pd.to_datetime(x, format="%d/%m/%Y", errors="coerce").dt.date
    )
    return df


if __name__ == "__main__":

    elake, palkaton, vuansiot = read_data()

    elake = parse_dates(elake, ["aalk", "apvm", "ppvm"])
    write_data(elake, ETK_PENSION_OUTPUT_DIR, "elake", "csv")
    write_data(elake, ETK_PENSION_OUTPUT_DIR, "elake", "feather")

    palkaton = parse_dates(palkaton, ["alkamispvm", "paattymispvm"])
    write_data(palkaton, ETK_PENSION_OUTPUT_DIR, "palkaton", "csv")
    write_data(palkaton, ETK_PENSION_OUTPUT_DIR, "palkaton", "feather")

    vuansiot.columns = vuansiot.columns.str.lower()
    vuansiot = vuansiot.drop(columns="he00hsur")
    write_data(vuansiot, ETK_PENSION_OUTPUT_DIR, "vuansiot", "csv")
    write_data(vuansiot, ETK_PENSION_OUTPUT_DIR, "vuansiot", "feather")
