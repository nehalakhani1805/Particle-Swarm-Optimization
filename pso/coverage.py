import backbone
import math
import random
random.seed(10)


nPart = 100  #number of particles is arbitrarily 100
numOrdNodes=backbone.ctrg #count of the ordinary nodes are stored in the variable numOrdNodes
ordNodes=backbone.ordinary #list of ordinary nodes is stored in ordNodes
radius=backbone.radius #radius stores the radius of range of each sensor node
X = [[0 for y in range(numOrdNodes)] for x in range(nPart)] #encoding function - array which stores 0 or 1. 0 means node is in sleep state. 1 means it is awake
ro=0.03 #adjustment parameter
particles=[] #list to store all the particles
cov_p=[] #list to store overlap coverage of each point considered
cov_p_without_s=[[0.0 for y in range(nPart)] for x in range(numOrdNodes)] #same as above but  without including coverage of s
cov_s=[] #list to store coverage of each sensor node s
cov_s_without_s=[min(cov_p_without_s[i]) for i in range(numOrdNodes)] #same as above but without including s

#class particle is created whose object stores its index, x coordinate and y coordinate
class particle:       
	def __init__(self, x, y):
		self.ind = 0
		self.x = x
		self.y = y

#function to find the coverage
def find_cov():
    for i in range(len(ordNodes)):
        ordNodes[i].indg=i        #assigning index to each ordinary node 
    for i in range(nPart):        #iterating through the particles array
        x = random.randint(0, 400) #generate a random value between 0 to 400, for the x coordinate of the particle
        y = random.randint(0, 400) #generate a random value between 0 to 400, for the x coordinate of the particle
        n = particle(x, y)         #n is an object of class particle
        n.ind = i                  #n is assigned the index i
        particles.append(n)         #n is added to the list of particles

    cov_s_p = [[0.0 for y in range(numOrdNodes)] for x in range(nPart)] #list to store coverage of sensor s with respect to particle p
    dis_s_p=  [[0.0 for y in range(numOrdNodes)] for x in range(nPart)] #list to store distance of s and particle p

    for i in range(nPart):              #iterate through particles
        for j in range(numOrdNodes):    #iterate through nodes
            d=(ordNodes[j].x-particles[i].x)**2 + (ordNodes[j].y-particles[i].y)**2  #find square of distance between particle and node
            dis_s_p[i][j]=math.sqrt(d)  #take sqrt and find distance
            rad=radius**2 
            if(d<=rad): #if distance squared is less than radius squared i.e particle is within sensor range
                temp=1+ro*math.sqrt(d) 
                cov_s_p[i][j]=1/(temp**2) #find coverage of s with respect to p using the formula given in the paper
            else:       # if particle is not in the sensing range of the sensor
                cov_s_p[i][j]=0 #coverage is zero
    R_node=[[] for x in range(numOrdNodes)] #list to store all the particles in the radius of a particular node
    for i in range(numOrdNodes):
        for j in range(nPart):
            if(dis_s_p[j][i]<radius): #if distance between particle and node is less than the radius of the node
                R_node[i].append(particles[j]) #add the particle to the list

    #R_particle matlab all the node jinke radius mein a particular particle is 
    R_particle=[[] for x in range(nPart)] #list to store all the particles who are in the range of a particular node
    for i in range(numOrdNodes):
        for j in range(nPart):
            if(dis_s_p[j][i]<radius): #if distance between particle and node is less than the radius of the node
                R_particle[j].append(ordNodes[i]) #add the node to the list

    for i in range(len(R_particle)):  #traverse through the list R_particle
        temp=1
        for j in R_particle[i]: #traverse through each list in R_particle
            temp=temp*(1-cov_s_p[i][j.indg]) #formula given in the paper to find overlap of the point
        cov_p.append(1-temp)

    for i in range(len(R_node)):  #traverse through R_node
        mini=math.inf       
        for j in R_node[i]:     #traverse through each list in R_node
            #print(cov_p[j.ind])
            if cov_p[j.ind] < mini: 
                mini=cov_p[j.ind]   #finding minimum overlap out of all the points
        cov_s.append(mini) #assigning the minimum value obtained to the coverage of sensor node s

    cov_n=0
    mini=math.inf
    for i in range(numOrdNodes): #traverse through the list of ordinary nodes
        if cov_s[i]<mini:
            mini=cov_s[i] #finding minimum coverage in the network
    cov_n=mini #minimum coverage obtained is the coverage of the whole network

    for i in range(numOrdNodes): #traverse through the list of ordinary nodes
        for j in range(nPart):  #traverse through the list of particles
            temp=1
            for k in R_particle[j]: #traverse through the list of R_particles
                if k.indg!=i:       #if the node is not equal to itself
                    temp=temp*(1-cov_s_p[j][k.indg]) #find the overlap
            cov_p_without_s[i][j]=1-temp  #finding the overlap same as the cov_p, except this one is without considering the sensor s

    awake=[] #list to store the sleep status of each ordinary node

    for i in range(numOrdNodes):
        if cov_s_without_s[i]<cov_s[i]: #if coverage without the node is less than the coverage with the node, the node is useful
            awake.append(1) #hence the node needs to stay awake
        else: #if coverage without the node is greater than or equal to the coverage then node is redundant
            awake.append(0) #hence the node can be put to sleep

    for j in range(numOrdNodes): # traverse through the list of ordinary nodes
        for k in R_node[j]:      # traverse through particles in the neigbourhood of j
            X[k.ind][j]=awake[j] # update the encoding function X

    s = 0 #sum variable
    #function to find how many total ordinary nodes are alive
    for i in range(len(X)):  #traverse through the encoding function
        if X[i].count(1)!=0: #if the node is alive
            s+=X[i].count(1) #increment s
    return cov_s_without_s, cov_s, X  #return the coverage without including the sensor node, coverage including the sensor node and the encoded function X


# main function 
if __name__ != '__main__':
    cov_s_without_s, cov_s,X=find_cov() #call the find_cov function
    print(numOrdNodes)  #print number of ordinary nodes



    
    

            