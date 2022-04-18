from pathlib import Path
import os
from datetime import datetime, timedelta
my_time = lambda: datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
import json as js

class Logger():
    def __init__(self, name):
        self.path =os.path.join("data" ,"logs")
        Path(self.path).mkdir(parents=True, exist_ok=True)    
        name = f"{name}_log.txt"
        self.path = os.path.join(self.path, name)
        with open(self.path, 'a') as f:
            pass
        print(self.path)


    def get_path(self):
        return self.path

    def write(self, data):
        new_line = my_time() +  data + '\n'
        with open(self.path, 'a') as f:
            f.write(new_line)

class Preferences():
    def __init__(self):
            self.path =os.path.join("data" ,"logs")
            Path(self.path).mkdir(parents=True, exist_ok=True)  
            self.path =os.path.join(self.path, "preferemces.json")
            with open(self.path) as json_file:
                self.data = js.load(json_file)


    def get_data(self):

            return self.data

    def write(self, data):
        for i in data:
            print(i, data[i])
            self.data[i] = data[i]
        with open(self.path, 'w') as outfile:
            js.dump(self.data, outfile)



if __name__ == '__main__':
    preferences = Preferences()
    data = {'2':2}
    print(preferences.get_data())
    preferences.write(data)
    print(preferences.get_data())
    exit()

    logger_data = Logger('data')
    print(logger_data.get_last())
    logger_error = Logger('error')

    for i in range(100):
        try:
            logger_data.write(f'test{i}')
            n = 1/(i%10)
        except Exception as e:
            logger_error.write(repr(e))