
from datetime import datetime


from datetime import datetime, timedelta
stringIn = '2022-04-18 13:06:03'

dt = datetime.strptime(stringIn, '%Y-%m-%d %H:%M:%S')
print(type(stringIn))
print(type(dt))
ts = dt.timestamp()
print(ts)
print(datetime.fromtimestamp(ts).strftime("%A, %B %d, %Y %I:%M:%S"))