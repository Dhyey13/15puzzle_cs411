''' CS 411 Homework 3: Solving 15 Puzzle using BFS;
    Name: Dhyey Patel;
    Professor Piotr;
    Assignment Description: 15 Puzzle Solver using breadth first search.
    Prompts user to enter 16 numbers in a form of 2D list from 0-16 and  
    gives the solution, the number of nodes expanded, path, memory used, 
    and time elapsed.
'''
import math
import time
import os, psutil # psutil for memory calculation

# Solution board should look like this:
finalBoard = str([[1, 2, 3, 4],
                  [5, 6, 7, 8], 
                  [9, 10, 11, 12],
                  [13, 14, 15, 0]])

# returns the list of the moves
def moves(sol): 
    listMoves = []  

    # for evaluation of the given source
    locate = eval(sol)   
    x = 0

    while 0 not in locate[x]: 
        x += 1
    y = locate[x].index(0);   

    if x > 0:      
        # move up
        locate[x][y], locate[x-1][y] = locate[x-1][y], locate[x][y]
        listMoves.append(str(locate))
        locate[x][y], locate[x-1][y] = locate[x-1][y], locate[x][y]
    
    if y < 3:                
        # move right
        locate[x][y], locate[x][y+1] = locate[x][y+1], locate[x][y]   
        listMoves.append(str(locate))
        locate[x][y], locate[x][y+1] = locate[x][y+1], locate[x][y]  
      
    if x < 3:                  
        # move down
        locate[x][y], locate[x+1][y] = locate[x+1][y], locate[x][y]   
        listMoves.append(str(locate))
        locate[x][y], locate[x+1][y] = locate[x+1][y], locate[x][y]   

    if y > 0:                   
        # move left
        locate[x][y], locate[x][y-1] = locate[x][y-1], locate[x][y]   
        listMoves.append(str(locate))
        locate[x][y], locate[x][y-1] = locate[x][y-1], locate[x][y]   

    return listMoves

def recordMoves(sol):
    # for marking the coordinates
    mrk = []
    # for listing the moves
    moves = []
    for x in range(0, len(sol)):
      locate = eval(sol[x])
      y = 0
      # y index of 0 in a row
      while 0 not in locate[y]: 
        y += 1
      # z index of 0 in a row
      z = locate[y].index(0);   
      mrk.append((y,z))
    for x in range(0, len(mrk)-1):
      if mrk[x][1] == mrk[x+1][1]:
        if mrk[x][0] > mrk[x+1][0]:
          moves.append('u')
        else:
          moves.append('d')
      elif mrk[x][0] == mrk[x+1][0]:
        if mrk[x][1] > mrk[x+1][1]:
          moves.append('l')
        else:
          moves.append('r')
    return moves

# the breadth first search algorithm
def bfsSolver(startBoard): 
    # counts expanded nodes
    countNodes = 0 
    # to check the nodes that are already expanded
    expanded = []
    # append the first node to the first
    top = [[startBoard]] 
    while top: 
        x = 0
        # minimum
        for y in range(1, len(top)):    
            if len(top[y]) < len(top[x]):
                x = y
        path = top[x]         
        top = top[:x] + top[x+1:]
        endNode = path[-1]
        if endNode in expanded:
            continue
        for z in moves(endNode):
            if z in expanded:
                continue
            top.append(path + [z])
        expanded.append(endNode)
        countNodes = countNodes + 1
        if endNode == finalBoard: 
            break
    print ("Nodes Expanded: ", countNodes)
    return path

# main
def main():
    # prompt user for numbers
    print("Enter numbers from 0 to 16: ")
    myList = [int(i) for i in input().split()][:16]
    startBoard = str([[myList[0], myList[1], myList[2], myList[3]],
                      [myList[4], myList[5], myList[6], myList[7]], 
                      [myList[8], myList[9], myList[10], myList[11]],
                      [myList[12], myList[13], myList[14], myList[15]]])
   
    # start calculating memory
    process = psutil.Process(os.getpid())
    # record the starting time stamp
    startTime= time.time()
    memoryBefore = process.memory_info().rss / 1024.0
    solution = bfsSolver(startBoard)
    moves = recordMoves(solution)
    # record the ending time
    endTime = time.time()
    memoryAfter = process.memory_info().rss / 1024.0
    
    # the output: memory, time elapsed, path, and moves
    print("Memory elapsed: ", (memoryAfter - memoryBefore), "kb");
    print("Time elapsed Solving:" ,round((endTime - startTime), 3), "seconds")
    print("Moves Taken:", moves)

if __name__ == '__main__': main()