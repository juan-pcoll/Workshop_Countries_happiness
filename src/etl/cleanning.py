import pandas as pd

def cleanning(df, df_2015, df_2016, df_2017, df_2018, df_2019):
    # Drop unnecessary columns
    columns_to_drop = [
        "Region",
        "Standard Error",
        "Lower Confidence Interval",
        "Upper Confidence Interval",
        "Whisker.high",
        "Whisker.low",
        "Dystopia Residual",
        "Dystopia.Residual"
    ]

    existing_columns2015 = [
        col for col in columns_to_drop
        if col in df_2015.columns
    ]
    C2015 = df_2015.drop(columns=existing_columns2015)

    existing_columns2016 = [
        col for col in columns_to_drop
        if col in df_2016.columns
    ]
    C2016 = df_2016.drop(columns=existing_columns2016)

    existing_columns2017 = [
        col for col in columns_to_drop
        if col in df_2017.columns
    ]
    C2017 = df_2017.drop(columns=existing_columns2017)

    existing_columns2018 = [
        col for col in columns_to_drop
        if col in df_2018.columns
    ]
    C2018 = df_2018.drop(columns=existing_columns2018)

    existing_columns2019 = [
        col for col in columns_to_drop
        if col in df_2019.columns
    ]
    C2019 = df_2019.drop(columns=existing_columns2019)
    
    dfs = [
        C2015,
        C2016,
        C2017,
        C2018,
        C2019   
    ]

    unified_df = pd.concat(
    dfs,
    ignore_index=True
    )

    unified_df.loc[
    (unified_df["Happiness_score"] > 0)
    &
    (unified_df["Economy_(GDP_per_Capita)"] > 0)
    &
    (unified_df["freedom"] > 0)
]

    return df, dfs, unified_df, C2015, C2016, C2017, C2018, C2019
