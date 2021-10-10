'''
	Dhyey Patel;
	CS 411;
	Homework 4; 
	DUE: 02/19/21 09:00AM
	Professor Piotr;
	Assignment description: Solving 15 puzzle by using Iterative 
	Deepening Depth First Search.
'''

import time
import psutil, os

from queue import PriorityQueue

class Node:
	def __init__( self, state, parent, operator, depth, cost ):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost

	def getParent(self):
		return self.parent

	def getState(self):
		return self.state
		
	def getMoves(self):
		return self.operator
		
	def getCost(self):
		return self.cost
	
	def pathFromStart(self):
		stateList = []
		movesList = []
		currNode = self
		while currNode.getMoves() is not None:
			#print stateList
			stateList.append(currNode.getState())
            #print movesList
			movesList.append(currNode.getMoves())
			currNode = currNode.parent
		movesList.reverse()
		stateList.reverse()
		return movesList

finalState = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]

# Moves the blank tile right on the board. Returns a new state as a list.
def move_right (state):
	# Performs an object copy. Python passes by reference.
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [3, 7, 11, 15]:
		# Swap the values.
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None
		return None

# Moves the blank tile left on the board. Returns a new state as a list.
def move_left (state):
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 4, 8, 12]:
		# Swap the values.
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move it, return None
		return None
	
# Moves the blank tile up on the board. Returns a new state as a list
def move_up (state):
	# Perform an object copy
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 1, 2, 3]:
		# Swap the values.
		temp = new_state[index - 4]
		new_state[index - 4] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None
		return None

# Moves the blank tile down on the board. Returns a new state as a list.
def move_down (state):
	# Perform object copy
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [12, 13, 14, 15]:
		# Swap the values.
		temp = new_state[index + 4]
		new_state[index + 4] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		# Can't move, return None
		return None

def expand_node (node):
	# Returns a list of expanded nodes
	expanded_nodes = []
	expanded_nodes.append(Node( move_up( node.state ),   node, "U", (node.depth + 1), 0 ) )
	expanded_nodes.append(Node( move_down( node.state ), node, "D", (node.depth + 1), 0 ) )
	expanded_nodes.append(Node( move_left( node.state ), node, "L", (node.depth + 1), 0 ) )
	expanded_nodes.append(Node( move_right( node.state), node, "R", (node.depth + 1), 0 ) )
	# Filter the list and remove the nodes that are impossible (move function returned None)
	expanded_nodes = [node for node in expanded_nodes if node.state != None] 
	return expanded_nodes

# iterative deepening search
def ids (start, goal, depth=10):
	for i in range( depth ):
		result = dls( start, goal, i )
		if result != None: return result

# depth limiting search
def dls (start, goal, depth=10):
	depth_limit = depth
	# A list (can act as a stack too) for the nodes.
	nodes = []
	# Create the queue with the root node in it.
	nodes.append(Node( start, None, None, 0, 0 ) )
	count=0
	explored = []
	while nodes:
		# take the node from the front of the queue
		node = nodes.pop(0)
		count+=1
		explored.append(node.getState())
		# for debugging
		# print ("Trying state", node.state, " and move: ", node.operator)
		# if this node is the goal, return the moves it took to get here.
		if node.state == goal:
			print ("Nodes Expanded: ", count)
			print ("Moves Taken: ")
			return node.pathFromStart()
		if node.depth < depth_limit:
			expanded_nodes = expand_node(node)
			for item in expanded_nodes:
			    state = item.getState()
			    if state not in explored:
			        nodes.insert(0, item)

# Main method
def main():
	' ' ' ******** TEST CASES PROVIDED BY PROFESSOR ******** ' ' '
	#start_state = [1,0,3,4,5,2,6,8,9,10,7,11,13,14,15,12]
	#start_state = [1,2,3,4,5,6,8,0,9,11,7,12,13,10,14,15]
	#start_state = [1,0,2,4,5,7,3,8,9,6,11,12,13,10,14,15]
	#start_state = [1,2,0,4,6,7,3,8,5,9,10,12,13,14,11,15]
	#start_state = [1,3,4,8,5,2,0,6,9,10,7,11,13,14,15,12]

	# OR manually enter:
	print ("Enter numbers from 0 to 15: ")
	start_state = [int(i) for i in input().split()][:16]

	start = time.time()
	process = psutil.Process(os.getpid())
	memoryBefore = process.memory_info().rss 
	result = ids( start_state, finalState )
	end = time.time()
	memoryAfter = process.memory_info().rss 
	print (result)
	print (len(result), " moves")
	# memory calculated in bytes as kb was showing 0.0 kb used when dealing with small mem
	print("Memory elapsed: ", (memoryAfter - memoryBefore), "bytes");
	print("Total searching time: ", round((end-start), 3), "seconds")

if __name__ == "__main__": main()
