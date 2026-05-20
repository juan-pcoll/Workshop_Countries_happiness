from pathlib import Path
import pandas as pd


BASE_DIR = Path.cwd().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"

def get_csv_files():
    """
    Get all CSV files from raw data directory.
    """

    csv_files = list(RAW_DATA_PATH.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_PATH}"
        )

    return csv_files


def extract_single_file(file_path):
    """
    Extract a single CSV file into a DataFrame.
    """

    try:
        df = pd.read_csv(file_path)

        # Extract year from filename
        df["year"] = file_path.stem

        return df

    except Exception as e:
        print(f"[ERROR] Failed loading {file_path.name}")
        print(e)

        return None


def extract_all_data():
    """
    Extract all CSV datasets.
    """

    csv_files = get_csv_files()

    datasets = {}

    for file in csv_files:

        df = extract_single_file(file)

        if df is not None:
            datasets[file.stem] = df

    return datasets


if __name__ == "__main__":

    data = extract_all_data()

    df_2015 = data["2015"]

    df_2016 = data["2016"]

    df_2017 = data["2017"]

    df_2018 = data["2018"]

    df_2019 = data["2019"]

    for year, df in data.items():
        print("\n")
        print(f"Dataset Year: {year}")
        print(df.head())
