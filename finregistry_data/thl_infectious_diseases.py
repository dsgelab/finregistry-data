import pandas as pd
from config import THL_INFECTIOUS_DISEASES_DATA_PATH

MISSING_VALUES = [0]
MISSING_VALUES_STR = [str(i) for i in MISSING_VALUES]


def read_data(filepath=THL_INFECTIOUS_DISEASES_DATA_PATH):
    """Read infectious diseases data"""
    dtypes = {
        "TAPAUS_ID": int,
        "TNRO": str,
        "KOODIN_TNS": int,
        "KUVAUS": str,
        "ARVO_KOODI": float,
        "ARVO_TEKSTI": str,
    }
    df = pd.read_csv(filepath, sep=";", encoding="latin9", dtype=dtypes,)
    return df


def replace_missing_with_na(df):
    """Replace missing vaues with NA"""
    d = {"ARVO_KOODI": MISSING_VALUES, "ARVO_TEKSTI": MISSING_VALUES_STR}
    df = df.replace(d, pd.NA)
    return df

