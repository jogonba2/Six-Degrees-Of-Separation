#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Seis grados de separación ##

class friendTree:
	
	def __init__(self,nameSource,father):
		self.namePerson = nameSource
		self.father = father
		self.sons = []
	
	def _insertArray(self,peopleNames):
		self.sons = [friendTree(e,self.namePerson) for e in peopleNames]
	
	@staticmethod
	def _insertArrayNoRoot(fTree,peopleNames):
		fTree.sons = [friendTree(e) for e in peopleNames]
		
	@staticmethod 
	def _getDegree(fTree,nameDest):
		return friendTree._getDegreeBack(fTree,nameDest,0)
		
	@staticmethod
	def _getDegreeBack(fTree,nameDest,degree):
		if fTree.namePerson==nameDest: return degree
		else:
			if fTree.sons != None:
				for e in fTree.sons:
					tr = friendTree._getDegreeBack(e,nameDest,degree+1)
					if tr != None: return tr
	@staticmethod
	def _getPersonTree(fTree,namePerson):
		if fTree.namePerson==namePerson: return fTree
		else:
			for e in fTree.sons: 
				tr = friendTree._getPersonTree(e,namePerson)
				if tr != None: return tr
		
	@staticmethod
	def _parseRawDataBack(fd):
		with open(fd,"r") as fd:
			line = fd.readline()
			fTree = friendTree(line[0:line.find(":")],None)
			me = fTree.namePerson
			sons = line[line.find(":")+2:].split(",")	
			sons[len(sons)-1] = sons[len(sons)-1].replace("\n","")
			fTree._insertArray(sons)
			for line in fd.readlines():
				tTree = friendTree._getPersonTree(fTree,line[0:line.find(":")])
				sons = line[line.find(":")+2:].split(",")		
				sons[len(sons)-1] = sons[len(sons)-1].replace("\n","")
				tTree._insertArray(sons)	
		fd.close()
		return friendTree._getPersonTree(fTree,me)
		
	@staticmethod
	def _getUserChain(fTree,namePerson):
		node = friendTree._getPersonTree(fTree,namePerson)
		lst = []
		while node!=None and node.father!=None:
			namePerson = node.father
			lst.append(namePerson)
			node = friendTree._getPersonTree(fTree,namePerson)
		lst.reverse()
		return lst
		
	@staticmethod
	def _getString(fTree,namePerson,root=True):
		chain = friendTree._getUserChain(fTree,namePerson)
		offset = None
		if root == True: 
			res = chain[0] + " conoce a " + chain[1]
			offset = 2
		else: 
			res = chain[1] + " conoce a " + chain[2]
			offset = 3
		for e in chain[offset:]:
			res += " que conoce a " + e
		res += " que conoce a " + namePerson + " por lo tanto, grado: " + str(friendTree._getDegree(fTree,namePerson))
		return res

def main():
	
	## Testing load file and calculate the degree of separation between overxfl0w and friend35 ##
	print "Loading file..."
	sndTree = friendTree._parseRawDataBack("friends.txt")
	print "Testing Overxfl0w -> friend66"
	print friendTree._getString(sndTree,"friend66")
	print "Testing Overxfl0w -> friend46"
	print friendTree._getString(sndTree,"friend46")
	
	## Buscar desde otros nodos que no sean la raiz ##
	print "Testing friend2 -> friend60"
	print friendTree._getString(friendTree._getPersonTree(sndTree,"friend2"),"friend60",False)
	
if __name__ == "__main__": main()
