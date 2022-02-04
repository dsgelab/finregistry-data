"""
Kela Kanta data preprocessing

Reads Kela Kanta data, applies the preprocessing steps below and writes the result to files.
- remove extra linebreaks
- remove empty lines
- transform base16 ints to base10 ints
- parse dates
- replace "," with "." as a decimal point

Note: running this script on ePouta takes several hours.
Speed could be improved with e.g. multiprocessing if needed.

Input files: 
- 107_522_2021_LM_<YYYY>.csv.finreg_IDs (11 files)
- 107_522_2021_LT_<YYYY>.csv.finreg_IDs (11 files)

Output files: 
- prescriptions_<YYYY>_<YYYY-MM-DD>.csv (11 files)
- deliveries_<YYYY>_<YYYY-MM-DD>.csv (11 files)
"""

import os
import re
import pandas as pd
from datetime import datetime
from functools import partial
from finregistry_data.config import KELA_KANTA_INPUT_DIR, KELA_KANTA_OUTPUT_DIR


def read_prescription_data(filepath):
    """Read drug prescriptions data in chunks"""
    hash_to_int = partial(int, base=16)
    hash_cols = [
        "CDA_ID_MD5HASH",
        "CDA_SET_ID_MD5HASH",
        "DOC_GROUP_MD5HASH",
        "CDA_ADDENDUM_REF_MD5HASH",
        "CDA_RPLC_ID_MD5HASH",
        "PRO_PERSON_REG_MD5HASH",
        "ORGANIZATION_OID_MD5HASH",
    ]
    date_cols = ["CREATION_DATE"]
    dtypes = {
        "PATIENT_ID": str,
        "DOC_TYPE_CODE": float,
        "DOC_VERSION": float,
        "DRUG_NAME_C": str,
        "DOSE_QUANTITY_TEXT": str,
        "ATC_CODE": str,
        "PURPOSE_OF_USE": str,
        "DOSAGE_INSTRUCTIONS": str,
        "ITERATION_CODE": float,
        "TYPE_1_AMOUNT": str,
        "TYPE_1_SIZE": str,
        "TYPE_2_AMOUNT": str,
        "TYPE_2_SIZE_UNIT": str,
        "TYPE_3_TIME": str,
        "TYPE_3_UNIT": str,
        "PRODUCT_CODE": float,
        "DOSE_DISTRIBUTION": str,
        "PREPARATION_TYPE_CODE": float,
        "RESEPTISTATUS": str,
        "LAAKEMUOTOKOODI": float,
        "ERIKOISALA_CODE": str,
        "MED_EXCHANGE_BAN": str,
        "RENEWAL_BAN": str,
    }
    chunks = pd.read_csv(
        filepath,
        sep=";",
        engine="python",
        encoding="utf-8",
        encoding_errors="ignore",
        on_bad_lines="warn",
        converters=dict.fromkeys(hash_cols, hash_to_int),
        parse_dates=date_cols,
        dtype=dtypes,
        chunksize=10000,
    )
    return chunks


def read_delivery_data(filepath):
    """Read drug delivery data in chunks"""
    hash_to_int = partial(int, base=16)
    hash_cols = [
        "CDA_ID_MD5HASH",
        "DOC_GROUP_MD5HASH",
        "CDA_ADDENDUM_REF_MD5HASH",
        "CDA_RPLC_ID_MD5HASH",
    ]
    date_cols = ["CREATION_DATE"]
    dtypes = {
        "PATIENT_ID": str,
        "DRUG_NAME_C": str,
        "DOSE_QUANTITY_TEXT": str,
        "ATC_CODE": str,
        "MED_EXCHANGED": str,
        "DIS_AMOUNT_CALC_TXT": str,
        "DIS_AMT_VALUE": str,
        "DIS_AMOUNT_TXT": str,
        "DIS_AMT_UNIT": str,
        "PRODUCT_CODE1": str,
        "DOSE_DISTRIBUTION": str,
        "PREPARATION_TYPE_CODE": float,
        "RESEPTISTATUS": str,
        "LAAKEMUOTOKOODI": float,
        "DELIVERY_FEE": float,
    }
    chunks = pd.read_csv(
        filepath,
        sep=";",
        engine="python",
        encoding="utf-8",
        encoding_errors="ignore",
        on_bad_lines="warn",
        decimal=",",
        converters=dict.fromkeys(hash_cols, hash_to_int),
        parse_dates=date_cols,
        dtype=dtypes,
        chunksize=10000,
    )
    return chunks


def get_output_filepath(input_filepath):
    """Get output filepath from input filepath."""
    input_filename = os.path.basename(input_filepath)
    today = datetime.today().strftime("%Y-%m-%d")
    pattern = r"^107_522_2021_(.{2})_(\d{4})\.csv\.finreg_IDs"
    filetype, year = re.findall(pattern, input_filename, re.IGNORECASE)[0]
    filetype = "prescriptions" if filetype == "LM" else "deliveries"
    output_filename = filetype + "_" + year + "_" + today + ".csv"
    output_path = KELA_KANTA_OUTPUT_DIR / output_filename
    return output_path


def write_chunk_to_csv(chunk, output_filepath):
    """Writes chunk to csv"""
    chunk.to_csv(
        output_filepath,
        mode="a",
        header=not os.path.exists(output_filepath),
        index=False,
        sep=";",
    )


if __name__ == "__main__":

    # Preprocess drug prescriptions
    # prescription_files = KELA_KANTA_INPUT_DIR.glob("107_522_2021_LM_*")
    # for prescription_file in prescription_files:
    #     print(prescription_file)
    #     output_filepath = get_output_filepath(prescription_file)
    #     chunks = read_prescription_data(prescription_file)
    #     for chunk in chunks:
    #         chunk = chunk.replace("\n", " ", regex=True)
    #         write_chunk_to_csv(chunk, output_filepath)

    # Preprocess drug deliveries
    delivery_files = KELA_KANTA_INPUT_DIR.glob("107_522_2021_LT_*")
    for delivery_file in delivery_files:
        print(delivery_file)
        output_filepath = get_output_filepath(delivery_file)
        chunks = read_delivery_data(delivery_file)
        for chunk in chunks:
            chunk = chunk.replace("\n", " ", regex=True)
            write_chunk_to_csv(chunk, output_filepath)
