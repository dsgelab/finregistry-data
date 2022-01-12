from pathlib import Path

ROOT_DIR = Path("/data")
ORIGINAL_DATA_DIR = ROOT_DIR / "original_data"

THL_VACCINATION_DIR = ORIGINAL_DATA_DIR / "thl_vaccination"
VACCINATION_PROTECTION_PATH = THL_VACCINATION_DIR / "thl2196_rokotussuoja.csv"
VACCINATION_REGISTRY_PATH = (
    THL_VACCINATION_DIR / "thl2196_rokoterekisteri.csv.finreg_IDs"
)
