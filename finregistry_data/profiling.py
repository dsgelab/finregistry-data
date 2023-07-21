"""
Data profiling for data dictionaries
- number of rows 
- number of columns 
- for each column: 
    - % of missing values 
    - number of unique values 
    - minimum value 
    - maximum value 
    - 5 most frequent values (min 10 subjects)

If there are less than MIN_SUBJECTS subjects MIN_SUBJECTS_STR will be printed instead
"""

import numpy as np
import pandas as pd

MIN_SUBJECTS = 5
MIN_SUBJECTS_STR = "<not enough subjects>"


def check_min_subjects(values, df, col, id_col):
    res = np.array([], dtype=str)
    values = np.array(values)
    if col == id_col:
        res = np.append(res, MIN_SUBJECTS_STR)
    elif id_col:
        for value in values[~pd.isnull(values)]:
            n_subjects = len(set(df.loc[df[col] == value, id_col].values))
            value = value if n_subjects >= MIN_SUBJECTS else MIN_SUBJECTS_STR
            res = np.append(res, value)
            if value == MIN_SUBJECTS_STR:
                break
    else:
        res = values
    res = " ".join(res.astype(str))
    return res


def profile(df, id_col=None):
    nrows, ncols = df.shape

    d = {
        "col": df.columns,
        "missing_pct": [],
        "unique_values": [],
        "min": [],
        "max": [],
        "top5": [],
    }

    for col in df:

        print(col)
        counts = df[col].value_counts()

        missing_pct = round(df[col].isnull().sum(axis=0) / nrows * 100, 2)
        unique_values = len(counts)
        min_value = check_min_subjects([counts.index.min()], df, col, id_col)
        max_value = check_min_subjects([counts.index.max()], df, col, id_col)
        top5_values = check_min_subjects(
            counts[counts >= MIN_SUBJECTS].head(5).index, df, col, id_col
        )

        d["missing_pct"].append(missing_pct)
        d["unique_values"].append(unique_values)
        d["min"].append(min_value)
        d["max"].append(max_value)
        d["top5"].append(top5_values)

    profiles = pd.DataFrame.from_dict(d)

    print(f"Number of rows: {nrows}")
    print(f"Number of columns: {ncols}")
    print("Column profiles:")
    print(profiles)

    return profiles
