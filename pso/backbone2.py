

def backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,ctrg,temp,col,extra_energy = 1):
	print("Repair called")
	#ordNodes - list containing ordinary nodes
	#nodes - list containing all the nodes 
	#numNodes - total no of nodes
	#backbone_nodes - list containing backbone nodes
	#ctr - number of backbone nodes
	#ctrg - number of ordinary nodes
	#temp - index of the dead node
	#col - array of colors of nodes, 0-> white, 1 ->black, 2->grey
	candidates=[] #list to store neighbouring nodes of the dead backbone node who are grey in color
	n_of_n=[] #array which stores the neighbours of the above grey nodes
	new_backbone=[] #new array which consists of only the new nodes added to the backbone and not the whole backbone
	backbone_nodes.remove(nodes[temp]) #temp is the index of the dead node, that node is removed from the existing backbone
	bbind_ctr=0
	for i in range(len(backbone_nodes)):
		backbone_nodes[i].bbind=bbind_ctr
		bbind_ctr+=1
	# if nodes[temp].res > 0:
	# 	ordNodes.append(nodes[temp]) 
		
	ctr-=1  #decrease the total number of nodes in the backbone by 1
	for i in range(0,len(neighbours[temp])-1):  #for loop to traverse through the neighbours of the dead node
		if col[neighbours[temp][i].ind]==2: #if the ith neighbour of the dead node is grey in color
			candidates.append(neighbours[temp][i]) #add that neighbour to the list of candidates for repair
	for i in range(len(candidates)):  #for loop to traverse through the candidates
		if candidates[i].alive == False: #if candidate is dead then don't consider it
			continue 
		flag=False
		n_of_n=neighbours[candidates[i].ind] #if candidate is alive, store all it's neighbours in the array n_of_n
		for j in range(0,len(n_of_n)-1): #traverse through the neighbours of this candidate
			n3=neighbours[n_of_n[j].ind] #n3 stores the neighbours of each neighbour of the candidate
			for k in range(len(n_of_n)): #for loop to traverse through the neighbours of the candidate
				if k!=j and k!=len(n_of_n)-1: #if neighbour is not equal to itself and if the index is not the last index
					n4=neighbours[n_of_n[k].ind] #n4 stores the neighbours of the above obtained node
					if n_of_n[j] not in n4: #if the 2 neighbours of the candidate nodes are not previously connected, candidate becomes the replacement
						candidates[i].res+=extra_energy #increase the residual energy of the candidate 
						candidates[i].einit+=extra_energy #increase the initial energy of the candidate
						backbone_nodes.append(candidates[i]) #add the candidate to the list of backbone nodes
						candidates[i].bbind=len(backbone_nodes)-1
						ctr+=1
						if candidates[i] in ordNodes: 
							ordNodes.remove(candidates[i]) #remove the candidate from the list of ordinary nodes
							ctrg-=1	
							for ii in range(len(ordNodes)):
								ordNodes[ii].ordInd=ii						#decrease the count of ordinary nodes by 1
						# new_backbone.append(candidates[i]) #add the candidate to the list of newly added nodes to the backbone
						 								#increase the number of backbone nodes by 1
						return ordNodes,backbone_nodes,ctrg

	return ordNodes,backbone_nodes,ctrg  #return the ordinary nodes, backbone nodes and the count of ordinary nodes

