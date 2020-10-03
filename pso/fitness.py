import math
import random
from shapely.geometry import * #shapely is a library to find union of two overlapping areas
random.seed(10)


# fitness function f1 to check for residual energy
def fx1_func(numOrdNodes,X,E_init,ordNodes,i): 
	# 
	sum_temp = 0 #temporary sum variable
	fX1 = 0      #value to return 
	for j in range(numOrdNodes): #traverse through ordinary nodes
		sum_temp += X[i][j] * ordNodes[j].res #sum of residual energy of alive ordinary nodes
	fX1 = 1 - (sum_temp / numOrdNodes * E_init)	#subtract the sum_temp value from 1 to make fX1 a minimization function
	return fX1 

# fitness function f2 to check for centered degree
def fx2_func(numOrdNodes,X,ordNodes,particles,neighbours,sink_x,sink_y,nPart):
	fx2_temp=[]						#list to store normalised values of fX2
	fX2 = [0 for x in range(nPart)] #list to store actual values of fX2
	for ii, i in enumerate(X):      #traverse through X
		sum_f = 0
		for j in range(numOrdNodes): #traverse through ordinary nodes
			sum_temp = 0
			tx = particles[ii].x	#store the x coordinate of the particle in tx
			ty = particles[ii].y	#store the y coordinate of the particle in ty
			for k in range(neighbours[ordNodes[j].ind][-1]):	# traverse through the neighbours of 
				dis_ij = math.sqrt((tx - ordNodes[k].x) ** 2 + (ty - ordNodes[k].y) ** 2) #distance between sensor node and it's neighbour
				dis_sinkj = math.sqrt((tx - sink_x) ** 2 + (ty - sink_y) ** 2) #distance between sensor node and sink node
				sum_temp += (dis_sinkj - dis_ij) ** 2 # square of difference between the two distances is added to sum
			sum_f += math.sqrt(sum_temp / neighbours[ordNodes[j].ind][-1])  #this sum divided by the total number of neighbours is added to final sum
		fX2[ii] = sum_f # this value is the value of the fitness function
	fx2_temp = [float(i)/sum(fX2) for i in fX2] # normalisation of the fitness function fX2
	return fx2_temp

#fitness function f3 to measure redundant area of overlap
def fx3_func(numOrdNodes,X,radius,ordNodes,i):
	fx3 = 0		
	sum_f = 0
	dummy1 = Point(0, 0).buffer(0)	#dummy point of radius zero
	dummy2 = Point(0, 0).buffer(0)	#dummy point of radius zero
	union_area = dummy1.union(dummy2)	#dummy1 and dummy2 used to initialize union_area
	for j in range(numOrdNodes):	#traverse through ordinary nodes
		if(X[i][j] == 1):			#if node is awake
			sum_f += 3.14 * (radius ** 2)	# add the area to sum_f
			a = Point(ordNodes[j].x, ordNodes[j].y).buffer(radius) #area of ordinary sensor node
			union_area = union_area.union(a) #union of that sensor node with the current union
	try:
		fx3 = sum_f / union_area.area # dividing summation with union
	except:
		fx3 = 0		# error on division by 0 i.e when union area is zero (doesn't enter the for loop)
	return fx3


