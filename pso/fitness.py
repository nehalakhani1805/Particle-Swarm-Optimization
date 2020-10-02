#import coverage
#import backbone
import math
import random
random.seed(10)


# X = coverage.X
# nPart = 100
# numOrdNodes=backbone.ctrg
# ordNodes=backbone.ordinary
# radius=backbone.radius
# E_init = backbone.E_init
# particles = coverage.particles
# sink_x = 200
# sink_y = 200
# neighbours = backbone.neighbours


# fX1 = [0 for x in range(nPart)]
# fX2 = [0 for x in range(nPart)]
# fX3 = [0 for x in range(nPart)]

# fX = [0 for x in range(nPart)]





def fx1_func(numOrdNodes,X,E_init,ordNodes,i):
	sum_temp=0
	fX1=0
	for j in range(numOrdNodes):
		sum_temp += X[i][j] * ordNodes[j].res
			# sum_init += E_init
	fX1 = 1 - (sum_temp / numOrdNodes * E_init)
	return fX1


def fx2_func():
	for ii, i in enumerate(X):
		sum_f = 0
		for j in range(numOrdNodes):
			sum_temp = 0
			tx = particles[ii].x
			ty = particles[ii].y
			for k in range(neighbours[ordNodes[j].ind][-1]):
				dis_ij = math.sqrt((tx - ordNodes[k].x) ** 2 + (ty - ordNodes[k].y) ** 2)
				dis_sinkj = math.sqrt((tx - sink_x) ** 2 + (ty - sink_y) ** 2)
				sum_temp += (dis_sinkj - dis_ij) ** 2
				print(dis_ij, " ", dis_sinkj)
			sum_f += math.sqrt(sum_temp / neighbours[ordNodes[j].ind][-1])
		fX2[ii] = sum_f



if __name__ == '__main__':
	fx1_func(numOrdNodes,X,E_init,ordNodes,i)
	fx2_func()
