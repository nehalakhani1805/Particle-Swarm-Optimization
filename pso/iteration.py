import coverage
import numpy as np
import fitness
import random

print("Inside iter")
numNodes=coverage.backbone.numNodes
nodes=coverage.backbone.nodes
neighbours=coverage.backbone.neighbours
nPart=coverage.nPart
particles=coverage.particles
ordNodes=coverage.ordNodes
numOrdNodes=coverage.numOrdNodes
cov_s_without_s=coverage.cov_s_without_s
cov_s=coverage.cov_s
X=coverage.X
radius=coverage.backbone.radius
numIter=2
sink_x = 200
sink_y = 200
E_init=coverage.backbone.E_init
alpha=coverage.backbone.alpha
#print("Inside iter")
#print(X)

# fX1 = [0 for x in range(nPart)]
# fX2 = [0 for x in range(nPart)]
# fX3 = [0 for x in range(nPart)]
fX = [0 for x in range(nPart)]

fgbest=9999
fpbest=[9999.0 for i in range(nPart)]
xpbest=[[] for i in range(nPart)]
xgbest=[]
wmax=0.9
wmin=0.4
c1=0.4
c2=0.4


def crossover(a,b):
    temp=[]
    for i in range(len(a)):
        y=random.random()
        if y<=0.5:
            temp.append(a[i])
        else:
            temp.append(b[i])
    return temp


for t in range(numIter):
    for i in range(len(X)):
        fX[i]=alpha*fitness.fx1_func(numOrdNodes,X,E_init,ordNodes,i)
        if fX[i]<fpbest[i]:
            fpbest[i]=fX[i]
            xpbest[i]=X[i]
            if fX[i]<fgbest:
                fgbest=fX[i]
                xgbest=X[i]
    #for i in range
        #CHANGE ENERGY\
    print("Before changes")
    print(X[1].count(1))
    for i in range(len(X)):
        r1=random.random()
        w=wmin+(wmax-wmin)*(numIter-t)/numIter
        #DETERMINE Xi FOR NEXT ITERATION
        if r1<w:
            #MUTATION
            random.shuffle(X[i])
        # if i==1:
        #     print("After A")
        #     print(X[i].count(1))
        r2=random.random()
        if r2<c1:
            X[i]=crossover(X[i],xpbest[i])
        # if i==1:
        #     print("After B")
        #     print(X[i].count(1))
        r3=random.random()
        if r3<c2:
            X[i]=crossover(X[i],xgbest)
        #print(X[i][0])
        # if i==1:
        #     print("After C")
        #     print(X[i].count(1))


    



#if __name__=='__main__':
