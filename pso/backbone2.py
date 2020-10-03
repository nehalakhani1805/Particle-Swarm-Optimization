

def backbone_repair(ordNodes,nodes,numNodes, backbone_nodes, neighbours,ctr,ctrg,temp,col):
	
	candidates=[] #grey neighbours
	n_of_n=[]
	new_backbone=[]
	backbone_nodes.remove(nodes[temp])
	ctr-=1
	for i in range(0,len(neighbours[temp])-1):
		if col[neighbours[temp][i].ind]==2:
			candidates.append(neighbours[temp][i])
	for i in range(len(candidates)):
		if candidates[i].alive == False:
			continue
		flag=False
		n_of_n=neighbours[candidates[i].ind]
		for j in range(0,len(n_of_n)-1):
			n3=neighbours[n_of_n[j].ind]
			for k in range(len(n_of_n)):
				if k!=j and k!=len(n_of_n)-1:
					n4=neighbours[n_of_n[k].ind]
					if n_of_n[j] not in n4 and n_of_n[k] not in n3:
						candidates[i].res+=50
						candidates[i].einit+=50
						backbone_nodes.append(candidates[i])
						if candidates[i] in ordNodes:
							ordNodes.remove(candidates[i])
							ctrg-=1							
						new_backbone.append(candidates[i])
						ctr+=1
						#ctr+=1
						return ordNodes,backbone_nodes,ctrg
						# flag=True
						# break
			if flag:
				break
	return ordNodes,backbone_nodes,ctrg

