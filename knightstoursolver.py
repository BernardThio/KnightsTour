#improting pygame to draw the knightstour
import pygame

'''
Author: Ben-Ji Thio, finished on 4-5-2020
The knightstour is the path a knight can take in a chess game, to make sure that it touches every square once
This program will calculate the knightstour, using a backtracking algorithm. However, if only a backtracking algorithm is implemented, it will take a long time to calculate a valid path, because it is in NP.
To fix that problem, an algorithm was also implemented, to make sure it tries the moves which are most likely to succeed first
I will comment starting from the main solve function, and branch off into the other functions.
'''

#this is the actual backtracking algorithm which solves the knighstour
def solve(posX, posY, posList, lenX, lenY): #it takes a starting position Y and X, and also a list of where it has already been, called posList and decides the size of the board
    if len(posList) == lenX * lenY: #this tells the program when to quit. If it is for instance trying to solve an 8x8 knightstour, if it has touched every square, the length of posList will be equal to 8*8 = 64, and it needs to stop when it gets there
        print(posList)  #this tells the program to print posList if it is finished
        return True
    listMoves = [[posX - 2, posY - 1], [posX-2, posY + 1], [posX-1, posY + 2], [posX + 1, posY + 2], [posX+2, posY + 1], [posX+2, posY -1], [posX+1, posY - 2], [posX-1, posY -2]]  #this are all the possible moves a knight can perform
    listMoves = prioritise(posX, posY, posList, listMoves, lenX, lenY)  #this backtracking program will try the first move in listMoves first, however this takes a very long time if it always does the same one first.
                                                            #this prioritise function will change the order of the function to minimilise the calculation time. This is further explained in 'def prioritise'
    for move in listMoves:
        if checkMove(move[0], move[1], posList, lenX, lenY):    #if the move is legal
            posList.append([move[0], move[1]])  #add it to poslist
            if solve(posList[-1][0], posList[-1][1], posList, lenX, lenY):  #call the solve function in itself again (recursion)
                return posList  #this ensure that the function as a whole returns posList, so that it can be drawn
    posList.pop()   #if no moves are possible, it runs through here and pops the last element of the lest, before returning the function, meaning that it will go one 'layer' back
    return False

'''
The prioritise function does the following:
It takes in the current position of the knight  posX, posY
It takes in all the possible moves and where the knight already has been
It makes a new list called order and calculates using the function nMovesFind how likely it is that this move is the best choice (very brief explaination, for more in depth explaination go to 'def nMovesFind'),
and assigns a value to order. The lower the value of order, how 'more likely' it is that the move with the same index as the index of the value of order, is the best move.
It then reassembles the list of moves, called listMovesPri in this function to avoid confusion, and then returns it, which causes the solve function to try the best moves first
'''
def prioritise(posX, posY, posList, listMoves, lenX, lenY):
    listMovesPri = [[posX - 2, posY - 1], [posX-2, posY + 1], [posX-1, posY + 2], [posX + 1, posY + 2], [posX+2, posY + 1], [posX+2, posY -1], [posX+1, posY - 2], [posX-1, posY -2]]   #All possible moves under a different name to avoid confusion
    order = []  #Declaring the order list, which is currently empty
    for move in listMoves:  #It goes through every move in listMoves
        order.append(nMovesFind(posList, move[0], move[1], lenX, lenY)) #and for each move appends the number of moves it is possible to do from that move, and places it in the list order under the same index as the move in listMoves it was calculated from
    run = True  #Setting up a variable to ensure that the while loop can be stopped
    runCount = 0 #adding a counter
    while run:
        for i in range(len(order)-1):   #for each i in range(8)
            if order[i] > order[i+1]:   #if the nMoves in order at index i is bigger than at index i + 1, it is swapped
                if i != 7:  #making sure swapping between the last element of a list and the first isn't possible
                    listMovesPri[i], listMovesPri[i+1] = listMovesPri[i+1], listMovesPri[i] #swapping the number
                    order[i], order[i+1] = order[i+1], order[i] #swapping the list order at the same index
        runCount += 1   #everytime this is done for every i in range(8), the run counter increases with one
        if runCount == 7:   #if it is at 7, the while loop has run enough, to ensure that it is perfectly ordered
            run = False     #stopping the while loop
            return listMovesPri #returning the list of moves ordered by priority

def nMovesFind(posList, posX, posY, lenX, lenY):   #this calculates the number of possible moves. It is used in the function prioritise to calculate which move should come first in the list of listMovesGlob, which will in turn decide what move gets calculated first in the function solve
    listMoves = [[posX - 2, posY - 1], [posX-2, posY + 1], [posX-1, posY + 2], [posX + 1, posY + 2], [posX+2, posY + 1], [posX+2, posY -1], [posX+1, posY - 2], [posX-1, posY -2]]
    nMoves = 0  #counter for number of possible moves
    for move in listMoves:  #from the move activated in prioritise, this calculates the number of moves possible from that move
        if checkMove(move[0], move[1], posList, lenX, lenY):    #if a move is possible, it adds 1 to the move counter, if there are more moves possible, it is easier to reach from a different place, and
            nMoves += 1                            #it is therefore less important to reach right away. Basically: the more ways there are to reach that square, and it will be less important to go there right away
    if nMoves == 0:     #if there are 0 places you can go from that move, that move shouldn't even be tried except if it's the last one and therefor should be at the end of the order
        nMoves = 9
    return nMoves   #it returns n of moves possible from a square

#This checks the move
def checkMove(posX, posY, posList, lenX, lenY):
    if posX < 0 or posX > lenX - 1 or posY < 0 or posY > lenY - 1: #adding 'walls'
        return False
    if [posX, posY] in posList: #making sure you can't go back to the same coördinates
        return False
    return True #if it passes the above 'tests', it is a legal move and therefore True can be returned

startPos = [0,0]    #where the horse starts
lenX = 7        #the lenght of the board in the X direction
lenY = 7       #the length of the board in the Y direction
sul = solve(startPos[0], startPos[1] ,[startPos], lenX, lenY) #running the solve command at position 0,0 and with posList at with the starting location

#this uses pygame to draw the knighstour
pygame.init()
screen = pygame.display.set_mode((lenX * 27,lenY * 27)) #makes a screen
pygame.display.set_caption("Knightstour")
try:
    for move in sul:    #goes through every move in the solution
        pygame.time.delay(750)  #delay
        pygame.draw.rect(screen, (255,255,255), (move[0] * 27, move[1] * 27, 25, 25))   #draws a screen with correct length and scales the coördinate with 27 pixels, to ensure better visibility
        pygame.display.update() #updates the screen
except: #if an error occurs, something is wrong with the given input and the following will be printed
    print("Not a valid input")
