"""
THL Malformations data processing 

Reads THL Malformations data, applies the preprocessing steps below, and writes the result to a file.
- remove extra linebreaks and quotations
- parse dates
- replace missing values with NA

Input files: 
- thl2020_2196_er_basic.csv.finreg_IDs
- thl2020_2196_er_anomalies.csv.finreg_IDs

Output files:
- malformations_basic_<YYYY-MM-DD>.csv
- malformations_anomaly_<YYYY-MM-DD>.csv
"""

import pandas as pd
import re
from finregistry_data.utils import write_data
from finregistry_data.config import (
    THL_MALFORMATIONS_OUTPUT_DIR,
    THL_MALFORMATIONS_BASIC_DATA_PATH,
    THL_MALFORMATIONS_ANOMALIES_DATA_PATH,
)

MISSING_VALUES = ["", "nan", "0.0", "00000", "000000"]


def join_multiline_rows(lines):
    """Join rows taking up multiple lines to a single line"""
    pattern = re.compile(r"^(FR\d*);([^;]*);([^;]*);([^;]*$)", re.S | re.M)
    data = pattern.findall(lines)
    return data


def read_anomaly_data(filepath=THL_MALFORMATIONS_ANOMALIES_DATA_PATH):
    """Read anomaly dataset"""
    with open(filepath) as f:
        lines = join_multiline_rows(f.read())
    df = pd.DataFrame(lines, columns=["TNRO", "DIAGNOSE", "ICD9", "ICD10"], dtype=str)
    return df


def read_basic_data(filepath=THL_MALFORMATIONS_BASIC_DATA_PATH):
    date_cols = ["DATE_OF_DEATH", "C_BIRTHDATE"]
    df = pd.read_csv(filepath, sep=";", parse_dates=date_cols)
    return df


def remove_extra_linebreaks(df):
    """Remove extra linebreaks from anomaly.DIAGNOSE and anomaly.ICD10"""
    df["DIAGNOSE"] = df["DIAGNOSE"].str.replace("\s+", " ", regex=True)
    df["ICD10"] = df["ICD10"].str.replace("\s+", "", regex=True)
    return df


def remove_extra_quotations(df):
    """Remove extra quotation marks from anomaly.DIAGNOSE"""
    df["DIAGNOSE"] = df["DIAGNOSE"].str.replace('"', "")
    return df


def replace_missing_with_na(df):
    """Replace missing vaues with NA"""
    df = df.replace(MISSING_VALUES, pd.NA)
    return df


def preprocess_basic_data(df):
    """Apply the preprocessing pipeline to basic data"""
    df = replace_missing_with_na(df)
    return df


def preprocess_anomaly_data(df):
    """Apply the preprocessing pipeline to anomaly data"""
    df = remove_extra_linebreaks(df)
    df = remove_extra_quotations(df)
    df = replace_missing_with_na(df)
    return df


if __name__ == "__main__":
    basic = read_basic_data()
    anomaly = read_anomaly_data()
    basic = preprocess_basic_data(basic)
    anomaly = preprocess_anomaly_data(anomaly)

    
    # change header to upper case
    basic.columns= basic.columns.str.upper()
    anomaly.columns= anomaly.columns.str.upper()
    # change TNRO to FINREGISTRYID
    basic = basic.rename(columns={"TNRO": "FINREGISTRYID"})
    anomaly = anomaly.rename(columns={"TNRO": "FINREGISTRYID"})
    
    write_data(basic, THL_MALFORMATIONS_OUTPUT_DIR, "malformations_basic", "csv")
    write_data(anomaly, THL_MALFORMATIONS_OUTPUT_DIR, "malformations_anomaly", "csv")
