import string
import numpy
from queue import Queue
import copy

#####################################################################
def splitToQueue(word): 
    queue = list()
    for char in word:
        queue.append(char)
    return queue

def ProgramBuilder():
    file = open("entrada.txt","r")

    program = file.readlines()

    transitions = []
    for i in range(len(program)):
        currentState = program[i][0]
        if currentState == '*':
            break
        currentChar = program[i][2]
        currentInstruction = 'read'
        if currentChar == ' ' and (len(program[i]) > 7):
            currentChar = program[i][6]
            currentInstruction = 'write'
            
        newState = program[i][4]
        transitions.append([currentState,currentChar,newState,currentInstruction])
        
    return transitions

def GetCurrentTransition(transitions, currentState, currentChar):
    for i in range(len(transitions)):
        if currentState == transitions[i][0] and currentChar == transitions[i][1]:
            return transitions[i]
        elif currentState == transitions[i][0] and transitions[i][3] == 'write':
            return transitions[i]

    return 0

#####################################################################


machine = ProgramBuilder()

palavra = input("Digite uma palavra:\n")
execution = input("Qual o número máximo de execuções?\n")
fila = splitToQueue(palavra)

# program start
currentExecution = 0
currentState = '1'

while len(fila) > 0:
    auxQueue = fila.copy()
    currentChar = auxQueue.pop(0)
    currentTransition = GetCurrentTransition(machine, currentState, currentChar)
    if currentTransition == 0:
        print("Palavra não suportada")
        exit()
    if currentTransition[2] == 'h':
        print("PALAVRA ACEITA!\n")
        exit()

    currentInstruction = currentTransition[3]

    if currentInstruction == 'read':
        fila.pop(0)
    elif currentInstruction == 'write':
        fila.append(currentTransition[1])
    
    currentState = currentTransition[2]
    currentExecution+=1
    print(fila)
    if currentExecution >= int(execution):
        print("Número máximo de execuções atingido.\n")
        exit()
