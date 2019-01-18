"""
The Bandersnatch Simulation Part II
Kevin Xie 
CS550 Healey

Using the same class as in Part I, I calculate the most frequent number of outcomes users
will find before giving up (a trial number range between 1 and a given maximum). Some users
may only try once and be satisfied by one ending, some may go up to 10 or 100 times. I wanted
to see how these variables changed how many outcomes users discovered.

COMPREHENSIVE SOURCES CAN BE FOUND IN PART I

On my honor,
I have neither given nor received unauthorized aid.

Kevin Xie '19

"""
from datasim import *
import random, sys
import matplotlib.pyplot as plt

# sets number of trials (n) and maximum retention rate (limit) based on user input and sets x axis and base frewuency for later
n = int(sys.argv[1])
limit = int(sys.argv[2])
x = [k+1 for k in range(11)]
count = [0 for i in range(11)]

# repeats for n
for i in range(n):
	# selects a random retention rate for each user with a maximum of "limit", starts a Bandersnatch session with that many trials
	t = random.randrange(1,limit)
	trial = Bandersnatch()
	results = trial.run(t)[0] # records results
	results[:] = (value for value in results if value != 0) # filters zero values -- https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
	uniques = len(results) # uses list without 0 results to find how many endings were discovered
	# COUNTS HOW MANY ENDINGS DISCOVERED AND ADDS TO FREQUENCY
	count[uniques-1] += 1

# bar graph color changes with value -- https://stackoverflow.com/questions/18973404/setting-different-bar-color-in-matplotlib-python
barcolor = [0 for i in range(11)]
for i in range(len(count)):
	barcolor[i] = [1-count[i]/(max(count)*1.5),0,0,1]
"""
STYLING SOURCES (in addition to in part I)
https://stackoverflow.com/questions/37246941/specifying-the-order-of-matplotlib-layers
"""
fig, ax1 = plt.subplots()
# makes sure that all endings are labeled on x-axis
ax1.set_xticks(np.arange(len(x)+1))
# removes some extraneous frame lines
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.plot(x, count, linestyle = "--", color = [0,0,0,1])
# adds guide for ease of viewing
for y in range(50,max(count),50):
	ax1.plot(range(1,12),[y for i in range(11)],"--", lw=0.5, zorder=0,color=[0,0,0,0.3])
plt.title("# endings " +str(n)+ " viewers found with a maximum retention rate of "+str(limit))
plt.bar(x,count,color=barcolor)
plt.show()