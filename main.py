

import datetime
import time
from Data.pull_data import pull_data

if __name__ == '__main__':

    path = "Data/IMWUT_Data/ON_OFF"
    print('Pulling Data....')
    tstart = int(time.mktime(datetime.datetime(2022, 8, 11, 0, 8).timetuple()) * 1000)
    tend = int(time.mktime(datetime.datetime(2022, 8, 11, 0, 12).timetuple()) * 1000)
    print(tstart)
    pull_data(path,tstart,tend)

    print('---------------------Done!---------------------')





