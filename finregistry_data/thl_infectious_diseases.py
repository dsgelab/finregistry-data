"""
THL Infectious Diseases data processing 

Reads THL Infectious Diseases data, applies the preprocessing steps below, and writes the result to a file.
- Replace missing values with NA
- Translate variables to English
- Reshape data from wide to long format 
- Drop redundant columns 
- Flatten lists of length 1
- TODO: insert ARVO_KOODI to missing ARVO_TEKSTI

Input file: 
- thl2021_2196_ttr.csv.finreg_IDs

Output files: 
- infectious_diseases_<YYYY-MM-DD>.csv
- infectious_diseases_<YYYY-MM-DD>.feather

Examples of output dataset usage: 

Example 1: Filter by value in list column
```
temp = df[~df["diagnosis_code"].isna()]
temp[temp["diagnosis_code"].apply(lambda x: "<diagnosis code>" in x)]
```

Example 2: Unlist list column
```
temp = df.loc[~df["diagnosis_code"].isna()] # not required but faster
temp["diagnosis_code"].apply(pd.Series)
```

Example 3: Count unique values in list column:
```
temp = df.loc[~df["diagnosis_code"].isna()]
pd.Series([item for sublist in temp["diagnosis_code"] for item in sublist]).value_counts()
```
"""

import pandas as pd
import numpy as np
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


def translate_variables(df):
    """
    Translate variables with _ as separator.
    Needed to reshape data from long to wide format.
    """
    d = {
        "Alkuperäinen sairaanhoitopiiri": "original_hospital_district",
        "Diagnoosikoodi": "diagnosis_code",
        "Hengityksen tukihoito": "breathing_assistance_treatment",
        "Hoidon lopputulos/status": "treatment_status",
        "Ikä vuosina": "age_years",
        "Ilmoitustyyppi": "notice_group",
        "Kansalaisuusluokka": "nationality_category",
        "Kulunut aika tilastoinnin ja kuoleman välillä": "time_between_recording_and_death",
        "Laboratoriotyyppi": "laboratory_type",
        "Lähikontakti COVID-19 -tapaukseen tai -epäiltyyn": "contact_with_covid19_case_or_suspected_case",
        "Mikrobi": "microbe",
        "Mikrobiominaisuus": "microbe_property",
        "Mikrobisuku": "microbal_family",
        "Näyte kantakokoelmassa": "sample_in_kantakokoelma",
        "Näytelaatu": "sample_type",
        "Näytteenottopäivä": "sampling_date",
        "Pitkäaikaissairaus": "chronic_disease",
        "Postinumero": "zip_code",
        "Potilaan alkuperä": "patient_origin",
        "Potilaan alkuperän maantieteellinen alue": "patient_origin_geographical_area",
        "Raportointiryhmä": "reporting_group",
        "Sairaalahoito": "hospital_care",
        "Sairaanhoitopiiri": "hospital_district",
        "Sairauden oireiden alkamiskuukausi": "symptom_start_month",
        "Sairauden oireiden alkamispäivämäärä": "symptom_start_date",
        "Sairauden oireiden alkamisvuosi": "symptom_start_year",
        "Sairauden oireita": "symptoms",
        "Seurantakohde, myös historia": "monitoring_target_incl_history",
        "Syntymävuosi": "birth_year",
        "Tartuntamaa": "infection_country",
        "Tartuntamaaluokka": "infection_country_category",
        "Tauti": "disease",
        "Tehohoito": "intensive_care",
        "Terveydenhuollon työntekijä": "healthcare_worker",
        "Tilastointikuukausi": "recording_month",
        "Tilastointiviikko": "recording_week",
        "Tilastointivuosi": "recording_year",
        "Toteamistapa": "diagnosis_method",
        "Viikko": "week",
    }
    df = df.replace({"KUVAUS": d})
    return df


def reshape_long_to_wide(df):
    """
    Reshape the data from long to wide format.
    KOODIN_TNS-ARVO_KOODI pairs with more than one value per KUVAUS are returned as lists.
    """
    df = df.dropna(subset=["ARVO_TEKSTI"]).reset_index()
    df = (
        df.groupby(["TAPAUS_ID", "TNRO", "KUVAUS"])["ARVO_TEKSTI"]
        .agg(list)
        .reset_index()
    )
    df = df.pivot(
        index=["TAPAUS_ID", "TNRO"], columns="KUVAUS", values="ARVO_TEKSTI"
    ).reset_index()
    return df


def drop_columns(df):
    """Drop columns that are not needed"""
    drop = [
        "age_years",
        "recording_month",
        "recording_year",
        "symptom_start_month",
        "symptom_start_year",
        "time_between_recording_and_death",
        "week",
    ]
    df = df.drop(columns=drop)
    return df


def flatten_lists(df):
    """Flatten lists if the column only includes lists of length one"""
    cols = set(df.columns) - set(["TAPAUS_ID", "TNRO"])
    for col in cols:
        list_lengths = df[col].str.len().unique()
        list_lengths = list_lengths[~np.isnan(list_lengths)]
        if len(list_lengths) == 1:
            df[col] = df[col].str[0]
    return df


def preprocess_data(df):
    """Apply the preprocessing pipeline"""
    df = replace_missing_with_na(df)
    df = translate_variables(df)
    df = reshape_long_to_wide(df)
    df = drop_columns(df)
    df = flatten_lists(df)
    return df
