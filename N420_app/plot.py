
from time import time
import pandas as pd
import numpy as np
import json as js
from os.path import join
from datetime import datetime, timedelta
import plotly
import plotly.express as px


class Plot():
    path_data = join('data','logs','data_log.txt')

    def __init__(self):
        pass

    @classmethod   
    def get_data(cls, options):
        print('start reading')
        mytime = time()
        options['date'] = 'on'
        days = int(options.pop('days'))  
        with open(cls.path_data, 'r') as f:
            data =[js.loads(i[i.find('{'): i.rfind('}')+1]) for i in f.readlines()]

            df = pd.DataFrame(data)

            thisData = df.iloc[:][[i for i in options]] 

            thisData['date'] = [datetime.strptime(i, '%m/%d/%Y %H:%M:%S') for i in thisData['date']]

            thisData = thisData[thisData['date']>= datetime.now()-timedelta(days=days)]

            
            # thisData.set_index('date', inplace=True)
            return(thisData)

    @classmethod
    def get_plot(cls, options):
        print('building plot ')   
        mytime = time()
        data = cls.get_data(options)
        # fig = px.line(data)
        # print('plot builded in ', time()-mytime, 'seconds')   
        # mytime = time()
        # graphJSON = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        # print('convert to js ', time()-mytime, 'seconds')   
        # mytime = time()
        # print('plot generated')
        #print(data.to_json())
        return data.to_json() # graphJSON
        



if __name__ == '__main__':
    path  =join('data','logs','data_log.txt')
    options = {'temp': 'on', 'soil1': 'on', 'days': '1'}
    Plot.get_plot(options)