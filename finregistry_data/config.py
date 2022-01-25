from pathlib import Path

ROOT_DIR = Path("/data")
ORIGINAL_DATA_DIR = ROOT_DIR / "original_data"
PROCESSED_DATA_DIR = ROOT_DIR / "processed_data"

# THL Vaccination
THL_VACCINATION_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_vaccination"
THL_VACCINATION_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_vaccination"
VACCINATION_PROTECTION_DATA_PATH = (
    THL_VACCINATION_INPUT_DIR / "thl2196_rokotussuoja.csv"
)
VACCINATION_REGISTRY_DATA_PATH = (
    THL_VACCINATION_INPUT_DIR / "thl2196_rokoterekisteri.csv.finreg_IDs"
)

# THL Infectious Diseases
THL_INFECTIOUS_DISEASES_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_infectious_diseases"
THL_INFECTIOUS_DISEASES_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_infectious_diseases"
THL_INFECTIOUS_DISEASES_DATA_PATH = (
    THL_INFECTIOUS_DISEASES_INPUT_DIR / "thl2021_2196_ttr.csv.finreg_IDs"
)

# THL Malformations
THL_MALFORMATIONS_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_malformations"
THL_MALFORMATIONS_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_malformations"
THL_MALFORMATIONS_BASIC_DATA_PATH = (
    THL_MALFORMATIONS_INPUT_DIR / "thl2020_2196_er_basic.csv.finreg_IDs"
)
THL_MALFORMATIONS_ANOMALIES_DATA_PATH = (
    THL_MALFORMATIONS_INPUT_DIR / "thl2020_2196_er_anomalies.csv.finreg_IDs"
)

# FICC Intensive Care
FICC_INTENSIVE_CARE_INPUT_DIR = ORIGINAL_DATA_DIR / "ficc_intensive_care"
FICC_INTENSIVE_CARE_OUTPUT_DIR = PROCESSED_DATA_DIR / "ficc_intensive_care"
FICC_INTENSIVE_CARE_TEHO_DATA_PATH = (
    FICC_INTENSIVE_CARE_INPUT_DIR / "thl2020_2196_teho.csv.finreg_IDs"
)
FICC_INTENSIVE_CARE_TEHO_TISS_DATA_PATH = (
    FICC_INTENSIVE_CARE_INPUT_DIR / "thl2020_2196_teho_tiss.csv.finreg_IDs"
)

