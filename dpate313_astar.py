'''
	Dhyey Patel;
	CS 411;
	Homework 5; 
	DUE: 02/26/21 09:00AM
	Professor Piotr;
	Assignment description: Solving 15 puzzle by using A-star
	heuristic search (misplaced tiles,  manhattan distance)
'''

import time
import psutil, os

from queue import PriorityQueue

def board_state(state):
	i=0
	temp=[([0] * 4) for j in range(4)]
	for row in range(4):
		for col in range(4):
			temp[row][col] = state[i]
			i+=1
	return temp
	
class Node:
	def __init__(self, state, parent, operator, depth, cost):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost
		self.f_cost = 0

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

def h1(state, goal):
	#using misplaced tiles
	cost = 0
	for i in range( len( state ) ):
		if state[i] != goal[i]:
			cost += 1
	return cost 

def f1(node):
	#using misplaced tiles
	return node.depth + h1(node.state, finalState)

def h2(state):
	#using Manhattan distance
	finalposition = [(0,0),(0,1),(0,2),(0,3),
				     (1,0),(1,1),(1,2),(1,3),
					 (2,0),(2,1),(2,2),(2,3),
					 (3,0),(3,1),(3,2),(3,3)]
	cost = 0
	temp=board_state(state)
	for y in range(4):
		for x in range(4):
			t = temp[y][x]
			xf, yf = finalposition[t]
			cost += abs(xf - x) + abs(yf - y)
	return cost

def f2(node):
	#using sum of manhattan distance
	return node.depth + h2(node.state)

# Perfoms the A* heuristic search
def a_star(start, goal):
	process = psutil.Process(os.getpid())
	memoryBefore = process.memory_info().rss / 1024.0
	nodes = []
	nodes.append(Node( start, None, None, 0, 0 ) )
	explored = []
	count=0
	while nodes:
		# take the node from the front of the queue
		node = nodes.pop(0)
		explored.append(node.getState())
		#misplaced tiles
		#f1(node) 
		#manhattan distance
		f2(node)
		count+=1
		# for debugging
		# if this node is the goal, return the moves it took to get here.
		# print ("Trying state", node.state, " and move: ", node.operator)
		if node.state == goal:
			memoryAfter = process.memory_info().rss / 1024.0
			print ("The number of nodes visited", count)
			print ("States of moves are as follows:")
			print("Memory elapsed: ", (memoryAfter - memoryBefore), "kb")
			return node.pathFromStart()
		else:
		    # Expand the node and add all the expansions to the end of the queue
			expanded_nodes = expand_node( node )
			for item in expanded_nodes:
			    state = item.getState()
			    if state not in explored:
			       nodes.append(item)

# Main method
def main():
	' ' ' ******** TEST CASES PROVIDED BY PROFESSOR ******** ' ' '
	#start_state = [1,0,3,4,5,2,6,8,9,10,7,11,13,14,15,12]
	start_state = [1,2,3,4,5,6,8,0,9,11,7,12,13,10,14,15]
	#start_state = [1,0,2,4,5,7,3,8,9,6,11,12,13,10,14,15]
	#start_state = [1,2,0,4,6,7,3,8,5,9,10,12,13,14,11,15]
	#start_state = [1,3,4,8,5,2,0,6,9,10,7,11,13,14,15,12]

	# OR manually enter:
	#print ("Enter numbers from 0 to 15: ")
	#start_state = [int(i) for i in input().split()][:16]

	start = time.time()
	 
	result = a_star( start_state, finalState )
	end = time.time()
	print (result)
	print (len(result), " moves")
	print("Total searching time: ", round((end-start), 3), "seconds")

if __name__ == "__main__": main()
