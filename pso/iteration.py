import coverage
import backbone2
import numpy as np
import fitness
import random
import math
import matplotlib.pyplot as plt
plt.ion()
fig, ax = plt.subplots(1,1,figsize=(8,8))
plt.xlim((0,400))
plt.ylim((0,400))
plt.scatter(200,200,c='y',marker='v',s=200)
import time

backbone_nodes = coverage.backbone.backbone_nodes

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
numIter=20
sink_x = 200
sink_y = 200
E_init=coverage.backbone.E_init
alpha=coverage.backbone.alpha
backbone_nodes=coverage.backbone.backbone_nodes
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


ctr = coverage.backbone.ctr
ctrg = coverage.backbone.ctrg
col = coverage.backbone.col


def crossover(a,b):
    temp=[]
    for i in range(len(a)):
        y=random.random()
        if y<=0.5:
            temp.append(a[i])
        else:
            temp.append(b[i])
    return temp
diction=coverage.backbone.assign_head(backbone_nodes,ordNodes)
# for i in diction:
#     print(diction[i].ind)

for t in range(numIter):
    # print(nodes[backbone_nodes[0].ind].res)
    for i in range(len(X)):
        fX[i]=alpha*fitness.fx1_func(numOrdNodes,X,E_init,ordNodes,i)
        if fX[i]<fpbest[i]:
            fpbest[i]=fX[i]
            xpbest[i]=X[i]
            if fX[i]<fgbest:
                fgbest=fX[i]
                xgbest=X[i]
    for i in ordNodes:
        bb=diction[i]
        dist=math.sqrt((i.x-bb.x)**2 + (i.y-bb.y)**2)
        if i.res>=0:
            i.res-=0.01*dist
            if i.res<=0:
                i.res=0
                i.alive = False

        dist2=math.sqrt((bb.x-sink_x)**2 + (bb.y-sink_y)**2)
        if(nodes[bb.ind].res>=0):
            nodes[bb.ind].res -= 0.01*dist
            if(nodes[bb.ind].res<=0):
                nodes[bb.ind].res=0
                nodes[bb.ind].alive = False

                ordNodes,backbone_nodes,numOrdNodes=backbone2.backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,numOrdNodes,bb.ind,col)
                diction=coverage.backbone.assign_head(backbone_nodes,ordNodes)
            else:
                nodes[bb.ind].res -= 0.005*dist2
                if(nodes[bb.ind].res<=0):
                    nodes[bb.ind].res=0
                    nodes[bb.ind].alive = False
                    ordNodes,backbone_nodes,numOrdNodes=backbone2.backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,numOrdNodes,bb.ind,col)
                    diction=coverage.backbone.assign_head(backbone_nodes,ordNodes)
    
    for i in range(len(xgbest)):
        if(xgbest[i] == 0):
            plt.scatter(ordNodes[i].x,ordNodes[i].y,c='b')
        else:
            plt.scatter(ordNodes[i].x,ordNodes[i].y,c='r')

    xcords = [i.x for i in backbone_nodes]
    ycords = [i.y for i in backbone_nodes]
    plt.scatter(xcords, ycords, c='k')
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.5)

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

# print(xgbest.count(1))



    



#if __name__=='__main__':
