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


def preprocess_data(df):
    df = replace_missing_with_na(df)
    df = translate_variables(df)
    df = reshape_long_to_wide(df)
    df = drop_columns(df)
    return df
