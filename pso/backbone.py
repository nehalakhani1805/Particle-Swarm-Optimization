import random
import math
import operator
import  collections
class node:
	def __init__(self, x, y):
		self.ind = 0
		self.x = x
		self.y = y
		self.res = 50
		self.q = 30 # random Q
		self.weight = 0


radius = 10
nPart = 500


nodes = []

neighbours = [[] for x in range (0, nPart)]
E_tx_arr = [[] for x in range (0, nPart)]
# costs = [1.0 for x in range(nPart)]
costs = []

wt_T = [1.0 for x in range(nPart)]

N = 3 # Backnode black

E_init = 2
Efs = 10 #PJ/bit/m2
k = 1000 #bits
EDA = 5 #nJ/bit/signal
Eelec = 50 #nJ/bit
Eamp = 0.0013 #PJ/bit/m4
d0 = 90 #m
n = 300
α = 0.35
β = 0.45
δ = 0.2
wmin = 0.4


w1 = 0.3
w2 = 0.4
w3 = 0.3 # w for Backbone

nMax = 0 #neighbour max
cMax = 0 #cost max


for i in range(nPart):
	x = random.randint(0, 100)
	y = random.randint(0, 100)
	n = node(x, y)
	n.ind = i
	nodes.append(n)

for i in range(nPart):
	count = 0
	for j in range(nPart):
		if i != j:
			if ((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2 < radius ** 2):
				count += 1
				neighbours[i].append(nodes[j])
	neighbours[i].append(count)
	if count > nMax:
		nMax = count


def costPart(i,cMax, neighbours, E_tx_arr):
	xi = nodes[i].x
	yi = nodes[i].y
	cost = 0
	for j in range(len(neighbours[i]) - 1):
		eTemp = Eelec + Efs * ((xi - neighbours[i][j].x) ** 2 + (yi - neighbours[i][j].y) ** 2)
		E_tx_arr[i].append(eTemp)
		num = eTemp * E_init
		denom = nodes[i].q * neighbours[i][j].res
		cost += math.sqrt(num / denom)
	costs.append(cost)
	if cMax < cost:
		cMax = cost
	return cost

def weight(i, neighbours, costs):
	# print(costs[i], ' ', nMax
	if costs[i] != 0:
		T_temp = w1 * nodes[i].res / E_init + w2 * neighbours[i][-1] / nMax + w3 * cMax / costs[i]
	else:
		T_temp = 0
	nodes[i].weight = T_temp
	wt_T[i] = T_temp
	return T_temp



# avg = 0
# for i in range(nPart):
# 	avg += neighbours[i][-1]

# print(avg / nPart)


def initNodes(nPart, nodes, neighbours, E_tx_arr):
	for i in range(nPart):
		costPart(i, cMax, neighbours, E_tx_arr) # cost(i) initialization
	for i in range(nPart):
		weight(i, neighbours, costs)


initNodes(nPart, nodes, neighbours, E_tx_arr)

# for i in range(nPart):
# 	print(wt_T[i])


col = [0 for x in range(nPart)]
# 0 -> WHITE
# 1 -> BLACK
# 2 -> GREY



def step1(nPart, nodes, wt_T):
	ind = 0
	maxWt = 0
	for i in range(nPart):
		if wt_T[i] > maxWt:
			ind = i
			maxWt = wt_T[i]
	col[ind] = 1
	return ind



# for i in neighbours[0][:-1]:
# 	print(i.weight)


# nl = sorted(neighbours[0][:-1], key = operator.attrgetter("weight"), reverse = True)

# print("/n")
# for i in nl:
# 	print(i.weight)





queue = collections.deque()
def step2(nPart, nodes, neighbours, stInd):
	ctr2 = 0
	ctr = 0
	# stInd = step1(nPart, nodes, wt_T)
	queue.append(nodes[stInd])
	while(len(queue) != 0):
		nl = sorted(neighbours[queue[0].ind][:-1], key = operator.attrgetter("weight"), reverse = True)
		nl.append(neighbours[queue[0].ind][-1])
		for i in neighbours[queue[0].ind][:-1]:
			print("neigh ", queue[0].ind, " ",i.ind)
		print("")
		# print(i.ind for i in neighbours[queue[0].ind])
		neighbours[queue[0].ind] = nl
		for i in neighbours[queue[0].ind][:-1]:
			print("neigh ", queue[0].ind, " ",i.ind)
		# print(i.ind for i in neighbours[queue[0].ind])
		nTemp = N
		for i in range(len(neighbours[queue[0].ind]) - 1):
			if col[neighbours[queue[0].ind][i].ind] == 0:
				if nTemp > 0:
					ctr += 1
					col[neighbours[queue[0].ind][i].ind] = 1
					queue.append(neighbours[queue[0].ind][i])
					print("i", neighbours[queue[0].ind][i].ind)
					nTemp -= 1
				else:
					ctr2 += 1
					col[neighbours[queue[0].ind][i].ind] = 2
		queue.popleft()
		# print(queue)
	print(ctr)
	print(ctr2)
	print(nPart - ctr)


# step2(nPart, nodes, neighbours)






	# nl = sorted(neighbours[stInd][:-1], key = operator.attrgetter("weight"), reverse = True)
	# nl.append(neighbours[stInd][-1])
	# neighbours[stInd] = nl
	# for i in range(len(neighbours[stInd] - 1)):
	# 	if i < N:
	# 		col[neighbours[stInd][i].ind] = 1
	# 	else:
	# 		col[neighbours[stInd][i].ind] = 2


def step3(nPart, nodes, neighbours):
	stInd = step1(nPart, nodes, wt_T)
	step2(nPart, nodes, neighbours, stInd)
	for i in range(nPart):
		if col[i] == 0:
			step2(nPart, nodes, neighbours, i)
	for i in range(nPart):
		if col[i] == 1:
			flag = False
			for j in range(neighbours[i][-1] - 1):
				if neighbours[i][j] != 1:
					flag = True
			if(not flag):
				col[i] = 2



ctr = 0
step3(nPart, nodes, neighbours)
for i in range(nPart):
	if col[i] == 1:
		print("blac",i)
		ctr += 1
	if col[i] == 0:
		print("whit",i)
print(ctr)
