"""Util functions for FinRegistry data processing"""

from datetime import datetime
from pathlib import Path


def write_data(df, outputdir, dataset_name, format="csv"):
    """
    Write data to a csv or feather file
    
    Args:
      - df (pd.DataFrame): dataframe to be written to a file
      - outputdir (str): output directory path 
      - dataset_name (str): name of the dataset, used for naming the output file 
      - format (str): output file format; "csv" or "feather" 

    """
    today = datetime.today().strftime("%Y-%m-%d")
    outputdir = Path(outputdir)
    if format == "csv":
        filename = dataset_name + "_" + today + ".csv"
        df.to_csv(outputdir / filename, sep=";", index=False)
    elif format == "feather":
        filename = dataset_name + "_" + today + ".feather"
        df.to_feather(outputdir / filename)
    else:
        print("Invalid file format")
