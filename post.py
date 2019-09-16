import string
import numpy
from queue import Queue
import copy

#####################################################################

# Separa a palavra (string) numa fila
def splitToQueue(word): 
    queue = list()
    for char in word:
        queue.append(char)
    return queue

# Monta o programa que a Máquina de Post executará
def ProgramBuilder():
    file = open("entrada2.txt","r")

    program = file.readlines()

    transitions = []
    for i in range(len(program)):
        currentState = program[i][0]

        # Se for um comentário, ignora
        if currentState == '*':
            continue
        currentChar = program[i][2]
        currentInstruction = 'read'   # Inicialmente define como read
        # Se não tiver algo para ler, define a instrução com o tipo write
        if currentChar == ' ' and (len(program[i]) > 7):
            currentChar = program[i][6]
            currentInstruction = 'write'
            
        newState = program[i][4]
        transitions.append([currentState,currentChar,newState,currentInstruction])
        
    return transitions

# Verifica qual transição do autômato combina com a transição e caractere atual da fita no caso de read
# Se nenhum combina, retorna a transição de write do estado atual
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

# Program start
currentExecution = 0
currentState = '1'
halted = False

while not halted:
    auxQueue = fila.copy()   # Copia a fila para uma auxiliar
    if len(auxQueue) > 0:
        currentChar = auxQueue.pop(0)

    # Retorna a transição que combina com as condições atuais
    currentTransition = GetCurrentTransition(machine, currentState, currentChar)

    if currentTransition == 0:   # Se não existe uma transição que combine, é rejeitado
        print("Palavra não suportada")
        exit()
    if currentTransition[2] == 'h':   # Se chegou no estado 'h', é o final da palavra, a palavra é aceita
        print("PALAVRA ACEITA!\n")
        halted = True
        continue

    # Caso a palavra não tenha sido rejeitada ou não tenha terminado
    # A instrução (read ou write) da transição atual é lida e executada
    currentInstruction = currentTransition[3]
    if currentInstruction == 'read':
        fila.pop(0)
    elif currentInstruction == 'write':
        fila.append(currentTransition[1])
    
    # Estado atual é atualizado para o próximo estado do autômato
    currentState = currentTransition[2]
    currentExecution += 1   # Incrementa a quantidade de execuções
    
    print(currentTransition[0],'->',currentTransition[2],'\t',fila)

    # Se o programa atingiu o limite de execuções, termina 
    if currentExecution >= int(execution):
        print("Número máximo de execuções atingido.\n")
        exit()
