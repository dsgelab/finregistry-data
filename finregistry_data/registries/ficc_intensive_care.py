"""
FICC Intensive Care data preprocessing

Reads FICC Intensive Care data, applies the preprocessing steps below and writes the result to a file.
- parse dates
- drop redundant columns 
- TODO: parse missing and invalid values (probably 0 and/or 99)
- TODO: reshape TISS from long to wide format
- TODO: replace GROUP_SEX with FEMALE

Input files: 
- thl2020_2196_teho.csv.finreg_IDs
- thl2020_2196_teho_tiss.csv.finreg_IDs

Output files: 
- intensive_care.csv
- tiss.csv
"""

import pandas as pd
from finregistry_data.utils import write_data
from finregistry_data.config import (
    FICC_INTENSIVE_CARE_TEHO_DATA_PATH,
    FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH,
    FICC_INTENSIVE_CARE_OUTPUT_DIR,
)


def read_data(filepath):
    """Read data from file"""
    df = pd.read_csv(filepath, sep=";")
    return df


def parse_dates(df, date_cols):
    """Parse dates as pandas dates. Invalid dates are returned as NaT."""
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], format="%d.%m.%Y", errors="coerce")
        df[date_col] = df[date_col].dt.date        
    return df
    

def drop_columns(df):
    """Drop columns that are not needed from the Teho dataset"""
    drop = ["YEAR", "HOSP_ADM_TIME"]
    df = df.drop(columns=drop)
    return df


def preprocess_teho_data(df):
    """Preprocess Teho dataset"""
    df = parse_dates(df, ["HOSP_DISCH_TIME", "ADM_TIME", "DISCH_TIME"])
    df = drop_columns(df)
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    return df


def preprocess_tiss_data(df):
    """Preprocess TISS dataset"""
    df = parse_dates(df, ["DATETIME"])
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    return df


if __name__ == "__main__":
    teho = read_data(FICC_INTENSIVE_CARE_TEHO_DATA_PATH)
    tiss = read_data(FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH)
    
    teho = preprocess_teho_data(teho)
    tiss = preprocess_tiss_data(tiss)
    
    write_data(teho, FICC_INTENSIVE_CARE_OUTPUT_DIR, "intensive_care", "csv")
    write_data(tiss, FICC_INTENSIVE_CARE_OUTPUT_DIR, "tiss", "csv")
