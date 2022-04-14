
import time
from datetime import datetime
curr_time = time.ctime()
print(curr_time)
curr_time = curr_time.split()[3]

print('time :',type(curr_time))

t = datetime.now()
print(t)
print(t.day)

# time.sleep(3)

t1 = datetime.now()
print(t1)

t2 = t1-t
print(t2.seconds)


print(t.isoformat()[0:11], type(t.isoformat()))

s = 'Average 😐'
print(s[0:-2])
