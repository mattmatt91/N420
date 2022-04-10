from pathlib import Path
import os
from datetime import datetime, timedelta
my_time = lambda: datetime.now().strftime("%m_%d_%Y-%H_%M_%S")
import json as js

class Logger():
    def __init__(self, name):
        self.path =os.path.join("data" ,"logs")
        Path(self.path).mkdir(parents=True, exist_ok=True)  
        date = my_time()   
        name = f"{name}_log.txt"
        self.path = os.path.join(self.path, name)
        # with open(self.path, 'a+') as f:
            # f.write('server restarted\n')
            # print(f.readlines())

        print(self.path)

    def get_last(self):
        try:
            f = open(self.path)
            preferences = f.readlines()[-1]
            print(preferences)
            # f.close()
            # return js.loads(preferences[preferences.find('{'):])
        except:
            print(f"no file found at\033[1;33;40m {self.path}\033[0;37;40m")
            return None

    def get_path(self):
        return self.path

    def write(self, data):
        new_line = my_time() +  data + '\n'
        with open(self.path, 'a') as f:
            f.write(new_line)



if __name__ == '__main__':
    logger_data = Logger('data')
    logger_error = Logger('error')

    for i in range(100):
        try:
            logger_data.write(f'test{i}')
            n = 1/(i%10)
        except Exception as e:
            logger_error.write(repr(e))