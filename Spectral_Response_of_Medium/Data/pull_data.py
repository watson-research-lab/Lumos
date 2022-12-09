import os
from pathlib import Path
from sshtunnel import SSHTunnelForwarder
import psycopg2
import yaml
from pandas import DataFrame
import pandas as pd

def process_df(df):
    key_415, key_445, key_480, key_515, key_555, key_590, key_630, key_680 = 180, 181, 182, 183, 184, 185, 186, 187
    df.columns = ['key','timestamp','counts']
    df_415 = df.loc[df['key'] == key_415].drop('key', axis = 1)
    df_415.columns = ['timestamp', '415_counts']
    df_445 = df.loc[df['key'] == key_445].drop('key', axis = 1)
    df_445.columns = ['timestamp', '445_counts']
    df_480 = df.loc[df['key'] == key_480].drop('key', axis = 1)
    df_480.columns = ['timestamp', '480_counts']
    df_515 = df.loc[df['key'] == key_515].drop('key', axis = 1)
    df_515.columns = ['timestamp', '515_counts']
    df_555 = df.loc[df['key'] == key_555].drop('key', axis = 1)
    df_555.columns = ['timestamp', '555_counts']
    df_590 = df.loc[df['key'] == key_590].drop('key', axis = 1)
    df_590.columns = ['timestamp', '590_counts']
    df_630 = df.loc[df['key'] == key_630].drop('key', axis = 1)
    df_630.columns = ['timestamp', '630_counts']
    df_680 = df.loc[df['key'] == key_680].drop('key', axis = 1)
    df_680.columns = ['timestamp', '680_counts']
    final_df = pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(pd.merge(df_415, df_445, on='timestamp'),
            df_480, on='timestamp'), df_515, on='timestamp'), df_555, on='timestamp'), df_590, on='timestamp'),
            df_630, on='timestamp'), df_680, on='timestamp')
    return final_df

def pull_data(path,tstart, tend):
    with open(os.path.join(Path(__file__).parents[0], "config.yml"), 'r') as f:
        config = yaml.safe_load(f)

    server = SSHTunnelForwarder(
        'tb.precise.seas.upenn.edu',
        ssh_username=config['credentials']['ssh_username'],
        ssh_pkey=os.path.join(Path(__file__).parents[0], ".ssh/id_rsa"),
        remote_bind_address=('127.0.0.1', 5432)
    )

    server.start()
    print("Connected to PRECISE Thingsboard on: {}:{}".format(
        server.local_bind_address[0],
        server.local_bind_port))

    params = {
        'database': config['credentials']['database'],
        'user': config['credentials']['username'],
        'password': config['credentials']['password'],
        'host': 'localhost',
        'port': server.local_bind_port
    }

    conn = psycopg2.connect(**params)
    cursor = conn.cursor()

    print("Pulling data between: ",tstart, tend)

    #path = 'Data/'+path

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)

    print("Pulling Spec 1 Data")
    cursor.execute(
        ("select * from ts_kv where entity_id = 'b3e21af0-223a-11ec-939e-7d5fd0d48abe' AND ts>='{0}' AND ts<='{1}'").format(
            tstart, tend))
    spec1_df = DataFrame(cursor.fetchall())
    if spec1_df.empty==0:
        print(spec1_df.head(20))
        spec1_df.to_csv(path+'/spec_1.csv')

    print("Pulling Spec 2 Data")
    cursor.execute(
        ("select * from ts_kv where entity_id = '9ee57f80-223e-11ec-9769-7d5fd0d48abe' AND ts>='{0}' AND ts<='{1}'").format(
            tstart, tend))
    spec2_df = DataFrame(cursor.fetchall())
    if spec2_df.empty == 0:
        print(spec2_df.head())
        spec2_df.to_csv(path+'/spec_2.csv')

    print("Pulling Spec 3 Data")
    cursor.execute(
        ("select * from ts_kv where entity_id = '1c96e150-1270-11ec-a39b-ab9e04536e22' AND ts>='{0}' AND ts<='{1}'").format(
            tstart, tend))
    spec3_df = DataFrame(cursor.fetchall())
    if spec3_df.empty == 0:
        print(spec3_df.head())
        spec3_df.to_csv(path+'/spec_3.csv')

    print("Pulling Key Values")
    cursor.execute("select * from ts_kv_dictionary")
    key_df = DataFrame(cursor.fetchall())
    print(key_df.head())
    key_df.to_csv('Data/key_df.csv')


