"""
THL Birth data processing 

Reads THL Birth data, applies the preprocessing steps below, and writes the result to a file.
- parse dates
- replace empty strings with NA

Input file: 
- thl2021_2196_synret.csv.finreg_IDs

Output files: 
- birth_<YYYY-MM-DD>.csv
- birth_<YYYY-MM-DD>.feather
"""

import pandas as pd
from finregistry_data.config import THL_BIRTH_DATA_PATH, THL_BIRTH_OUTPUT_DIR
from finregistry_data.utils import write_data

NA_VALUES = ["", " "]


def read_data(filepath=THL_BIRTH_DATA_PATH):
    """
    Read THL Birth dataset.
    Numeric columns with at least one NaN are read as floats.
    """
    dtypes = {
        "AITI_TNRO": str,
        "LAPSI_TNRO": str,
        "KESTOVKPV": str,
        "TILASTOVUOSI": int,
        "AITI_HETU_OK": bool,
        "LAPSI_HETU_OK": bool,
        "AIDIN_SYNTYMAPVM": str,
        "AITI_IKA": int,
        "ASUINKUNTA": int,
        "KANSALAISUUS": float,
        "SIVIILISAATY": int,
        "AVOLIITTO": float,
        "AMMATTILUOKITUS": float,
        "SOSEKO": float,
        "AIEMMATRASKAUDET": float,
        "KESKENMENOJA": float,
        "KESKEYTYKSIA": float,
        "ULKOPUOLISIA": float,
        "AIEMMATSYNNYTYKSET": float,
        "KUOLLEENASYNT": float,
        "TARKASTUKSET": float,
        "POLILLA": float,
        "NEUVOLAPVM": str,
        "APAINO": float,
        "APITUUS": float,
        "TUPAKOINTITUNNUS": int,
        "FOOLIHAPPOLISA": float,
        "FOOLIHAPPOLISA_KK": str,
        "RDIAG1": str,
        "RDIAG2": str,
        "RDIAG3": str,
        "RDIAG4": str,
        "RDIAG5": str,
        "RDIAG6": str,
        "RDIAG7": str,
        "RDIAG8": str,
        "RDIAG9": str,
        "RDIAG10": str,
        "VERENVUO": int,
        "VERENPAI": int,
        "ENNENAIK": int,
        "MUUSYY": int,
        "IVF": int,
        "ICSI": int,
        "PAS": int,
        "BLASTOKYSTIVILJELY": int,
        "ALKION_VITRIFIKAATIO": int,
        "ALKIODIAGNOSTIIKKA": int,
        "LUOVUTETTU_SUKUSOLU": int,
        "INSEMINAATIO": int,
        "KYPSYTYSHOITO": int,
        "HEDHOITO_EI_TIETOA_TYYPISTA": int,
        "KOEPUTKI": float,
        "ALKIONSIIRTO": int,
        "MUUKEINO": float,
        "NISKATURVOTUS_PAKSUUS_MM": float,
        "KROMOSOMIEN_SEULONTA_NIPT": int,
        "TRISOMIA_21_RISKILUKU": str,
        "TARKENNETTU_ULTRA": int,
        "KORIONVI": int,
        "LVESITUT": int,
        "ALKURASKAUDEN_INFEKTIOSEULA": float,
        "STREPTOKOKKI_B_SEULA": float,
        "ASEKTIO": int,
        "YMPARILEIKATTU": int,
        "TROMBOOSIPROF": int,
        "ANEMIA": int,
        "SOKERI_TEHTY": int,
        "SOKERI_PATOL": int,
        "INSULIINI_ALOITETTU": int,
        "MUU_RASKAUS_DIABETES_HOITO": int,
        "KORTIKOSTEROIDI": int,
        "DIABETES": float,
        "TUKIOMM": float,
        "SYNNYTYS_PALTU": float,
        "SYNTYMAPAIKKA": float,
        "VIIMEINEN_KUUKAUTISPVM": str,
        "LAPSIVEDENMENOPVM": str,
        "SKESTO_AVAUT": float,
        "SKESTO_PONN": float,
        "SKESTO_AVAUT_H": float,
        "SKESTO_AVAUT_MIN": float,
        "SKESTO_PONN_H": float,
        "SKESTO_PONN_MIN": float,
        "EI_LIEVITYSTA": int,
        "EI_LIEVITYS_TIETOA": int,
        "EPIDURAALI": int,
        "SPINAALI": int,
        "SPINAALI_EPIDUR": int,
        "PARASERVIKAALI": int,
        "PUDENDAALI": int,
        "ILOKAASU": int,
        "MUULAAKLIEV": int,
        "MUULIEVITYS": int,
        "KAYNNISTYS": int,
        "EDISTAMINEN": int,
        "PUHKAISU": int,
        "OKSITOSIINI": int,
        "PROSTAGLANDIINI": int,
        "ISTUKANIRROITUS": int,
        "KAAVINTA": int,
        "OMPELU": int,
        "GBS_PROFYLAKSIA": int,
        "AIDIN_ANTIBIOOTTIHOITO": int,
        "VERENSIIRTO": int,
        "YMPARILEIKKAUKSEN_AVAUS": int,
        "KOHDUNPOISTO": int,
        "EMBOLISAATIO": int,
        "AITISIIRRETTY": int,
        "SYNNYTYSTAPATUNNUS": float,
        "VUODON_MAARA": float,
        "ETINEN": int,
        "ISTIRTO": int,
        "RKOURIS": int,
        "HARTIADYSTOKIA": int,
        "ASFYKSIA": int,
        "PERATILA": int,
        "MUUTARPO": int,
        "SDIAG1": str,
        "SDIAG2": str,
        "SDIAG3": str,
        "SDIAG4": str,
        "SDIAG5": str,
        "SDIAG6": str,
        "SDIAG7": str,
        "SDIAG8": str,
        "SDIAG9": str,
        "SDIAG10": str,
        "LAPSEN_SYNTYMAPVM": str,
        "SYNTYMAKLO": str,
        "SYNTYMATILATUNNUS": int,
        "SUKUP": int,
        "SIKIOITA": int,
        "MONISIKI_SYNNYTYSTUNNUS": float,
        "KAKSOSUUDEN_TYYPPI": float,
        "SYNTYMAPAINO": float,
        "SYNTYMAPITUUS": float,
        "PAANYMPARYS": float,
        "APGAR_1MIN": float,
        "APGAR_5MIN": float,
        "NAPAVALTIMOPH": float,
        "NAPALASKIMOPH": float,
        "HENGITYS_AVUSTUS_ALKU": int,
        "LISAHAPPI_ALKU": int,
        "PAINELUELVYTYS_ALKU": int,
        "ADRENALIINI_ALKU": int,
        "NESTETAYTTO_ALKU": int,
        "RESPIRAATTORI": int,
        "ELVYTYS": int,
        "ELVALVONTA": int,
        "TEHO": int,
        "VALVONTA": int,
        "MUUSAIR": int,
        "ELVYTYS_ALKU_JALKEEN": int,
        "VERENVAIHTO": int,
        "VALOHOITO": int,
        "ANTIBIOOTTI": int,
        "ANTIBIOOTTI_ENINT_2VRK": int,
        "ANTIBIOOTTI_YLI_2VRK": int,
        "KVITAMIINI": int,
        "BCG_ROKOTUS": int,
        "HEPATIITTI_B_ROKOTUS": int,
        "HYPOTYREOOSI": int,
        "AINEENVAIHDUNTA": int,
        "VIILENNYSHOITO": int,
        "HYPOGLYKEMIAN_IV_GLUK_HOITO": int,
        "LAITE_HENGITYSTUKI": int,
        "HAPPI_KYLLASTEISYYS_SEULA": int,
        "ICD10_1": str,
        "ICD10_2": str,
        "ICD10_3": str,
        "ICD10_4": str,
        "ICD10_5": str,
        "ICD10_6": str,
        "ICD10_7": str,
        "ICD10_8": str,
        "ICD10_9": str,
        "ICD10_10": str,
        "HOITOPAIKKATUNNUS": float,
        "LAPSEN_LAHTOPVM": str,
        "LAPSEN_LAHTOKLO": str,
        "LAPSEN_KUOLINPVM": str,
        "LAPSEN_KUOLINKLO": str,
        "KUOLLEISUUS": int,
        "IMEVAISKUOLLEISUUS": int,
        "LAPSEN_RAVINTO_7VRK": float,
        "LISAMAITO": float,
        "AITI_SEURANTAPVM": str,
        "AITI_TULOPVM": str,
        "AITI_LAHTOPVM": str,
    }

    df = pd.read_csv(filepath, sep=";", dtype=dtypes, na_values=NA_VALUES)

    return df


def parse_dates(df):
    """
    Parse dates from dd.mm.yyyy to yyyy-mm-dd.
    Invalid dates (invalid format, too far in the future) are returned as missing (NaT).
    """
    date_cols = [
        "AIDIN_SYNTYMAPVM",
        "NEUVOLAPVM",
        "VIIMEINEN_KUUKAUTISPVM",
        "LAPSIVEDENMENOPVM",
        "LAPSEN_SYNTYMAPVM",
        "LAPSEN_LAHTOPVM",
        "LAPSEN_KUOLINPVM",
        "AITI_TULOPVM",
        "AITI_LAHTOPVM",
        "AITI_SEURANTAPVM",
    ]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col], format="%d.%m.%Y", errors="coerce")
        df[date_col] = df[date_col].dt.date

    return df


if __name__ == "__main__":
    df = read_data(THL_BIRTH_DATA_PATH)
    df = parse_dates(df)
    df.columns = df.columns.str.upper()
    df = df.rename(
        columns={"LAPSI_TNRO": "LAPSI_FINREGISTRYID", "AITI_TNRO": "AITI_FINREGISTRYID"}
    )

    write_data(df, THL_BIRTH_OUTPUT_DIR, "birth", "csv")
    write_data(df, THL_BIRTH_OUTPUT_DIR, "birth", "feather")
