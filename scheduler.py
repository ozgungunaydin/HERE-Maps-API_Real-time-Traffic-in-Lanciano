import os
from datetime import datetime, timedelta
from pytz import timezone
import time

def realtime_traffic_lanciano():
    os.system('path_to_your_script.py')
# ____________________________________________________________________________________________________________

# ALTERNATIVE 1:
# this method has the highest accuracy between all alternatives.
# i set a daily basic task in Windows Task Scheduler with the following arguments:
# program script: "C:\Program Files\Python37\python.exe", add arguments: my script's path like C:\Files\script.py
# under 'triggers' menu: start at a given time, select 'repeat task every 5 minutes',
# 'stop all running tast at the end of repetition duration', expire at a given time
# under 'conditions' menu: uncheck 'start the task only if the computer is on AC power'

realtime_traffic_lanciano()
# ____________________________________________________________________________________________________________

# # ALTERNATIVE 2:
# # this method is only useful if time delay of about 0.2 - 0.4 seconds is not important when extracting data
# # it should be noted that it is rather more sensitive than ALTERNATIVE 2,
# # however still not as sensitive as ALTERNATIVE 1

# # this project is supposed to start at 07:00
# start_time = 7
# # this project is supposed to end at 22:00
# end_time = 22
# # difference between the given times
# difference = end_time - start_time
# # i want to extract data every 5 minutes
# repeat_pattern = 5
# # thus, the function needs to be be run 'necessary_count' times
# necessary_count = difference * repeat_pattern

# # first count is zero
# count = 0

# while True:
# 	# each loop increases the count by 1
# 	count = count + 1
# 	# until the count exceeds 'necessary_count'
# 	if count <= necessary_count:
# 		# time_now variable is set to the current time in Rome/Italy
# 		time_now = datetime.now(timezone('Europe/Rome'))
# 		# print local time in Rome/Italy
# 		print(time_now)
# 		# print updated count
# 		print(count)

#  		# run the function
# 		realtime_traffic_lanciano()
	
# 		# schedule next time to run the function to 5 mins later
# 		time_scheduled = timedelta(minutes=5) + time_now

# 	# if the scheduled time still has not arrived
# 	while datetime.now(timezone('Europe/Rome')) < time_scheduled:
# 		# wait for another second
# 	  	time.sleep(1)
# ____________________________________________________________________________________________________________

# # ALTERNATIVE 3:
# # this method is only useful if time delay is not important when extracting data

# # this project is supposed to start at 07:00
# start_time = 7
# # this project is supposed to end at 22:00
# end_time = 22
# # difference between the given times
# difference = end_time - start_time
# # i want to extract data every 5 minutes
# repeat_pattern = 5
# # thus, the function needs to be be run 'necessary_count' times
# necessary_count = difference * repeat_pattern

# # first count is zero
# count = 0

# while True:
# 	# each loop increases the count by 1
# 	count = count + 1
# 	# until the count exceeds 'necessary_count'
# 	if count <= necessary_count:
# 		# run the function
# 		realtime_traffic_lanciano()
# 		# print local time in Rome/Italy
# 		print(datetime.now(timezone('Europe/Rome')))
# 		# print updated count
# 		print(count)
# 		# to make the loop sleep for a while,
# 		# i need to convert 5 mins to seconds: 5min x 60sec = 300sec,
# 		# since i noticed a pattern of about 5 seconds delay, i subtract it from the sleep time
# 		# but remember that this is not suggested if delays in extraction is important
# 		time.sleep(300 - 5)
# 	else:
# 		# if the count exceeds 'necessary_count', break the loop
# 		break