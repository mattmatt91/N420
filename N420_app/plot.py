from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import json as js
from os.path import join
from datetime import datetime, timedelta


class Plot():
    def __init__(self, path_data):
        self.path_data = path_data
        self.plot = None
        
    def get_data(self, options):
        with open(self.path_data, 'r') as f:
            data =[js.loads(i[i.find('{'): i.rfind('}')+1]) for i in f.readlines()]
            df = pd.DataFrame(data)
            days = int(options.pop('days'))  
            options['date'] = 'on'
           
            thisData = df.iloc[:][[i for i in options]] 
            thisData['date'] = [datetime.strptime(i, '%m/%d/%Y %H:%M:%S') for i in thisData['date']]
            thisData = thisData[thisData['date']>= datetime.now()-timedelta(days=days)]
            thisData.set_index('date', inplace=True)
            print(thisData)
            return(thisData)

    def gen_plot(self, options):
        data = self.get_data(options)
        # Create figure with secondary y-axis
        fig, ax = plt.subplots()
        fig.subplots_adjust(right=0.75)
        twins = []
        for i in range(len(data.columns)-1):
            twins.append(ax.twinx())


        # Offset the right spine of twin2.  The ticks and label have already been
        # placed on the right by twinx above.
        twin2.spines.right.set_position(("axes", 1.2))

        p1, = ax.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")
        for twin in twins:
            p2, = twin1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature")
        p3, = twin2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")

        ax.set_xlim(0, 2)
        ax.set_ylim(0, 2)
        for twin in twins:
            twin.set_ylim(0, 4)


        ax.set_xlabel("Distance")
        ax.set_ylabel("Density")
        for twin in twins:
            twin.set_ylabel("Temperature")


        ax.yaxis.label.set_color(p1.get_color())
        for twin in twins:
            twin.yaxis.label.set_color(p2.get_color())
       

        tkw = dict(size=4, width=1.5)
        ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
        for twin in twins:
            twin.tick_params(axis='y', colors=p2.get_color(), **tkw)
       
        ax.tick_params(axis='x', **tkw)

        ax.legend(handles=[p1, p2, p3])

        plt.show()

    def get_plot(self, options):
        return self.plot

if __name__ == '__main__':
    path  =join('data','logs','data_log.txt')
    options = {'temp': 'on', 'soil1': 'on', 'days': '1'}
    plot = Plot(path)
    plot.gen_plot(options)