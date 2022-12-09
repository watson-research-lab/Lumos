

import datetime
import time

import pandas as pd

from Spectral_Response_of_Medium.Data.pull_data import pull_data, process_df

if __name__ == '__main__':

    path = "Spectral_Response_of_Medium/Data/test"
    print('Pulling Data....')
    tstart = int(time.mktime(datetime.datetime(2022, 8, 12, 16, 6).timetuple()) * 1000)
    tend = int(time.mktime(datetime.datetime(2022, 8, 12, 16, 8).timetuple()) * 1000)
    print(tstart)
    pull_data(path,tstart,tend)

    led_df = pd.read_csv("Spectral_Response_of_Medium/Data/test/spec_1.csv", usecols = ['1', '2', '5'])
    print(process_df(led_df).head(20))

    print('---------------------Done!---------------------')


