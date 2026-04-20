# core/data_loader.py

import pandas as pd


def load_csv(file_path):
    """
    Load student dataset from CSV file.
    Removes missing values.
    Returns cleaned DataFrame.
    """

    try:
        df = pd.read_csv(file_path)

        # Drop missing values
        df = df.dropna()

        return df

    except Exception as e:
        print("Error loading file:", e)
        return None