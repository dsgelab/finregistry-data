"""
THL Avohilmo data preprocessing

Reads the data, applies the preprocessing steps below and writes the result to a file.
- Combine files into a single output by category
- Harmonize date formats
- Fix column order 
- Rename TNRO to FINREGISTRYID
- TODO: combine everything to a single file, merging based on Avohilmo ID
- TODO: remove duplicated rows
- TODO: rename TNRO to FINREGISTRYID

Input files: 
- THL2021_2196_AVOHILMO_2020.csv.finreg_IDs
- THL2021_2196_AVOHILMO_2021.csv.finreg_IDs
- THL2021_2196_AVOHILMO_ICD10_DIAG.csv.finreg_IDs
- THL2021_2196_AVOHILMO_ICPC2_DIAG.csv.finreg_IDs
- THL2021_2196_AVOHILMO_JATKOH.csv.finreg_IDs
- THL2021_2196_AVOHILMO_KOTIHOITO.csv.finreg_IDs
- THL2021_2196_AVOHILMO_LAAKE.csv.finreg_IDs
- THL2021_2196_AVOHILMO_LAHETE.csv.finreg_IDs
- THL2021_2196_AVOHILMO_ROKOSUOJA.csv.finreg_IDs
- THL2021_2196_AVOHILMO_ROKOTUS.csv.finreg_IDs
- THL2021_2196_AVOHILMO_TOIMP.csv.finreg_IDs
- thl2019_1776_avohilmo_11_12.csv.finreg_IDs
- thl2019_1776_avohilmo_13_14.csv.finreg_IDs
- thl2019_1776_avohilmo_15_16.csv.finreg_IDs
- thl2019_1776_avohilmo_17_18.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_icd10.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_icpc2.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_jatkoh.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_kotihoito.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_laake.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_lahete.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_rokotus.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_rokotussuoja.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_suu_toimp.csv.finreg_IDs
- thl2019_1776_avohilmo_17_20_toimenpide.csv.finreg_IDs
- thl2019_1776_avohilmo_19_20.csv.finreg_IDs
- thl2019_1776_avohilmo_icd10.csv.finreg_IDs
- thl2019_1776_avohilmo_icpc2.csv.finreg_IDs
- thl2019_1776_avohilmo_jatkohoito.csv.finreg_IDs
- thl2019_1776_avohilmo_kotihoito.csv.finreg_IDs
- thl2019_1776_avohilmo_laake.csv.finreg_IDs
- thl2019_1776_avohilmo_lahete.csv.finreg_IDs
- thl2019_1776_avohilmo_rokotus.csv.finreg_IDs
- thl2019_1776_avohilmo_rokotussuoja.csv.finreg_IDs
- thl2019_1776_avohilmo_suu_toimenpide.csv.finreg_IDs
- thl2019_1776_avohilmo_toimenpide.csv.finreg_IDs
- thl2021_2196_avohilmo_suu_toimp.csv.finreg_IDs

Output files: 
- avohilmo.csv
- avohilmo_icd10.csv
- avohilmo_icpc2.csv
- avohilmo_jatkohoito.csv
- avohilmo_kotihoito.csv
- avohilmo_laake.csv
- avohilmo_lahete.csv
- avohilmo_rokosuoja.csv
- avohilmo_rokotus.csv
- avohilmo_toimenpide.csv
- avohilmo_suu_toimenpide.csv
"""

import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

from finregistry_data.config import (
    THL_AVOHILMO_MAIN,
    THL_AVOHILMO_ICD10,
    THL_AVOHILMO_ICPC2,
    THL_AVOHILMO_JATKOHOITO,
    THL_AVOHILMO_KOTIHOITO,
    THL_AVOHILMO_LAAKE,
    THL_AVOHILMO_LAHETE,
    THL_AVOHILMO_ROKOSUOJA,
    THL_AVOHILMO_ROKOTUS,
    THL_AVOHILMO_TOIMENPIDE,
    THL_AVOHILMO_SUU_TOIMENPIDE,
    THL_AVOHILMO_OUTPUT_DIR,
)


def preprocess_avohilmo_main(file, output_path):
    """
    Preprocess the AvoHilmo main file in chunks and write to a file.
    - Fix data types
    - Parse dates
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "ASIAKAS_KOTIKUNTA": str,
        "ASIAKAS_POSTINUMERO": str,
        "ASIAKAS_KOTIMAA": str,
        "PALVELUNTUOTTAJA": str,
        "PALVELUNTUOTTAJA_YKSIKKO": str,
        "HTA_AMMATTIOIKEUS": str,
        "HTA_AMMATTI": str,
        "HTA_ENSIKAYNTI": str,
        "HTA_KIIREELLISYYS": str,
        "HTA_LUONNE": str,
        "HTA_TULOS": str,
        "AJANVARAUS_AMMATTIOIKEUS": str,
        "AJANVARAUS_AMMATTI": str,
        "AJANVARAUS_PALVELUMUOTO": str,
        "AJANVARAUS_YHTEYSTAPA": str,
        "KAYNTI_KAVIJARYHMA": str,
        "KAYNTI_KIIREELLISYYS": str,
        "KAYNTI_LUONNE": str,
        "KAYNTI_ENSIKAYNTI": str,
        "KAYNTI_ERIKOISALA": str,
        "KAYNTI_AMMATTIOIKEUS": str,
        "KAYNTI_AMMATTI": str,
        "KAYNTI_PALVELUMUOTO": str,
        "KAYNTI_YHTEYSTAPA": str,
        "ULKOINEN_SYY": str,
        "TAPATURMATYYPPI": str,
        "PAINO": float,
        "PAINO_YKSIKKO": str,
        "PITUUS": float,
        "EPDS": str,
        "VYOTARO_YMPARYS": float,
        "DIASTOLINEN_VERENPAINE": float,
        "SYSTOLINEN_VERENPAINE": float,
        "HH_PYSYVA_KARIOITUNEET": str,
        "HH_PYSYVA_PUUTTUVAT": str,
        "HH_PYSYVA_PAIKATUT": str,
        "HH_MAITO_KARIOITUNEET": str,
        "HH_MAITO_PUUTTUVAT": str,
        "HH_MAITO_PAIKATUT": str,
        "HH_PYSYVA_DMFS": str,
        "HH_OIKOMISTARVE": str,
        "HH_HARJAUSKERTA_LKM": str,
        "TUPAKOINTI": str,
        "AUDIT_FULL": str,
        "AUDIT_C": str,
        "RASKAUS_PARITEETTI": str,
        "RASKAUS_RASKAUSVIIKOT": str,
        "KOTIHOITO_PALVELUSUUNNITELMA": str,
    }
    date_cols = [
        "SEURANTATIETUE_PAIVITETTY",
        "YHTEYDENOTTO_AJANKOHTA",
        "HOIDONTARVE_AJANKOHTA",
        "AJANVARAUS_AJANKOHTA",
        "AJANVARAUS_VARATTU",
        "KOTIHOITO_TARKISTUS_AJANKOHTA",
        "PERUUTUS_AJANKOHTA",
        "RASKAUS_LASKETTUAIKA",
        "KAYNTI_ALKOI",
        "KAYNTI_LOPPUI",
    ]
    
    header = pd.DataFrame(columns=(list(dtypes.keys()) + date_cols))

    # Write header if file does not exist
    if not os.path.isfile(output_path):
        header = pd.DataFrame(columns=(list(dtypes.keys()) + date_cols))
        header = header.rename(columns={"TNRO": "FINREGISTRYID"})
        header.to_csv(output_path, index=False)

    # Write content in chunks
    # TODO: rename TNRO to FINREGISTRYID
    chunksize = 10**5
    with pd.read_csv(
        file,
        chunksize=chunksize,
        sep=";",
        encoding="latin-1",
        dtype=dtypes,
        parse_dates=date_cols
    ) as reader:
        for chunk in tqdm(reader):
            assert chunk.shape[1] == (len(dtypes.keys()) + len(date_cols))
            chunk[header.columns].to_csv(output_path, mode="a", index=False, header=False)


def preprocess_avohilmo_icd10(file):
    """
    Preprocess THL Avohilmo ICD10
    - Fix data types
    - Fix column order
    """
    dtypes = {"AVOHILMO_ID": int, "TNRO": str, "JARJESTYS": int, "ICD10": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_icpc2(file):
    """
    Preprocess THL Avohilmo ICDPC2
    - Fix data types
    - Fix column order
    """
    dtypes = {"AVOHILMO_ID": int, "TNRO": str, "JARJESTYS": int, "ICPC2": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_jatkohoito(file):
    """
    Preprocess THL Avohilmo Jatkohoito (follow-up care)
    - Fix data types
    - Fix column order
    """
    dtypes = {"AVOHILMO_ID": int, "TNRO": str, "JARJESTYS": int, "TOIMENPIDE": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_kotihoito(file):
    """
    Preprocess THL Avohilmo Kotihoito (home care)
    - Fix data types
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "ATERIAPALVELU": str,
        "KULJETUSPALVELU": str,
        "SIIVOUSPALVELU": str,
        "SAATTAJAPALVELU": str,
        "TURVAPALVELU": str,
        "KAUPPAPALVELU": str,
        "OMAISHOIDONTUKI": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"}) 
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_laake(file):
    """
    Preprocess THL Avohilmo Laake (medication)
    - Fix data types
    - Convert date formats
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "LAAKEAINE": str,
        "LAAKEPAKKAUSNRO": str,
        "LAAKE_KAUPPANIMI": str,
    }
    date_cols = ["LAAKE_MAARATTY"]
    df = pd.read_csv(
        file, sep=";", dtype=dtypes, encoding="latin-1", parse_dates=date_cols
    )
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == (len(dtypes.keys()) + len(date_cols))
    return df


def preprocess_avohilmo_lahete(file):
    """
    Preprocess THL Avohilmo Lahete (referral)
    - Fix data types
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "JARJESTYS": int,
        "LAHETE_AMMATTIOIKEUS": str,
        "LAHETE_AMMATTI": str,
        "LAHETE_ERIKOISALA": str,
        "LAHETE_YKSIKKO": str,
        "LAHETE_KOHDE": str,
    }
    date_cols = ["LAHETE_AJANKOHTA"]
    df = pd.read_csv(
        file, sep=";", dtype=dtypes, encoding="latin-1", parse_dates=date_cols
    )
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == (len(dtypes.keys()) + len(date_cols))
    return df


def preprocess_avohilmo_rokosuoja(file):
    """
    Preprocess THL Avohilmo Rokosuoja (vaccine protection)
    - Fix data types
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "JARJESTYS": int,
        "ROKOTUSSUOJA": str,
        "LR_JARJESTYS": int,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_rokotus(file):
    """
    Preprocess THL Avohilmo Rokotus (vaccination)
    - Fix data types
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "JARJESTYS": int,
        "LAAKEAINE": str,
        "LAAKEPAKKAUSNRO": str,
        "LAAKE_KAUPPANIMI": str,
        "ANNOS_JARJESTYSNRO": str,
        "ROKOTUSTAPA": str,
        "PISTOSKOHTA": str,
    }
    date_cols = ["LAAKE_MAARATTY", "ROKOTE_ANTOPVM"]
    df = pd.read_csv(
        file, sep=";", dtype=dtypes, encoding="latin-1", parse_dates=date_cols
    )
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})   
    assert df.shape[1] == (len(dtypes.keys()) + len(date_cols))
    return df


def preprocess_avohilmo_toimenpide(file):
    """
    Preprocess THL Avohilmo Toimenpide (operation)
    - Fix data types
    - Fix column order
    """
    dtypes = {"AVOHILMO_ID": int, "TNRO": str, "JARJESTYS": int, "TOIMENPIDE": str}
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})  
    assert df.shape[1] == len(dtypes.keys())
    return df


def preprocess_avohilmo_suu_toimenpide(file):
    """
    Preprocess THL Avohilmo suu toimenpide (mouth operation)
    - Fix data types
    - Fix column order
    """
    dtypes = {
        "AVOHILMO_ID": int,
        "TNRO": str,
        "JARJESTYS": int,
        "TOIMENPIDE": str,
        "TOIMENPIDE_HAMMAS": str,
    }
    df = pd.read_csv(file, sep=";", dtype=dtypes, encoding="latin-1")
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
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
    output_path = THL_AVOHILMO_OUTPUT_DIR / (output_filename + "_" + today + ".csv")

    for file in tqdm(files, desc=output_filename):
        header = True if file == files[0] else False
        func(file).to_csv(output_path, mode="a", index=False, header=header)


if __name__ == "__main__":
    # Preprocessing all the files by category

    preprocessing_loop(THL_AVOHILMO_ICD10, preprocess_avohilmo_icd10, "avohilmo_icd10")
    preprocessing_loop(THL_AVOHILMO_ICPC2, preprocess_avohilmo_icpc2, "avohilmo_icpc2")
    preprocessing_loop(
        THL_AVOHILMO_JATKOHOITO, preprocess_avohilmo_jatkohoito, "avohilmo_jatkohoito"
    )
    preprocessing_loop(
        THL_AVOHILMO_KOTIHOITO, preprocess_avohilmo_kotihoito, "avohilmo_kotihoito"
    )
    preprocessing_loop(THL_AVOHILMO_LAAKE, preprocess_avohilmo_laake, "avohilmo_laake")
    preprocessing_loop(
        THL_AVOHILMO_LAHETE, preprocess_avohilmo_lahete, "avohilmo_lahete"
    )
    preprocessing_loop(
        THL_AVOHILMO_ROKOSUOJA, preprocess_avohilmo_rokosuoja, "avohilmo_rokosuoja"
    )
    preprocessing_loop(
        THL_AVOHILMO_ROKOTUS, preprocess_avohilmo_rokotus, "avohilmo_rokotus"
    )
    preprocessing_loop(
        THL_AVOHILMO_TOIMENPIDE, preprocess_avohilmo_toimenpide, "avohilmo_toimenpide"
    )
    preprocessing_loop(
        THL_AVOHILMO_SUU_TOIMENPIDE,
        preprocess_avohilmo_suu_toimenpide,
        "avohilmo_suu_toimenpide",
    )

    # HACK: the main AvoHilmo files are written in chunks due to the size of the data
    today = datetime.today().strftime("%Y-%m-%d")
    output_path = THL_AVOHILMO_OUTPUT_DIR / ("avohilmo_" + today + ".csv")
    for file in tqdm(THL_AVOHILMO_MAIN, desc="avohilmo main"):
        preprocess_avohilmo_main(file, output_path)
