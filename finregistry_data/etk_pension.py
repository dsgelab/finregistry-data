"""
ETK Pension data preprocessing

Reads ETK Pension data, applies the preprocessing steps below and writes the result to a file.
- Set column names to lowercase 
- Parse dates
- Set data types (feather)
- drop redundant columns
- transform income from cents to euros
- add indexed income to `vuansiot`

Input files: 
- etk_elake1990_2021.csv.finreg_IDs
- etk_palkaton2005_2021.csv.finreg_IDs
- etk_vuansiot2005_2021.csv.finreg_IDs
- consumer_price_index_1972_2021.csv

Output files: 
- elake.csv, elake.feather
- palkaton.csv, palkaton.feather
- vuansiot.csv, vuansiot.feather
"""

from multiprocessing.sharedctypes import Value
import pandas as pd
import logging

from finregistry_data.config import (
    ETK_PENSION_CPI_DATA_PATH,
    ETK_PENSION_ELAKE_DATA_PATH,
    ETK_PENSION_PALKATON_DATA_PATH,
    ETK_PENSION_VUANSIOT_DATA_PATH,
    ETK_PENSION_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

CENTS_IN_EURO = 100.0

logging.basicConfig(level=logging.INFO)


def read_data(
    elake_path=ETK_PENSION_ELAKE_DATA_PATH,
    palkaton_path=ETK_PENSION_PALKATON_DATA_PATH,
    vuansiot_path=ETK_PENSION_VUANSIOT_DATA_PATH,
    cpi_path=ETK_PENSION_CPI_DATA_PATH
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

    cpi = pd.read_csv(cpi_path)
    logging.info(f"CPI dataset loaded: {cpi.shape[0]:,} rows")

    return (elake, palkaton, vuansiot, cpi)


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

def add_indexed_value(df, value_col, year_col, cpi):
    """
    Add indexed value as a new column to `df`.

    Args: 
        df (DataFrame): dataset for adding the indexed value
        value_col (str): name of the column with values in df
        year_col (str): name of the column with years in df
        cpi (DataFrame): Consumer Price Index dataset. Must include all years in df[col].

    Returns:
        df (DataFrame): dataset with a column for the indexed value

    Raises:
        ValueError: if cpi does not include all years in df[col]
    """
    if set(df[year_col]) - set(cpi["year"]) != set():
        raise ValueError("All years in df are not covered in CPI")

    df = df.merge(cpi, left_on=year_col, right_on="year", how="left")
    df[value_col + "_indexed"] = df[value_col] * df["cpi"]
    df = df.drop(columns={"cpi", "year"})

    return df


if __name__ == "__main__":

    elake, palkaton, vuansiot, cpi = read_data()

    elake = parse_dates(elake, ["aalk", "apvm", "ppvm"])
    
    logging.info("Writing elake dataset to a file")
    write_data(elake, ETK_PENSION_OUTPUT_DIR, "elake", "csv")
    write_data(elake, ETK_PENSION_OUTPUT_DIR, "elake", "feather")

    palkaton = parse_dates(palkaton, ["alkamispvm", "paattymispvm"])
    
    logging.info("Writing palkaton dataset to a file")
    write_data(palkaton, ETK_PENSION_OUTPUT_DIR, "palkaton", "csv")
    write_data(palkaton, ETK_PENSION_OUTPUT_DIR, "palkaton", "feather")

    vuansiot.columns = vuansiot.columns.str.lower()
    vuansiot = vuansiot.drop(columns="he00hsur")
    vuansiot["vuosiansio"] = vuansiot["vuosiansio"] / CENTS_IN_EURO
    vuansiot = add_indexed_value(vuansiot, "vuosiansio", "vuosi", cpi)
    
    logging.info("Writing vuansiot dataset to a file")
    write_data(vuansiot, ETK_PENSION_OUTPUT_DIR, "vuansiot", "csv")
    write_data(vuansiot, ETK_PENSION_OUTPUT_DIR, "vuansiot", "feather")
