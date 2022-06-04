# import time
from datetime import datetime

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

t1 = datetime.fromtimestamp(1481538180).strftime("%A, %B %d, %Y %H:%M:%S")
t2 = datetime.fromtimestamp(1481540160).strftime("%A, %B %d, %Y %H:%M:%S")

t3 = datetime.today()
t4 = datetime.today().strftime("%H:%M:%S")
t5 = get_sec(datetime.fromtimestamp(1481538180).strftime("%H:%M:%S"))

print(t1)
print(t2)
print(str(t3).split(" ")[0])
print(t4)
print(t5)