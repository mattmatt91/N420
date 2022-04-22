
from time import strftime, time
import pandas as pd
import numpy as np
import json as js
from os.path import join
from datetime import datetime, timedelta
import plotly
import plotly.express as px


class Plot():
    path_data = join('data','logs','data_log.txt')
    options = ['date', 'temp', 'hum', 'pres', 'soil1', 'soil2', 'lamp_phase',
                        'lamp_state', 
                        'irrigation_interval', 'irrigation_duration',
                        'soil_moist_hyst_min', 'soil_moist_hyst_max', 'pot1_dry',
                        'pot2_dry',
                        'temp_hyst_min', 'temp_hyst_max', 'hum_hyst_min', 'hum_hyst_max',
                        'fan_state', 'cpu_temp', 'air_quality']

    def __init__(self):
        pass

    @classmethod   
    def get_data(cls, options):
        days = int(options['days'])
        with open(cls.path_data, 'r') as f:
            data =[js.loads(i[i.find('{'): i.rfind('}')+1]) for i in f.readlines()]
            df = pd.DataFrame(data) 
            thisData = df.iloc[:][[i for i in cls.options]] 
            thisData['date_secs'] = [int(datetime.strptime(i, '%m/%d/%Y %H:%M:%S').timestamp()) for i in thisData['date']]
            thisData['dt'] = [datetime.strptime(i, '%m/%d/%Y %H:%M:%S') for i in thisData['date']]
            thisTimedelta = pd.Timestamp(datetime.now()-timedelta(days=days))
            thisData = thisData[thisData['dt']>= thisTimedelta]
            thisData.pop('dt')
            thisData.pop('date')
            return(thisData)


    @classmethod
    def get_plot(cls, options):
        print('building plot ')   
        data = cls.get_data(options)
        return data.to_json() # graphJSON
        

if __name__ == '__main__':
    path  =join('data','logs','data_log.txt')
    options = {'temp': 'on', 'soil1': 'on', 'days': '4'}
    Plot.get_plot(options)