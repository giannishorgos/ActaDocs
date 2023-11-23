from random import random

def pit_uniform_distribution():
  pii = 21600 # Periodic Time Interval That CPE communicates. ex: 21600 s = 6 h every 6 hours
  pii_start_time_seconds = 0 # shift the start time
  pii_time_window_seconds = 6 * pii # PII is 6 hours or 21600 seconds
  random_seconds = int(random() * (pii_time_window_seconds + 1)) # random numbers in order to achive uniform distribution.
                                                                 # MAX value: 6 * (pii + 1), MIN value: 0
  start_time = pii_start_time_seconds + random_seconds

  hours = '%02d' % ((start_time // pii % 24) + 4)  
  minutes = '%02d' % (start_time // 60 % 60) 
  seconds = '%02d' % (start_time % 60) 
  periodic_inform_time = ({'hours':hours}, {'minute' : minutes}, {'seconds':seconds})
  return periodic_inform_time

pit = []
for i in range(10):
  pit.append(pit_uniform_distribution())
pit
