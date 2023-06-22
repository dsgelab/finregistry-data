"""
THL Hilmo data preprocessing

Reads the data, applies the preprocessing steps below and writes the result to a file.
- Combine files into a single output by category
- Harmonize date formats
- TODO: combine everything to a single file, merging based on Hilmo ID
- TODO: remove duplicated rows
- TODO: rename TNRO to FINREGISTRYID

Input files: 
- THL2021_2196_HILMO_2019_2021.csv.finreg_IDs
- THL2021_2196_HILMO_DIAG.csv.finreg_IDs
- THL2021_2196_HILMO_HAITMP.csv.finreg_IDs
- THL2021_2196_HILMO_HHAITTA.csv.finreg_IDs
- THL2021_2196_HILMO_LAAKITYS.csv.finreg_IDs
- THL2021_2196_HILMO_PSYKLAAKE.csv.finreg_IDs
- THL2021_2196_HILMO_PSYKP.csv.finreg_IDs
- THL2021_2196_HILMO_PSYKPPAK.csv.finreg_IDs
- THL2021_2196_HILMO_SYP.csv.finreg_IDs
- THL2021_2196_HILMO_TEHOHOITO.csv.finreg_IDs
- THL2021_2196_HILMO_TOIMP.csv.finreg_IDs
- THL2021_2196_HILMO_TULOSYY.csv.finreg_IDs
- thl2019_1776_hilmo.csv.finreg_IDs
- thl2019_1776_hilmo_9495.csv.finreg_IDs
- thl2019_1776_hilmo_9495_psykp.csv.finreg_IDs
- thl2019_1776_hilmo_9495_syp.csv.finreg_IDs
- thl2019_1776_hilmo_diagnoosit_kaikki.csv.finreg_IDs
- thl2019_1776_hilmo_haitmp.csv.finreg_IDs
- thl2019_1776_hilmo_hhaitta.csv.finreg_IDs
- thl2019_1776_hilmo_laakkeet.csv.finreg_IDs
- thl2019_1776_hilmo_psykp.csv.finreg_IDs
- thl2019_1776_hilmo_psykplaake.csv.finreg_IDs
- thl2019_1776_hilmo_psykppak.csv.finreg_IDs
- thl2019_1776_hilmo_syp.csv.finreg_IDs
- thl2019_1776_hilmo_tehohoito.csv.finreg_IDs
- thl2019_1776_hilmo_toimenpide.csv.finreg_IDs
- thl2019_1776_hilmo_tusyy.csv.finreg_IDs
- thl2019_1776_poisto_6986.csv.finreg_IDs
- thl2019_1776_poisto_8793.csv.finreg_IDs

Output files: 
- hilmo.csv
- hilmo_diag.csv
- hilmo_haitmp.csv
- hilmo_hhaitta.csv
- hilmo_laakkeet.csv
- hilmo_psyklaake.csv
- hilmo_psykp.csv
- hilmo_syp.csv
- hilmo_tehohoito.csv
- hilmo_toimenpide.csv
- hilmo_tulosyy.csv
"""

import pandas as pd
from datetime import datetime
from tqdm import tqdm

from finregistry_data.config import (
    THL_HILMO_MAIN,
    THL_HILMO_DIAG,
    THL_HILMO_HAITMP,
    THL_HILMO_HHAITTA,
    THL_HILMO_LAAKKEET,
    THL_HILMO_PSYKLAAKE,
    THL_HILMO_PSYKP,
    THL_HILMO_PSYKPPAK,
    THL_HILMO_SYP,
    THL_HILMO_TEHOHOITO,
    THL_HILMO_TOIMENPIDE,
    THL_HILMO_TULOSYY,
    THL_HILMO_OUTPUT_DIR,
)


def preprocess_hilmo_main(file):
    """
    Preprocess THL Hilmo main file
    - Fix data types
    - Convert date formats
    - Insert missing columns as NA
    - TODO: harmonize column names, e.g. possibly LPVM-LOMAPVM, JONOPVM-JOPVM, LANTOKOTAR-LANTTAR, JATTAR-JATKOODTAR

    Notes:
    - LOMAPV != LOMAPVM
    """
    dtypes = {
        "HILMO_ID": int,
        "TNRO": str,
        "IKA": float,
        "PALTU": str,
        "PALTUTAR": str,
        "PALA": str,
        "KIIREELLISYYS": str,
        "YHTEYSTAPA": str,
        "EA": str,
        "KAVIJARY": str,
        "KOKU": str,
        "ASUINPAIKAN_POSTINUMERO": str,
        "ULASU": str,
        "SATAP": str,
        "TULI": str,
        "TUSYY1": str,
        "TUSYY2": str,
        "TUSYY3": str,
        "LPKOD": str,
        "LPKODTAR": str,
        "LANTKO": str,
        "LANTTAR": str,
        "LANTKOTAR": str,
        "PALSET": str,
        "OSTOPAL": str,
        "VALINNANVAPAUS": str,
        "EUMAASTA": str,
        "JONOSYY": str,
        "HOITOITU": str,
        "HOITOI": str,
        "NORDDRG": str,
        "TEHOTUN": str,
        "RISKEURKAKSI": str,
        "PSYKP": str,
        "LOMAPV": float,
        "JATKOH": str,
        "JATKOOD": str,
        "JATTAR": str,
        "JATKOODTAR": str,
        "KOKKUST": float,
        "PTMPK1": str,
        "PTMPK2": str,
        "PTMPK3": str,
        "MTMP1K1": str,
        "MTMP2K1": str,
        "TMP1": str,
        "TMP2": str,
        "TMP3": str,
        "TAPTYYP": str,
        "HHAITTA": str,
        "HAITYYP": str,
        "HAIDIAG": str,
        "HAIDIAG2": str,
        "HAITMP1": str,
        "HAITMP2": str,
        "HAITMPZS": str,
        "PDG": str,
        "SDG1": str,
        "SDG2": str,
        "ULKSYY": str,
    }

    date_cols = [
        "LPVM",
        "JONOPVM",
        "JOPVM",
        "LOMAPVM",
        "TUPVA",
        "LANTTUPVA",
        "LANTKASPVA",
    ]

    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # Parse dates
    # Note: times are omitted
    for date_col in (set(date_cols) & set(df.columns)):
        df[date_col] = pd.to_datetime(df[date_col]).dt.date

    # Insert missing columns as NAs
    all_cols = list(dtypes.keys()) + date_cols
    missing_cols = [col for col in all_cols if col not in df.columns]
    for col in missing_cols:
        df[col] = pd.NA
        
    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(all_cols)

    return df


def preprocess_hilmo_diag(file):
    """
    Preprocess THL Hilmo Diag
    - Fix data types
    - Convert date formats
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "KENTTA": str, "N": int, "KOODI": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_haitmp(file):
    """
    Preprocess THL Hilmo Haitmp
    - Fix data types
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "HAITMP": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_hhaitta(file):
    """
    Preprocess THL Hilmo HHAITTA
    - Fix data types
    - TODO: missing values ("-" in HHAITTA)
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "HHAITTA": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_laakkeet(file):
    """
    Preprocess THL Hilmo LAAKKEET
    - Fix data types
    - TODO: Covert date formats (keep only date)

    Note: the older Hilmo files includes datetimes and the newer one only dates
    """
    dtypes = {
        "HILMO_ID": int,
        "TNRO": str,
        "MAAR_PVM": str,
        "ATC": str,
        "ATCSELITE": str,
        "VNR": str,
        "KAUPPANIMI": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df["MAAR_PVM"] = pd.to_datetime(
        df["MAAR_PVM"].str[:9],
    ).dt.date

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_psyklaake(file):
    """
    Preprocess THL Hilmo PSYKLAAKE
    - Fix data types
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "TOTLAAKPSYK": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_psykp(file):
    """
    Preprocess THL Hilmo PSYKP
    - Fix data types
    - Insert missing columns as NAs
    """
    dtypes = {
        "HILMO_ID": int,
        "TNRO": str,
        "TUTAP": str,
        "TRKESTO": str,
        "SUUNNITHOITO": str,
        "ITSHOITO": str,
        "LAAKPSYK": str,
        "PAKPSYK": str,
        "TUGAS": str,
        "POGAS": str,
        "OMTAP": str,
        "ITSPSYK": str,
        "HOIKER": str,
        "LHOI": str,
        "PAKKTOI1": str,
        "PAKKTOI2": str,
        "PAKKTOI3": str,
        "PAKKTOI4": str,
    }

    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # Insert missing columns as NAs
    all_cols = list(dtypes.keys())
    missing_cols = [col for col in all_cols if col not in df.columns]
    for col in missing_cols:
        df[col] = pd.NA
        
    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())

    return df


def preprocess_hilmo_psykppak(file):
    """
    Preprocess THL Hilmo PSYKPPAK
    - Fix data types
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "TOTPAKPSYK": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_syp(file):
    """
    Preprocess THL Hilmo syp
    - Fix data types
    """
    dtypes = {
        "HILMO_ID": int,
        "TNRO": str,
        "TMPTYP": str,
        "TMPTYP1": str,
        "TMPTYP2": str,
        "TMPTYP3": str,
        "TMPTYPTAR": str,
        "TMPLAJ": str,
        "NYHA": str,
        "RISKPI": str,
        "TYTILE": str,
        "TYSTAT": str,
        "TMPPRI": str,
        "TMPC1": str,
        "TMPC2": str,
        "TMPC3": str,
        "TMPC4": str,
        "TMPC5": str,
        "TMPC6": str,
        "TMPC7": str,
        "TMPC8": str,
        "TMPC9": str,
        "TMPC10": str,
        "TMPC11": str,
        "TMPLAJC": str,
        "TMPKIIR": str,
        "NYHAC": str,
        "RISKIEUR": str,
        "RISKEURL": str,
        "KOMPL1": str,
        "KOMPL2": str,
        "KOMPL3": str,
        "KOMPL4": str,
        "KOMPL5": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_hilmo_tehohoito(file):
    """
    Preprocess THL Hilmo Tehohoito
    - Fix data types
    - Convert date formats
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "TEHOTYYPPI": str}
    date_cols = ["TEHOALKUPVM", "TEHOLOPPUPVM"]
    df = pd.read_csv(
        file, sep=";", dtype=dtypes, parse_dates=date_cols, encoding="latin-1"
    )
    
    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == (len(dtypes.keys()) + len(date_cols))
    return df


def preprocess_hilmo_toimenpide(file):
    """
    Preprocess THL Hilmo Toimenpide
    - Fix data types
    - Convert date formats
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "N": int, "TOIMP": str}
    date_cols = ["TOIMPALKUPVM", "TOIMPLOPPUPVM"]
    df = pd.read_csv(
        file, sep=";", dtype=dtypes, parse_dates=date_cols, encoding="latin-1"
    )
    
    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == (len(dtypes.keys()) + len(date_cols))
    return df


def preprocess_hilmo_tusyy(file):
    """
    Preprocess THL Hilmo Tusyy
    - Fix data types
    """
    dtypes = {"HILMO_ID": int, "TNRO": str, "TUSYY": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")

    # jcd comment - quick fix, but not rerun yet
    # df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocessing_loop(files, func, output_filename):
    """
    Preprocess files in a loop. The output is appended.

    Args:
        files (list): list of files to preprocess
        func (function): preprocessing function to use
        output_filename (str): name of the output file without the file extension
    """
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = THL_HILMO_OUTPUT_DIR / (output_filename + "_" + today + ".csv")

    for file in tqdm(files):
        header = True if file == files[0] else False
        func(file).to_csv(output_path, mode="a", index=False, header=header)


if __name__ == "__main__":
    # Preprocessing all the files by category
    preprocessing_loop(THL_HILMO_MAIN, preprocess_hilmo_main, "hilmo")
    preprocessing_loop(THL_HILMO_DIAG, preprocess_hilmo_diag, "hilmo_diag")
    preprocessing_loop(THL_HILMO_HAITMP, preprocess_hilmo_haitmp, "hilmo_haitmp")
    preprocessing_loop(THL_HILMO_HHAITTA, preprocess_hilmo_hhaitta, "hilmo_hhaitta")
    preprocessing_loop(THL_HILMO_LAAKKEET, preprocess_hilmo_laakkeet, "hilmo_laakkeet")
    preprocessing_loop(
        THL_HILMO_PSYKLAAKE, preprocess_hilmo_psyklaake, "hilmo_psyklaake"
    )
    preprocessing_loop(THL_HILMO_PSYKP, preprocess_hilmo_psykp, "hilmo_psykp")
    preprocessing_loop(THL_HILMO_PSYKPPAK, preprocess_hilmo_psykppak, "hilmo_psykppak")
    preprocessing_loop(THL_HILMO_SYP, preprocess_hilmo_syp, "hilmo_syp")
    preprocessing_loop(
        THL_HILMO_TEHOHOITO, preprocess_hilmo_tehohoito, "hilmo_tehohoito"
    )
    preprocessing_loop(
        THL_HILMO_TOIMENPIDE, preprocess_hilmo_toimenpide, "hilmo_toimenpide"
    )
    preprocessing_loop(THL_HILMO_TULOSYY, preprocess_hilmo_tusyy, "hilmo_tulosyy")
