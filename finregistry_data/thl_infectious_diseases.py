"""
THL Infectious Diseases data processing 

Reads THL Infectious Diseases data, applies the preprocessing steps below, and writes the result to a file.
- Merge the original dataset with the amendment
- Replace missing values with NA
- Translate variables to English
- Insert `ARVO_KOODI` to missing `ARVO_TEKSTI`
- Reshape data from wide to long format 
- Flatten lists of length 1
- Add and indicator for COVID 
- Parse dates

Input files: 
- thl2021_2196_ttr.csv.finreg_IDs
- thl_2196_ttr.csv.finreg_IDs (amendment)

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
import logging

from finregistry_data.config import (
    THL_INFECTIOUS_DISEASES_DATA_PATH,
    THL_INFECTIOUS_DISEASES_AMENDMENT_DATA_PATH,
    THL_INFECTIOUS_DISEASES_OUTPUT_DIR,
)
from finregistry_data.utils import write_data

MISSING_VALUES = [0]
MISSING_VALUES_STR = [
    "0",
    "ei tietoa",
    "Ei tietoa",
    "ei tiedossa",
]

logging.basicConfig(level=logging.INFO)


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
    logging.info(f"Dataset loaded: {df.shape[0]:,} rows")
    return df


def merge_data(df_original, df_amendment):
    """
    Merge datasets. Identical columns are required.
    
    All rows recorded in 2021 (`Tilastointivuosi` == 2021) are dropped from `df_original` 
    as they are also present in `df_amendment`.
    """
    drop = df_original.loc[
        (df_original["KUVAUS"] == "Tilastointivuosi")
        & (df_original["ARVO_TEKSTI"] == "2021"),
        "TAPAUS_ID",
    ]
    df_original = df_original.loc[~df_original["TAPAUS_ID"].isin(drop)]
    df_original = df_original.reset_index(drop=True)
    df = pd.concat([df_original, df_amendment], ignore_index=True)
    logging.info(f"Datasets merged: {df.shape[0]:,} rows")
    return df


def replace_missing_with_na(df):
    """Replace missing vaues with NA"""
    d = {"ARVO_KOODI": MISSING_VALUES, "ARVO_TEKSTI": MISSING_VALUES_STR}
    df = df.replace(d, pd.NA)
    logging.info(f"Replaced missing values with NA")
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
    logging.info(f"Translated variables")
    return df


def reshape_long_to_wide(df):
    """
    Reshape the data from long to wide format.
    `KOODIN_TNS`-`ARVO_KOODI` pairs with more than one value per `KUVAUS` are returned as lists.
    If `ARVO_TEKSTI` is missing but `ARVO_KOODI` is not, `ARVO_KOODI` is used.
    """

    df["ARVO_TEKSTI"] = [
        code if text is pd.NA else text
        for text, code in zip(df["ARVO_TEKSTI"], df["ARVO_KOODI"])
    ]
    df = df.dropna(subset=["ARVO_TEKSTI"]).reset_index()

    df = (
        df.groupby(["TAPAUS_ID", "TNRO", "KUVAUS"])["ARVO_TEKSTI"]
        .agg(list)
        .reset_index()
    )
    df = df.pivot(
        index=["TAPAUS_ID", "TNRO"], columns="KUVAUS", values="ARVO_TEKSTI"
    ).reset_index()
    logging.info(f"Reshaped data from long to wide format: {df.shape[0]:,} rows")
    return df


def flatten_lists(df):
    """Flatten lists if the column only includes lists of length one"""
    cols = set(df.columns) - set(["TAPAUS_ID", "TNRO"])
    for col in cols:
        list_lengths = df[col].str.len().unique()
        list_lengths = list_lengths[~np.isnan(list_lengths)]
        if len(list_lengths) == 1:
            df[col] = df[col].str[0]
    logging.info(f"Flattened lists")
    return df


def add_covid_indicator(df):
    """
    Add an indicator for rows related to a COVID infection.
    `COVID` is True if `reporting_group` contains "Koronavirus" or "--COVID-19-koronavirusinfektio"
    """
    df["COVID"] = False
    mask1 = df["reporting_group"].str.contains("Koronavirus", regex=False)
    mask2 = df["reporting_group"].str.contains(
        "--COVID-19-koronavirusinfektio", regex=False
    )
    mask = mask1 | mask2
    df.loc[mask, "COVID"] = True
    logging.info(f"Added an indicator for COVID")
    return df


def parse_dates(df, date_cols):
    """Parse dates"""
    df[date_cols] = df[date_cols].apply(
        lambda x: pd.to_datetime(x, format="%Y-%m-%d", errors="coerce").dt.date
    )
    logging.info(f"Parsed dates")
    return df


def preprocess_data(df):
    """Apply the preprocessing pipeline"""
    df = replace_missing_with_na(df)
    df = translate_variables(df)
    df = reshape_long_to_wide(df)
    df = flatten_lists(df)
    df = add_covid_indicator(df)
    df = parse_dates(df, ["sampling_date"])
    df = df.rename(columns={"TNRO": "FINREGISTRYID"})
    return df


if __name__ == "__main__":

    df_original = read_data(THL_INFECTIOUS_DISEASES_DATA_PATH)
    df_amendment = read_data(THL_INFECTIOUS_DISEASES_AMENDMENT_DATA_PATH)

    df = merge_data(df_original, df_amendment)
    df = preprocess_data(df)

    write_data(df, THL_INFECTIOUS_DISEASES_OUTPUT_DIR, "infectious_diseases", "csv")
    write_data(df, THL_INFECTIOUS_DISEASES_OUTPUT_DIR, "infectious_diseases", "feather")
