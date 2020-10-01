import coverage
import backbone
import math
import random
random.seed(10)


X = coverage.X
nPart = 100
numNodes=backbone.ctrg
nodes=backbone.ordinary
radius=backbone.radius
E_init = backbone.E_init
particles = coverage.particles
sink_x = 200
sink_y = 200
neighbours = backbone.neighbours


fX1 = [0 for x in range(nPart)]
fX2 = [0 for x in range(nPart)]
fX3 = [0 for x in range(nPart)]

fX = [0 for x in range(nPart)]





def fx1_func():
	for ii, i in enumerate(X):
		sum_temp = 0
		sum_init = 0
		for j in range(numNodes):
			sum_temp += i[j] * nodes[j].res
			# sum_init += E_init
		fX1[ii] = 1 - (sum_temp / numNodes * E_init)


def fx2_func():
	for ii, i in enumerate(X):
		sum_f = 0
		for j in range(numNodes):
			sum_temp = 0
			tx = particles[ii].x
			ty = particles[ii].y
			for k in range(neighbours[nodes[j].ind][-1]):
				dis_ij = math.sqrt((tx - nodes[k].x) ** 2 + (ty - nodes[k].y) ** 2)
				dis_sinkj = math.sqrt((tx - sink_x) ** 2 + (ty - sink_y) ** 2)
				sum_temp += (dis_sinkj - dis_ij) ** 2
				print(dis_ij, " ", dis_sinkj)
			sum_f += math.sqrt(sum_temp / neighbours[nodes[j].ind][-1])
		fX2[ii] = sum_f



if __name__ == '__main__':
	fx1_func()
	fx2_func()
