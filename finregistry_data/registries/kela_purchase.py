"""
Kela Purchase data preprocessing

Reads Kela Purchase data, applies the preprocessing steps below and writes the result to files split by year.
- Convert column names to uppercase
- Rename HETU to FINREGISTRYID
- Format dates to YYYY-MM-DD
- Drop duplicates rows
- Fix data types

Input files: 
- For years 1995-2019 (split by year): 175_522_2020_LAAKEOSTOT_<year>.csv.finreg_IDs (25 files)
- For years 2020-2021 (split by month): 81_522_2022_LAAKEOSTOT_<year><month>.csv.finreg_IDs (24 files)

Output files: 
- purchase_<year>.csv (27 files)
- purchase_<year>.feather (27 files)
"""

import pandas as pd
import logging
from datetime import datetime

from finregistry_data.config import KELA_PURCHASE_INPUT_DIR, KELA_PURCHASE_OUTPUT_DIR
from finregistry_data.utils import write_data


def preprocess_purchases(path):
    """
    Preprocess Kela drug purchases input file

    Args:
        path (str): Path to the input file

    Returns:
        Preprocessed dataframe
    """
    df = pd.read_csv(path, sep=";", dtype=str)

    # Convert column names to uppercase
    df.columns = df.columns.str.upper()

    # Format dates
    for date_col in ["OSTOPV", "RKPV"]:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    # Rename HETU to FINREGISTRYID
    df = df.rename(columns={"HETU": "FINREGISTRYID"})

    # Drop duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Fix data types
    dtypes = {
        "PLKM": float,
        "KUST_EUR": float,
        "KORV_EUR": float,
        "KAKORV_EUR": float,
    }
    df = df.astype(dtypes)

    return df


def convert_csv_to_feather(path, output_name):
    """
    Convert a preprocessed KELA Purchases file into a feather file

    Args:
        path (str): path to the preprocessed file
        output_name (str): name of the output file without the file extension
    """
    dtypes = {
        "FINREGISTRYID": str,
        "ATC": str,
        "PLKM": float,
        "KUST_EUR": float,
        "KORV_EUR": float,
        "KAKORV_EUR": float,
        "RPK": str,
        "LAJI": str,
        "VNRO": str,
        "SAIR": str,
        "RGTNO": str,
        "ASKU": str,
        "SHP_NRO": str,
        "TILASTOVUOSI": str,
        "ANJA": str,
    }
    date_cols = ["OSTOPV", "RKPV"]
    df = pd.read_csv(path, dtype=dtypes, parse_dates=date_cols)
    write_data(df, KELA_PURCHASE_OUTPUT_DIR, output_name, "feather")


if __name__ == "__main__":
    # Set logging level to INFO
    logging.basicConfig(level=logging.INFO)

    # Loop through files split by year
    for year in range(1995, 2020):
        filename = "175_522_2020_LAAKEOSTOT_" + str(year) + ".csv.finreg_IDs"
        input_path = KELA_PURCHASE_INPUT_DIR / filename
        logging.info("Processing file " + filename)
        df = preprocess_purchases(input_path)
        write_data(df, KELA_PURCHASE_OUTPUT_DIR, "purchases_" + str(year), "csv")
        write_data(df, KELA_PURCHASE_OUTPUT_DIR, "purchases_" + str(year), "feather")

    # Loop through files split by month
    today = datetime.today().strftime("%Y-%m-%d")
    for year in range(2020, 2022):
        for month in range(1, 12):
            filename = (
                "81_522_2022_LAAKEOSTOT_"
                + str(year)
                + str(month).zfill(2)
                + ".csv.finreg_IDs"
            )
            input_path = KELA_PURCHASE_INPUT_DIR / filename
            logging.info("Processing file " + filename)
            df = preprocess_purchases(input_path)
            header = True if month == 1 else False
            output_path = KELA_PURCHASE_OUTPUT_DIR / (
                "purchases_" + str(year) + "_" + today + ".csv"
            )
            df.to_csv(output_path, mode="a", header=header, index=False)
        convert_csv_to_feather(KELA_PURCHASE_OUTPUT_DIR, "purchases_" + str(year))
