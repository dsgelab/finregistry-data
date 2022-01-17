import pandas as pd
from config import THL_INFECTIOUS_DISEASES_DATA_PATH


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

