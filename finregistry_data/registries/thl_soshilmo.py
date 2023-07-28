"""
THL Social Hilmo data processing 

Reads THL Social Hilmo data, applies the preprocessing steps below, and writes the result to a file.
- Fix data types 
- Parse dates
- Rename TNRO to FINREGISTRYID

Input files: 
- "thl2019_1776_soshilmo.csv.finreg_IDs"

Output files:
- soshilmo_<YYYY-MM-DD>.csv
- soshilmo_<YYYY-MM-DD>.feather
"""

import pandas as pd

from finregistry_data.config import THL_SOSHILMO_DATA_PATH, THL_SOSHILMO_OUTPUT_DIR
from finregistry_data.utils import write_data

def preprocess_soshilmo(file): 
    """Preprocess THL Social Hilmo file"""
    dtypes = {
        "TNRO": str,
        "VUOSI": int,
        "ILAJI": str,
        "PALTU": str,
        "PALTUTAR": str,
        "KOKU": str,
        "PALA": str,
        "VVAL": str,
        "ASUINPAIKAN_POSTINUMERO": str,
        "VAKASUM": str,
        "TUPVA": str,
        "TULI": str,
        "LPKOD": str,
        "LPKODTAR": str,
        "TUSYY1": str,
        "TUSYY2": str,
        "TUSYY3": str,
        "HOITOITU": str,
        "PDGO": str,
        "PDGE": str,
        "SDG1O": str,
        "SDG1E": str,
        "SDG2O": str,
        "SDG2E": str,
        "PDG": str,
        "SDG1": str,
        "HOITOI": str,
        "PITK": str,
        "LOMAPVM": str,
        "LPVM": str,
        "JATKOH": str,
        "ASMK": str,
        "KUNTMK": str,
        "MUUMMK": str,
        "MAPER": str,
        "HINTA": float, 
        "SYNTV": int,
        "IKA": float, 
        "IKAT": float, 
        "IKAPT": float,
        "SUKUP": str,
        "HOITOPV": float, 
        "KVHP": float,
        "IKA_VVLOPUSSA": float,
        "TYYPPI": str
    }

    df = pd.read_csv(file, sep=";", encoding="latin-1", dtype=dtypes)

    # Parse dates
    date_cols = ["TUPVA", "LPVM"]
    for date_col in date_cols: 
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    # Rename TNRO to FINREGISTRYID
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})

    return df

if __name__ == "__main__": 
    df = preprocess_soshilmo(THL_SOSHILMO_DATA_PATH)
    write_data(df, THL_SOSHILMO_OUTPUT_DIR, "soshilmo", "csv")
    write_data(df, THL_SOSHILMO_OUTPUT_DIR, "soshilmo", "feather")