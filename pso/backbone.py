#Importing all required libraries
import random
import math
import operator
import  collections

#This is used to generate the same random values always
random.seed(10)

#Making an class node
class node:
	def __init__(self, x, y):
		#All the attributes of Node Class
		self.ind = 0	#Node index
		self.x = x    #x co-ordinate
		self.y = y    #y co-ordinate
		self.res = 30	#Residual Energy
		self.q = random.randint(10,20) 	# random Q
		self.weight = 0		#T(i)
		self.indg= 0		#Index of grey node(if it is grey)
		self.alive = True	#Node alive or dead
		self.ordInd = -1	#index of ordNodes nodes(if ordNodes node)
		self.einit = 30   #initial energy of the node


radius = 45	#radius of each node
numNodes = 300	# Total Number of nodes present
 
costs = []	# list to store the cost used in T(i)

#initial list to store the values of T(i)
wt_T = [1.0 for x in range(numNodes)]

N = 2 # Backnode black(number of nodes from neighbours to be selected as black)


#Initialization of constants
E_init = 2  
Efs = 10 * 1e-12 #Pico Joule/bit/m2
k = 1000 #bits
EDA = 5 * 1e-9 #nJ/bit/signal
Eelec = 50 * 1e-9 #nJ/bit
Eamp = 0.0013 * 1e-12 #PJ/bit/m4
d0 = 90 #m


#Initialization of constants
# E_init = 30
# Efs = 10 #PJ/bit/m2
# k = 1000 #bits
# EDA = 5 #nJ/bit/signal
# Eelec = 50 #nJ/bit
# Eamp = 0.0013 #PJ/bit/m4
# d0 = 90 #m


#fitness function constants
alpha = 0.35
beta = 0.45
gamma = 0.2
wmin = 0.4


#Initialization of weights used for calculating T(i)
w1 = 0.3
w2 = 0.4
w3 = 0.3


cMax = 0 #cost max


#intialisationof all nodes
def initNodes_rand(nodes,numNodes):
	for i in range(numNodes):
		#Generating random co-ordinates for Nodes
		x = random.randint(0, 400)
		y = random.randint(0, 400)
		#making objects of Node Class
		n = node(x, y)
		n.ind = i 	#index of node
		nodes.append(n)		#adding the node to a list
	#returning a list with all nodes initialised
	return nodes


#Assigning neighbours of all the nodes
def initNeighbours(nodes,numNodes,neighbours,nMax):
	for i in range(numNodes):
		#counting number of neighbour for every node
		count = 0
		for j in range(numNodes):
			#if the index of both nodes are different
			if i != j:
				#if the nodes are overlapping(are close enough)
				if ((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2 < radius ** 2):
					count += 1
					#adding that node as a neighbour
					neighbours[i].append(nodes[j])
		#last index of node stores the count(number of neighbour of that node)
		neighbours[i].append(count)
		#nMax is maximum number of neighbour among all nodes
		if count > nMax:
			nMax = count
	return neighbours,nMax

#Calculating cost requied for T(i)
def costPart(i,cMax, neighbours, E_tx_arr):
	#co-ordinates of nodes
	xi = nodes[i].x
	yi = nodes[i].y
	cost = 0	#initial cost
	for j in range(len(neighbours[i]) - 1):		#len -1 as last index is not a node(it's the count of no. of neighbours)\
		#using the formula given in the paper
		#calculating the cost

		#Calculating ETx(i) and adding it to list
		#𝐸𝑇𝑥(𝑖) denotes the energy cost of node 𝑖 in transmitting one bit of message
		eTemp = Eelec + Efs * ((xi - neighbours[i][j].x) ** 2 + (yi - neighbours[i][j].y) ** 2)
		E_tx_arr[i].append(eTemp)

		num = eTemp * E_init	#E_init->inital enerygy|numerator of cost formula
		denom = nodes[i].q * neighbours[i][j].res   #denominator of cost formula
		cost += math.sqrt(num / denom)	#calculaing cost
	
	costs.append(cost)	#adding cost to a list
	#calculating maximum cost
	if cMax < cost:
		cMax = cost
	return cost

#Calculating T(I)
def weight(i, neighbours, costs):
	if costs[i] != 0:	#if cost is not 0
		#Calculating T(i) for the node
		T_temp = w1 * nodes[i].res / E_init + w2 * neighbours[i][-1] / nMax + w3 * cMax / costs[i]
	else:
		T_temp = 0
	#adding T(i) value to its node
	nodes[i].weight = T_temp
	#Also adding it to an list which has all values of T(i)
	wt_T[i] = T_temp
	return T_temp

#Merging and Calculation of T(i) and Cost
def initNodes(numNodes, nodes, neighbours, E_tx_arr):
	for i in range(numNodes):	#for every node
		costPart(i, cMax, neighbours, E_tx_arr) 	# cost(i) initialization
	for i in range(numNodes):	#for every node
		weight(i, neighbours, costs)	#calculating T(i) using cost

#initial colour assigned to each node
col = [0 for x in range(numNodes)]
# 0 -> WHITE
# 1 -> BLACK
# 2 -> GREY


#FORMATION OF BACKBONE

#STEP 1 of Backbone Formation
#used in STEP 2 for getting the start index for backbone nodes
def step1(numNodes, nodes, wt_T):
	ind = 0		#index of black nodes
	maxWt = 0	#Storing the Maximum T(i) 
	for i in range(numNodes):	#for every value of T(i)	
		#calculating the maximum T(i)
		if wt_T[i] > maxWt:
			ind = i   #storing index for black nodes
			maxWt = wt_T[i]		
	#assigning black colour for that index
	col[ind] = 1
	return ind


#STEP 2 of Backbone Formation
def step2(numNodes, nodes, neighbours, stInd):
	queue = collections.deque()		#queue stores all the black nodes
	ctr2 = 0	#count of number of grtey nodes
	ctr = 0		#count of number of black nodes

	queue.append(nodes[stInd])	#adding the 1st node as black node(we get this value from STEP 1)
	while(len(queue) != 0):		#till all the nodes are not coloured black or grey
		
		#sorting the neighbours of the black node according to it's T(i) value
		nl = sorted(neighbours[queue[0].ind][:-1], key = operator.attrgetter("weight"), reverse = True)
		nl.append(neighbours[queue[0].ind][-1])		#adding the neighbour with maximum T(i) in the list

		#storing the neighbours of the black node
		neighbours[queue[0].ind] = nl

		#N is the number of nodes from neighbours that must be selected as black| Others are marked as grey
		nTemp = N
		
		#for the 1st element of the queue(black nodes list)
		for i in range(len(neighbours[queue[0].ind]) - 1):
			if col[neighbours[queue[0].ind][i].ind] == 0:	#if the neighbour of that node is white
				if nTemp > 0:	#for the first nTemp elements assign it as black 
					ctr += 1	#increasing count of black nodes
					col[neighbours[queue[0].ind][i].ind] = 1	#assigning the color as that index as black
					queue.append(neighbours[queue[0].ind][i])	#adding the new black node formed in the queue
					nTemp -= 1	#decreasing the count of nTemp
				else:	#for the remaining elements mark it as grey
					#counting and assigning of GREY nodes
					ctr2 += 1
					col[neighbours[queue[0].ind][i].ind] = 2
		#removing the black node which was just used from the queue
		queue.popleft()

#STEP 1 of Backbone Formation
def step3(numNodes, nodes, neighbours):

	stInd = step1(numNodes, nodes, wt_T)	#getiing the start index from STEP 1
	step2(numNodes, nodes, neighbours, stInd)	#performing STEP 2 using the start index
	for i in range(numNodes):	#for all Nodes
		if col[i] == 0:		#if color is WHITE
			step2(numNodes, nodes, neighbours, i)	#Performing STEP 2
	for i in range(numNodes):	#for all nodes
		if col[i] == 1:		#if color is BLACK
			flag = False	#making flag as False
			for j in range(neighbours[i][-1] - 1):	#in all the neighbours of the specific node
				if col[neighbours[i][j].ind] != 1:	#
					flag = True
			if(not flag):
				col[i] = 2	#color assigned as GREY

#BACKBONE 2

#checking if any backbone node is dead
def check(backbone_nodes):
	for i in backbone_nodes:	#for all backbone nodes
		if i.res==0:	#if the residual energy is 0
			return i.ind 	#return the index
	#returns -1 if no backbone node found with energy as 0(i.e all nodes are alive)
	return -1


ordNodes=[]		#initalise list for ordinary nodes(used in backbone repair)
backbone_nodes=[]	#initalise list for backbone nodes
ctr=0	#count of BLACK nodes
ctrg=0	#count of GREY nodes


def testing_b2(numNodes, nodes, backbone_nodes, neighbours,ordNodes):
	global ctr 		#count of BLACK nodes
	global ctrg 	#count of GREY nodes
	for i in range(numNodes):	#for every Node
		if col[i] == 1:		#if the color is BLACK
			backbone_nodes.append(nodes[i])	#Adding it to backbone node list
			# nodes[i].res+=30
			# nodes[i].einit+=30	
			ctr += 1	#increment of count of BLACK nodes

		else:	#else if the node is GREY
			nodes[i].ordInd = ctrg	#assigning the nodes as Ordinary node and giving its index
			ordNodes.append(nodes[i])	#adding that node in ordinary nodes(all GREY nodes)
			ctrg+=1		#incrementing the count of GREY nodes


#assigning the nodes head
def assign_head(backbone_nodes, ordNodes):
	diction={}	#dictionary(hash map) that stores the cluster head of all ordinary nodes
	for i in range(len(ordNodes)):	#for all the ordinary nodes(Grey Nodes)
		mini=math.inf 	#initialize minimum as infinity
		for j in range(len(backbone_nodes)):	#for all the backbone nodes
			temp=(ordNodes[i].x - backbone_nodes[j].x) ** 2 + (ordNodes[i].y - backbone_nodes[j].y)**2	#calculating the distance between ordinary(grey) and backbone(black) nodes
			
			if (temp< mini):	#checking if distance is minimum
				mini=temp 		#assigning the minimum distance
				minnode=backbone_nodes[j]	#assigning that backbone node as the closest node
		diction[ordNodes[i]]=minnode	#for that ordinary node, storing its best cluster head
	return diction		#returning diction

#This is the main function
if __name__ != '__main__':
	nodes=[]	#initalise nodes llst(this contains all the nodes)
	neighbours = [[] for x in range (0, numNodes)]	#initalise neighbours for all nodes 
	nMax=0	#initialisation of nMax -> maximum number of neighbour among all nodes
	E_tx_arr = [[] for x in range (0, numNodes)] 
	nodes=initNodes_rand(nodes,numNodes)	#calling the initisation of nodes function
	neighbours,nMax=initNeighbours(nodes,numNodes,neighbours,nMax)	#callint the assigning of neighbours function
	initNodes(numNodes, nodes, neighbours, E_tx_arr)	#Initialisation of T(i) of all nodes
	step3(numNodes, nodes, neighbours)	#Calling STEP 3 for backbone formation| After this function the backbone nodes will be created
	testing_b2(numNodes, nodes, backbone_nodes, neighbours,ordNodes)	#calling the function which adds the Black and Grey node in lists
