"""
The Bandersnatch Simulation
Kevin Xie 
CS550 Healey

With the recent release of Netflix's Black Mirror Choose-Your-Own-Adventure Movie, I wanted to 
use Monte Carlo simulations to test which endings were the most common if the choices were
chosen at random. To do this, I used a class that contained all of the choices that are made
in the movie (spoiler alert!) and programmed in the style of a flow chart. At each point,
the player makes a random binary choice (sometimes, the result of the choice depends on 
past choices, which made it somewhat complicated.) and depending on the choices made, a 
specific ending is presented. My initial hypothesis was that the more choices and prerequisites
involved for an ending, the less frequently it is reached.

Sources (including Part II):
matplotlib styling - www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
matplotlib separate scales for y axes - https://matplotlib.org/examples/api/two_scales.html
label all bars in bar graph - https://stackoverflow.com/questions/26131822/how-to-display-all-label-values-in-matplotlib/
setting different colors for each bar - https://stackoverflow.com/questions/18973404/setting-different-bar-color-in-matplotlib-python
specifying layer order of graphs - https://stackoverflow.com/questions/37246941/specifying-the-order-of-matplotlib-layers
specifying when to run certain code - https://stackoverflow.com/questions/6523791/why-is-python-running-my-module-when-i-import-it-and-how-do-i-stop-it
smoothing out a curve - https://stackoverflow.com/questions/46633544/smoothing-out-curve-in-python/
divide one list by another - https://stackoverflow.com/questions/14434605/divide-one-list-by-another-list
remove certain values from a list - https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list

On my honor,
I have neither given nor received unauthorized aid.

Kevin Xie '19
"""
import random, sys
import matplotlib.pyplot as plt
# import numPy for polynomial approximation (smooth lines)
import numpy as np

# retrieve intended number of trials and create x axis
n = int(sys.argv[1])
x = [k+1 for k in range(11)]

# Bandersnatch game
class Bandersnatch:
	def __init__(self):
		self.endingcounts = [0 for i in range(11)] # counting frequency of each ending
		self.endingstepcounts = [0 for i in range(11)] # counting number of steps taken to each ending
		self.stepcount = 0 
		self.mom = False # a contingency for certain endings
		self.colinDeath = False # likewise
		self.PACS = False # likewise

	# executes story -- the first branch (each function from here is a branch of the story, usually with one binary choice)
	def run(self,n):
		for i in range(n):
			choice = random.randrange(0,2)
			self.stepcount += 1 # add stepcount every time a choice is made
			if choice == 0:
				choice2 = random.randrange(0,2)
				self.stepcount += 1
				if choice2 == 1:
					self.mom = True
				# continue to next branch -- survived first choice
				result = self.noDeal()
			# end of story
			else:
				result = 1
			# after result is retrieved from trial #n. result is recorded and step# recorded, everything is resset.
			self.endingcounts[result-1] += 1
			self.endingstepcounts[result-1] += self.stepcount
			self.mom = False
			self.colinDeath = False
			self.PACS = False
			self.stepcount = 0
		# returns the frequency count and step count for each ending
		return self.endingcounts, self.endingstepcounts
	# branch #2 --- etc. etc. (after this they are all the same -- one or two binary choices that either lead to an ending or another branch)
	def noDeal(self):
		choice = random.randrange(0,2)
		self.stepcount += 1
		if choice == 0:
			result = self.noTea()
		else:
			result = 2
		return result
	def noTea(self):
		choice = random.randrange(0,2)
		self.stepcount += 1
		if choice == 0:
			result = self.colin()
		else:
			result = self.haynes()
		return result
	def colin(self):
		choice = random.randrange(0,2)
		self.stepcount += 1
		if choice == 0:
			result = 3
		else:
			self.colinDeath = True
			result = self.haynes()
		return result
	def haynes(self):
		choice = random.randrange(0,2)
		self.stepcount +=1
		if choice == 0:
			result = self.noPills()
		else:
			result = 4
		return result
	def noPills(self):
		choice = random.randrange(0,2)
		self.stepcount +=1
		if choice == 0:
			result = self.keepComputer()
		else:
			result = 2
		return result
	def keepComputer(self):
		choice = random.randrange(0,2)
		self.stepcount +=1
		if choice == 0:
			result = self.family()
		else:
			result = self.book()
		return result
	def book(self):
		choice = random.randrange(0,2)
		self.stepcount+=1
		if choice == 0:
			result = self.family()
		else:
			# this ending/branch is contingent on certain parameters/choices player has made
			if self.mom == True and self.colinDeath == True:
				self.PACS = True
				result = self.family()
			elif self.mom == True:
				choice2 = random.randrange(0,2)
				self.stepcount+=1
				if choice2 == 1:
					result = 8
				else:
					result = self.family()
			else:
				result = self.family()
		return result
	def family(self):
		choice = random.randrange(0,2)
		self.stepcount+=1
		if choice == 0 and self.PACS == True:
			result = 5
		elif choice == 0:
			result = self.whiteBear()
		else:
			result = self.netflix()
		return result
	def whiteBear(self):
		choice = random.randrange(0,2)
		self.stepcount+=1
		if choice == 0:
			result = self.killDad()
		else:
			result = 6
		return result
	def netflix(self):
		choice = random.randrange(0,2)
		self.stepcount+=1
		if choice == 0:
			result = 9
		else:
			result = 10
		return result
	def killDad(self):
		choice = random.randrange(0,2)
		self.stepcount+=1
		if choice == 0:
			result = 11
		else:
			result = 7
		return result

# only executes if main file (module) is being executed -- https://stackoverflow.com/questions/6523791/why-is-python-running-my-module-when-i-import-it-and-how-do-i-stop-it
if __name__ == "__main__":
	# sets up a game
	trialrun = Bandersnatch()
	# runs trial for entered amount of trials and retrieves frequency counts and step count
	count, stepcount = trialrun.run(n)
	# calculates average stepcount per 1 run through for every ending (was total stepcount). Since it's a division, sometimes division by zero can occur, so simulations should have larger trial count (n)
	# -- https://stackoverflow.com/questions/14434605/divide-one-list-by-another-list
	stepcount = [int(b)/int(m) for b,m in zip(stepcount,count)]
	# varies bar chart color based on value -- https://stackoverflow.com/questions/18973404/setting-different-bar-color-in-matplotlib-python
	barcolor = [0 for i in range(11)]
	for i in range(len(count)):
		barcolor[i] = [0,1-count[i]/(max(count)*1.5),0,1]
	# generates smoother line and fits to data -- https://stackoverflow.com/questions/46633544/smoothing-out-curve-in-python/
	poly = np.polyfit(x,count,5)
	poly_y = np.poly1d(poly)(x)

	polysteps = np.polyfit(x,stepcount,5)
	polysteps_y = np.poly1d(polysteps)(x)
	"""
	STYLING SOURCES:
	www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
	https://matplotlib.org/examples/api/two_scales.html
	https://stackoverflow.com/questions/26131822/how-to-display-all-label-values-in-matplotlib/
	"""
	fig, ax1 = plt.subplots()
	ax1.plot(x, poly_y, linestyle = "--", color = [0,0,0,1]) # line of best fit
	plt.bar(x, count, color=barcolor)
	ax1.set_xlabel('ending (#)')
	ax1.set_ylabel('frequency (#)', color = [0,0.6,0,1]) # axis labels and ticks
	ax1.tick_params('y', colors = [0,0.6,0,1])
	ax1.set_xticks(np.arange(len(x)+1))

	ax2 = ax1.twinx() # creates separate y axis and scale
	ax2.plot(x,polysteps_y, linestyle = "--", color=[0,0,1,1])
	ax2.plot(x, stepcount, color = [0,0,1,0.5])
	ax2.set_ylabel('stepcount (#)', color = [0,0,1,1])
	ax2.tick_params('y', colors = [0,0,1,1])

	# removes unnecessary top of frame for aesthetic reasons
	ax1.spines["top"].set_visible(False)
	ax2.spines["top"].set_visible(False)

	# title and graph output
	plt.title("Frequency of endings in "+str(n)+" trials")
	fig.tight_layout()
	plt.show()