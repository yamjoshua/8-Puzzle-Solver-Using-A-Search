from Queue import PriorityQueue
from copy import copy, deepcopy
import itertools

#Make Eight Puzzle board from Text Input
class eightPuzzle:
    def __init__(self, s):
        self.puzzle=[[0 for i in range(3)] for j in range(3)] #Creates a 2-D Array. Filled with 3x3 Zeroes
        self.moves=["U","D","L","R"] #Possible Moves
        self.blank=(0,0) #Coordinate for the blank square
        counter = 0
        for i in range(3):
            for j in range(3):
                self.puzzle[i][j] = s[counter]
                if s[counter]=='0':
                    self.blank=(i,j)
                counter += 2
    def possibleMoves(self): #Generates the possible moves based on where the blank is
        posMoves=[]
        if self.blank[0]-1 >=0:
            posMoves.append("U")
        if self.blank[0]+1 <= 2:
            posMoves.append("D")
        if self.blank[1]-1 >= 0:
            posMoves.append("L")
        if self.blank[1]+1 <= 2:
            posMoves.append("R")
        self.moves=posMoves
        return posMoves
    def printPuzzle(self): #Prints the Puzzle to the Console
        counter = 0
        for i in self.puzzle:
            for j in i:
                print (j),
            print
        print
    def swap(self,(y1,x1),(y2,x2)): #Swaps two elements
        temp = self.puzzle[y1][x1]
        self.puzzle[y1][x1]=self.puzzle[y2][x2]
        self.puzzle[y2][x2]=temp
    def up(self): #Shifts blank up
        self.swap(self.blank,(self.blank[0]-1,self.blank[1]))
        self.blank=(self.blank[0]-1,self.blank[1])
    def down(self): #Shifts blank down
        self.swap(self.blank,(self.blank[0]+1,self.blank[1]))
        self.blank = (self.blank[0]+1,self.blank[1])
    def left(self):#Shifts blank left
        self.swap(self.blank,(self.blank[0],self.blank[1]-1))
        self.blank = (self.blank[0],self.blank[1]-1)
    def right(self):#Shifts blank right
        self.swap(self.blank,(self.blank[0],self.blank[1]+1))
        self.blank = (self.blank[0],self.blank[1]+1)
class Node: #Node class to be implemented in the A* search
    def __init__(self, puzzle, goal, heu,parent=None, swap=None):
        self.puzzle=puzzle
        self.goal=goal
        self.parent=parent
        self.swap=swap
        self.heu=heu
        if self.parent!= None:
            self.g = parent.g + 1
        else:
            self.g=0

    def h(self): #Heuristic Function based on user input
        if self.heu==1:
            return manhattanDistance(self.puzzle.puzzle, self.goal)
        else:
             return linearConflicts(self.puzzle.puzzle,self.goal)
    def f(self): #f(n) value
        return self.h()+self.g
    def path(self): #Traces path from solution to root
        node=self
        path=[]
        while node:
            path.append(node.swap)
            node=node.parent
        solution=path[::-1]
        return solution[1:]
    def sumValues(self): #Each individual f(n) value for each Node
        node=self
        sums=[]
        while node:
            sums.append(node.f())
            node=node.parent
        solution=sums[::-1]
        return solution[1:]
    def neighbors(self): #Generates all possible neighbor squres
        neighbors=[]
        posMoves=self.puzzle.possibleMoves()
        for i in posMoves:
            if i=="U":
                board=self.cloneNode("U")
                board.puzzle.up()
                neighbors.append(board)
            elif i=="D":
                board = self.cloneNode("D")
                board.puzzle.down()
                neighbors.append(board)
            elif i=="L":
                board = self.cloneNode("L")
                board.puzzle.left()
                neighbors.append(board)
            elif i=="R":
                board = self.cloneNode("R")
                board.puzzle.right()
                neighbors.append(board)
        return neighbors
    def cloneNode(self,swapped):
        return Node(deepcopy(self.puzzle), self.goal,self.heu, parent=self,swap=swapped)
    def priorityQueue(self): #Tuple to be put into priority Q
        return(self.f(),self)

def Asolve(start,goal): #A* Search Algorithm
    counter=0
    queue = PriorityQueue()
    seen=[]
    queue.put(start.priorityQueue())
    counter+=1
    while not queue.empty():
        print(seen)
        node=queue.get()[1]
        if node.puzzle.puzzle != goal:
            for neighbor in node.neighbors():
                if neighbor != node.parent and neighbor.puzzle.puzzle not in seen:
                    queue.put(neighbor.priorityQueue())
                    seen.append(neighbor.puzzle.puzzle)
                    counter+=1
        else:
            return (node.path(),counter,node.sumValues())
    return (None,counter)


def manhattanDistance(currentPuzzle,goalPuzzle): #Manhattan Distance
    sum =0
    for i in range(3):
        for j in range(3):
            if currentPuzzle[i][j]!="0":
                tupleOne = (i,j)
                tupleTwo = indexArray(currentPuzzle[i][j],goalPuzzle)
                sum+=abs(tupleOne[0]-tupleTwo[0])+abs(tupleOne[1]-tupleTwo[1])
    return sum
def linearConflicts(currentPuzzle,goalPuzzle): #Linear Conflicts Heuristic
    linearConflicts=[]
    columnsInit=[]
    for i in range(3):
        columnsInit.append([row[i] for row in currentPuzzle])
    for i in range(3):
        for x,y in itertools.combinations(currentPuzzle[i],2): #Takes Every Combination between two items in a row
            if (indexArray(x,goalPuzzle)[0]==indexArray(y,goalPuzzle)[0]) and (indexArray(x,goalPuzzle)[1]-indexArray(y,goalPuzzle)[1]>=0):
                linearConflicts.append((x,y))
    for i in range(3):
        for x,y in itertools.combinations(columnsInit[i],2): #Takes Every Combination between two items in a column
            if (indexArray(x,goalPuzzle)[1]==indexArray(y,goalPuzzle)[1]) and (indexArray(x,goalPuzzle)[0]-indexArray(y,goalPuzzle)[0]>=0):
                linearConflicts.append((x,y))
    for i in linearConflicts: #Removes any conflicts with zero as an element
        if i[0]==0 or i[1]==0:
            linearConflicts.remove(i)
    return manhattanDistance(currentPuzzle,goalPuzzle) + (len(linearConflicts*2))

def indexArray(item, array): #Returns the Index of an Array
    for i in range(3):
        if item in array[i]:
            return (i,array[i].index(item))
    return -1

def main():
    textFile = raw_input("Name of your file: ")
    selection = raw_input("Choose one of the following as the heuristic functions: \n \t 1) Sum of Manhattan distances"
                      "\n \t 2) Sum of Manhattan distances + 2 * Number of Linear Conflicts"
                        "\nYour Selection: ") #Choose the heuristic function
    inputFile = open(textFile,"r")
    line = inputFile.readlines()
    lines = [x.strip() for x in line]
    lines = ' '.join(lines)
    initialString = lines.split('  ')[0]
    goalString=lines.split('  ')[1] #Formating the Text input into a string
    iPuzzle=eightPuzzle(initialString) #Generating the initial State Puzzle Object
    gPuzzle=eightPuzzle(goalString) #Generating the goal state Puzzle Object

    iPuzzle.printPuzzle() #Prints the initial state to the console
    gPuzzle.printPuzzle() #Prints the goal state to the console
    root = Node(iPuzzle, gPuzzle.puzzle,int(selection),None,None) #Creating the root Node

    solution=Asolve(root,gPuzzle.puzzle)
    print(len(solution[0])) #Depth of Search Tree
    puzzleSolution=solution[1]
    print(puzzleSolution)#Number of Nodes
    print(solution[0])#Solution
    print(solution[2]) #f(n) values


main()