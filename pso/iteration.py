import coverage
import backbone2
import numpy as np
import fitness
import random
import math
import matplotlib.pyplot as plt
#plt.ion()
fig, ax = plt.subplots(1,1,figsize=(8,8))

#plt.xlim((0,400))
#plt.ylim((0,400))
#plt.scatter(200,200,c='y',marker='v',s=200)
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
numIter=201
sink_x = 200
sink_y = 200
E_init=coverage.backbone.E_init
alpha=coverage.backbone.alpha
beta=coverage.backbone.beta
gamma=coverage.backbone.gamma
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


xener = []
yener = []
xdead = []
ydead = []
for t in range(numIter):
    # print(nodes[backbone_nodes[0].ind].res)
    print("iteration number ",t)
    temp=fitness.fx2_func(numOrdNodes,X,ordNodes,particles,neighbours,sink_x,sink_y,nPart)
    for i in range(len(X)):
        fX[i]=alpha*fitness.fx1_func(numOrdNodes,X,E_init,ordNodes,i) + beta*temp[i] + gamma*fitness.fx3_func(numOrdNodes,X,radius,ordNodes,i)
        if fX[i]<fpbest[i]:
            fpbest[i]=fX[i]
            xpbest[i]=X[i]
            if fX[i]<fgbest:
                fgbest=fX[i]
                xgbest=X[i]
    
    for i in ordNodes:
        if(i.alive == True and xgbest[i.ordInd] == 1):
            bb=diction[i]
            dist=math.sqrt((i.x-bb.x)**2 + (i.y-bb.y)**2)
            if i.res>=0:
                i.res-=0.01*dist
                if i.res<=0:
                    i.res=0
                    i.alive = False

            dist2=math.sqrt((bb.x-sink_x)**2 + (bb.y-sink_y)**2)
            if(nodes[bb.ind].res>=0):
                nodes[bb.ind].res -= 0.0075*dist
                if(nodes[bb.ind].res<=0):
                    nodes[bb.ind].res=0
                    nodes[bb.ind].alive = False

                    ordNodes,backbone_nodes,numOrdNodes=backbone2.backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,numOrdNodes,bb.ind,col)
                    diction=coverage.backbone.assign_head(backbone_nodes,ordNodes)
                else:
                    nodes[bb.ind].res -= 0.0075*dist2
                    if(nodes[bb.ind].res<=0):
                        nodes[bb.ind].res=0
                        nodes[bb.ind].alive = False
                        ordNodes,backbone_nodes,numOrdNodes=backbone2.backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,numOrdNodes,bb.ind,col)
                        diction=coverage.backbone.assign_head(backbone_nodes,ordNodes)
    
    if t%10==0:
        enertot = 0
        for i in nodes:
            enertot += i.res
        yener.append(enertot)
        xener.append(t)
        deadnodecount = 0
        for i in nodes:
            if i.alive==False:
                deadnodecount+=1
        ydead.append((len(nodes)-deadnodecount)/len(nodes))
        xdead.append(t)
        # plt.savefig("finalnodegraph.png")
        # plt.clf()
        plt.plot(xener,yener,'r+-')
        plt.savefig("energraph2.png")
        plt.clf()
        plt.plot(xdead,ydead,'r+-')
        plt.savefig("deadgraph.png")
        plt.clf()
        # for i in ordNodes:
        #     if (i.alive==True):
        #         if(xgbest[i.ordInd] == 0):
        #             plt.scatter(i.x,i.y,c='b')
        #         else:
        #             plt.scatter(i.x,i.y,c='r')

        # # for i in ordNodes:
        # #     if(i.xBest == 0):
        # #         plt.scatter(i.x,i.y,c='b')
        # #     else:
        # #         plt.scatter(i.x,i.y,c='r')
        # xcords = [i.x for i in backbone_nodes if i.alive==True]
        # ycords = [i.y for i in backbone_nodes if i.alive==True ]
        # plt.scatter(xcords, ycords, c='k')
        # xc2=[i.x for i in nodes if i.alive==False]
        # yc2=[i.y for i in nodes if i.alive==False]
        # plt.scatter(xc2, yc2, facecolors='y', edgecolors='k')
        # #time.sleep(1)
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        # #time.sleep(0.5)

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

#plt.show()
#time.sleep(20)
print("Dead")
s=0
for i in range(len(nodes)):
    if nodes[i].alive==False:
        s+=1
print(s)