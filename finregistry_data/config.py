from pathlib import Path

ROOT_DIR = Path("/data")
ORIGINAL_DATA_DIR = ROOT_DIR / "original_data"
PROCESSED_DATA_DIR = ROOT_DIR / "processed_data"

# THL Birth registry
THL_BIRTH_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_birth"
THL_BIRTH_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_birth"
THL_BIRTH_DATA_PATH = THL_BIRTH_INPUT_DIR / "thl2021_2196_synret.csv.finreg_IDs"

# THL Vaccination
THL_VACCINATION_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_vaccination"
THL_VACCINATION_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_vaccination"
VACCINATION_PROTECTION_DATA_PATH = THL_VACCINATION_INPUT_DIR / "thl2196_rokotussuoja.csv"
VACCINATION_REGISTRY_DATA_PATH = THL_VACCINATION_INPUT_DIR / "thl2196_rokotus.csv.finreg_IDs"

# THL Infectious Diseases
THL_INFECTIOUS_DISEASES_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_infectious_diseases"
THL_INFECTIOUS_DISEASES_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_infectious_diseases"
THL_INFECTIOUS_DISEASES_DATA_PATH = THL_INFECTIOUS_DISEASES_INPUT_DIR / "thl2021_2196_ttr.csv.finreg_IDs"
THL_INFECTIOUS_DISEASES_AMENDMENT_DATA_PATH = THL_INFECTIOUS_DISEASES_INPUT_DIR / "thl2196_ttr.csv.finreg_IDs"

# THL Malformations
THL_MALFORMATIONS_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_malformations"
THL_MALFORMATIONS_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_malformations"
THL_MALFORMATIONS_BASIC_DATA_PATH = THL_MALFORMATIONS_INPUT_DIR / "thl2020_2196_er_basic.csv.finreg_IDs"
THL_MALFORMATIONS_ANOMALIES_DATA_PATH = THL_MALFORMATIONS_INPUT_DIR / "thl2020_2196_er_anomalies.csv.finreg_IDs"

# THL Cancer
THL_CANCER_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_cancer"
THL_CANCER_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_cancer"
THL_CANCER_DATA_PATH = THL_CANCER_INPUT_DIR / "fcr_data.csv.finreg_IDs"

# FICC Intensive Care
FICC_INTENSIVE_CARE_INPUT_DIR = ORIGINAL_DATA_DIR / "ficc_intensive_care"
FICC_INTENSIVE_CARE_OUTPUT_DIR = PROCESSED_DATA_DIR / "ficc_intensive_care"
FICC_INTENSIVE_CARE_TEHO_DATA_PATH = FICC_INTENSIVE_CARE_INPUT_DIR / "thl2020_2196_teho.csv.finreg_IDs"
FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH = FICC_INTENSIVE_CARE_INPUT_DIR / "thl2020_2196_teho_tiss.csv.finreg_IDs"

# KELA Kanta
KELA_KANTA_INPUT_DIR = ORIGINAL_DATA_DIR / "kela_kanta"
KELA_KANTA_OUTPUT_DIR = PROCESSED_DATA_DIR / "kela_kanta"

# Pension
ETK_PENSION_INPUT_DIR = ORIGINAL_DATA_DIR / "etk_pension"
ETK_PENSION_OUTPUT_DIR = PROCESSED_DATA_DIR / "etk_pension"
ETK_PENSION_ELAKE_DATA_PATH = ETK_PENSION_INPUT_DIR / "etk_elake1990_2021.csv.finreg_IDs"
ETK_PENSION_PALKATON_DATA_PATH = ETK_PENSION_INPUT_DIR / "etk_palkaton2005_2021.csv.finreg_IDs"
ETK_PENSION_VUANSIOT_DATA_PATH = ETK_PENSION_INPUT_DIR / "etk_vuansiot2005_2021.csv.finreg_IDs"
ETK_PENSION_CPI_DATA_PATH = ETK_PENSION_INPUT_DIR / "consumer_price_index_1972_2021.csv"

# SF education, occupation & SES
SF_SOCIOECONOMIC_INPUT_DIR = ORIGINAL_DATA_DIR / "sf_socioeconomic"
SF_SOCIOECONOMIC_OUTPUT_DIR = PROCESSED_DATA_DIR / "sf_socioeconomic"
SF_EDUCATION_DATA_PATHS = [
    SF_SOCIOECONOMIC_INPUT_DIR / "tutkinto_u1442_a.csv.finreg_IDs",
    SF_SOCIOECONOMIC_INPUT_DIR / "tutkinto_u1442_al10_osa1.csv.finreg_IDs",
    SF_SOCIOECONOMIC_INPUT_DIR / "tutkinto_u1442_al10_osa2.csv.finreg_IDs",
]
SF_OCCUPATION_DATA_PATHS = [
    SF_SOCIOECONOMIC_INPUT_DIR / "ammatti_u1442_a.csv.finreg_IDs",
    SF_SOCIOECONOMIC_INPUT_DIR / "ammatti_u1442_al10.csv.finreg_IDs"
]