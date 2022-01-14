from pathlib import Path

ROOT_DIR = Path("/data")
ORIGINAL_DATA_DIR = ROOT_DIR / "original_data"
PROCESSED_DATA_DIR = ROOT_DIR / "processed_data"

THL_VACCINATION_INPUT_DIR = ORIGINAL_DATA_DIR / "thl_vaccination"
THL_VACCINATION_OUTPUT_DIR = PROCESSED_DATA_DIR / "thl_vaccination"
VACCINATION_PROTECTION_DATA_PATH = (
    THL_VACCINATION_INPUT_DIR / "thl2196_rokotussuoja.csv"
)
VACCINATION_REGISTRY_DATA_PATH = (
    THL_VACCINATION_INPUT_DIR / "thl2196_rokoterekisteri.csv.finreg_IDs"
)
