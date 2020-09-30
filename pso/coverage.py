import backbone
import math
import random



nPart = 300
numNodes=backbone.numNodes
nodes=backbone.nodes
radius=backbone.radius
X = [[0 for y in range(numNodes)] for x in range(nPart)]
#print(X)
ro=0.75

class particle:
	def __init__(self, x, y):
		self.ind = 0
		self.x = x
		self.y = y


particles=[]
for i in range(numNodes):
	x = random.randint(0, 100)
	y = random.randint(0, 100)
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
            temp=1+ro*d
            cov_s_p[i][j]=1/(temp**2)
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
        temp=temp*(1-cov_s_p[i][j.ind])
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
        for k in R_particle[j]:
            if k.ind!=i:
                temp=temp*(1-cov_s_p[j][k.ind])
        cov_p_without_s[i][j]=1-temp

cov_s_without_s=[min(cov_p_without_s[i]) for i in range(nPart)]

# for i in range(numNodes):
#     if cov_s_without_s[i]<cov_s[i]:
#         X[]

            