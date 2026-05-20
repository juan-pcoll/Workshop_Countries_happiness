import os 
import pandas as pd 
from sqlalchemy import create_engine

def load_data():
    df = pd.read_csv('/data/processed/happiness_unified.csv')

    print("Datos finales:")
    print(df.head())
'''
def load_to_db(df):

    engine = create_engine(
    'postgresql://airflow:airflow@postgres:5432/airflow'
    )
    
    df.to_sql(
        'fact_tracks',
        engine,
        if_exists='replace',  # o 'append'
        index=False
    )

    print("Data loaded to database")

    df.to_csv("/opt/airflow/data/processed/final_df.csv", index=False)

def load_dw(engine, dim_artist, dim_genre, fact):

    dim_artist.to_sql('dim_artist', engine, if_exists='replace', index=False)
    dim_genre.to_sql('dim_genre', engine, if_exists='replace', index=False)
    fact.to_sql('fact_tracks', engine, if_exists='replace', index=False)

    print("DW cargado correctamente")

'''