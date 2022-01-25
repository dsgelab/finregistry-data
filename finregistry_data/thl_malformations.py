"""
THL Malformations data processing 

Reads THL Malformations data, applies the preprocessing steps below, and writes the result to a file.
- remove extra linebreaks
- parse dates
- replace missing values with NA

Input files: 
- thl2020_2196_er_basic.csv.finreg_IDs
- thl2020_2196_er_anomalies.csv.finreg_IDs

Output files:
- malformations_<YYYY-MM-DD>.csv
- malformations_<YYYY-MM-DD>.feather
"""

import pandas as pd
import re
from finregistry_data.config import (
    THL_MALFORMATIONS_BASIC_DATA_PATH,
    THL_MALFORMATIONS_ANOMALIES_DATA_PATH,
)

MISSING_VALUES = [""]


def join_multiline_rows(lines):
    """Join rows taking up multiple lines to a single line"""
    pattern = re.compile(r"^(FR\d*);([^;]*);([^;]*);([^;]*$)", re.S | re.M)
    data = pattern.findall(lines)
    return data


def read_anomaly_data(filepath=THL_MALFORMATIONS_ANOMALIES_DATA_PATH):
    """Read anomaly dataset"""
    with open(filepath) as f:
        lines = join_multiline_rows(f.read())
    df = pd.DataFrame(lines, columns=["TNRO", "DIAGNOSE", "ICD9", "ICD10"])
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
