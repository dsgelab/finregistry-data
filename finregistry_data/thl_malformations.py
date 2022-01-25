"""
THL Malformations data processing 

Reads THL Malformations data, applies the preprocessing steps below, and writes the result to a file.
- TODO: remove extra linebreaks
- TODO: parse dates
- TODO: replace missing values with NA 
- TODO: drop redundant columns

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
