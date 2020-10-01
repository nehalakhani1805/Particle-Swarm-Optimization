import backbone
import math
import random
random.seed(10)


nPart = 100
numNodes=backbone.ctrg
nodes=backbone.ordinary
radius=backbone.radius
# print(numNodes)
X = [[0 for y in range(numNodes)] for x in range(nPart)]
#print(X)
ro=0.03
for i in range(len(nodes)):
    nodes[i].indg=i

class particle:
	def __init__(self, x, y):
		self.ind = 0
		self.x = x
		self.y = y


particles=[]
for i in range(nPart):
	x = random.randint(0, 400)
	y = random.randint(0, 400)
	n = particle(x, y)
	n.ind = i
	particles.append(n)

cov_s_p = [[0.0 for y in range(numNodes)] for x in range(nPart)]
dis_s_p=  [[0.0 for y in range(numNodes)] for x in range(nPart)]

for i in range(nPart):
    for j in range(numNodes):
        d=(nodes[j].x-particles[i].x)**2 + (nodes[j].y-particles[i].y)**2
        dis_s_p[i][j]=math.sqrt(d)
        rad=radius**2
        if(d<=rad):
            temp=1+ro*math.sqrt(d)
            cov_s_p[i][j]=1/(temp**2)
            #print(cov_s_p[i][j])
        else:
            cov_s_p[i][j]=0
#R_node matlab all the particles in the radius of a particular node
R_node=[[] for x in range(numNodes)]
for i in range(numNodes):
    for j in range(nPart):
        if(dis_s_p[j][i]<radius):
            R_node[i].append(particles[j])

#R_particle matlab all the node jinke radius mein a particular particle is 
R_particle=[[] for x in range(nPart)]
for i in range(numNodes):
    for j in range(nPart):
        if(dis_s_p[j][i]<radius):
            R_particle[j].append(nodes[i])

cov_p=[]
for i in range(len(R_particle)):
    temp=1
    for j in R_particle[i]:
        temp=temp*(1-cov_s_p[i][j.indg])
    cov_p.append(1-temp)

cov_s=[]

for i in range(len(R_node)):
    mini=9999
    for j in R_node[i]:
        #print(cov_p[j.ind])
        if cov_p[j.ind] < mini:
            mini=cov_p[j.ind]
    cov_s.append(mini)

cov_n=0
mini=9999
for i in range(numNodes):
    if cov_s[i]<mini:
        mini=cov_s[i]
cov_n=mini

cov_p_without_s=[[0.0 for y in range(nPart)] for x in range(numNodes)]

for i in range(numNodes):
    for j in range(nPart):
        temp=1
        for k in R_particle[j]:
            if k.indg!=i:
                temp=temp*(1-cov_s_p[j][k.indg])
        cov_p_without_s[i][j]=1-temp
#print(cov_p_without_s)
cov_s_without_s=[min(cov_p_without_s[i]) for i in range(numNodes)]
# cov_s_without_s=[]
# for i in range(len(cov_p_without_s)):
#     mini=9999
#     for j in range(len(cov_p_without_s[i])):
#         if cov_p_without_s[i][j]<mini:
#             mini=cov_p_without_s[i][j]
#     cov_s_without_s.append(mini)
# for i in range(numNodes):
#     if cov_s_without_s[i]<cov_s[i]:
#         X[]
awake=[]
# print("without s")
# for i in cov_s_without_s:
#     print(i)
#print("with s")
#for i in cov_s:
    #print(i)
for i in range(numNodes):
    if cov_s_without_s[i]<cov_s[i]:
        awake.append(1)
    else:
        awake.append(0)

for j in range(numNodes):
    for k in R_node[j]:
        X[k.ind][j]=awake[j]
s=0
# print(len(X))
for i in range(len(X)):
    if X[i].count(1)!=0:
        #print(X[i].count(1))
        s+=X[i].count(1)
#print(s)



    
    

            