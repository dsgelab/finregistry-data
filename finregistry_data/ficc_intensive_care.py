"""
FICC Intensive Care data preprocessing

Reads FICC Intensive Care data, applies the preprocessing steps below and writes the result to a file.
- TODO: parse dates
- TODO: parse missing values 
- TODO: reshape TISS from long to wide format
- TODO: drop redundant columns 

Input files: 
- thl2020_2196_teho.csv.finreg_IDs
- thl2020_2196_teho_tiss.csv.finreg_IDs

Output files: 
- intensive_care.csv
- tiss.csv
"""

import pandas as pd
from config import (
    FICC_INTENSIVE_CARE_TEHO_DATA_PATH,
    FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH,
)


def read_data(filepath):
    """Read data from file"""
    df = pd.read_csv(filepath, sep=";")
    return df


def preprocess_data():
    teho = read_data(FICC_INTENSIVE_CARE_TEHO_DATA_PATH)
    tiss = read_data(FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH)

