### On importe les libraires, classes

import random
import simpy
import utils
from node import Node

### On crée l'environement simpy et le pipe pour le cannal de communication

env = simpy.Environment()
pipe = simpy.Store(env)

### TEST CREATION D'UN ANNEAU, RETRAIT ET AJOUT DE NOEUDS.

ring = [] # Ensemble des noeuds de l'anneau
#idSet = [] # Ensemble des ID des noeuds, on n'autorise pas d'avoir 2 noeuds de même ID

# On crée trois noeuds
node1 = Node(env, pipe, 1)
node2 = Node(env, pipe, 4)
node3 = Node(env, pipe, 7)
ring.append(node1)
ring.append(node2)
ring.append(node3)

# On les relie

node1.setPrev(node3)
node1.setNext(node2)

node2.setPrev(node1)
node2.setNext(node3)

node3.setPrev(node2)
node3.setNext(node1)

# A noter qu'on pourrait utiliser ce code :
"""node2.join(ring)
node3.join(ring)"""

# On vérifie que tout a bien été fait

utils.printGraph(ring)

# On rajoute un nouveau noeud d'ID 6

newNode = Node(env, pipe, 6)
randomNode = ring[random.randint(0, len(ring) - 1)]
randomNode.join(newNode)
ring.append(newNode)

utils.printGraph(ring)

# On fait quitter le node1 (ID= 1)

node1.leave(ring)
utils.printGraph(ring)

### ENVOIE ET RECEPTION DE MESSAGES

# Chaque nœud envoie un message à son voisin de droite (suivant)
for i in range(len(ring)):
    sender = ring[i]
    receiver = ring[i].getNext()
    #sender.sendMessage(receiver.getID(), f'What\'s up')

# Pour tester pour des chemins plus long

node2.sendMessage(7, "test")
newNode.sendMessage(6, "test")


# Chaque nœud reçoit un message de son voisin de gauche (précédent)
for i in range(len(ring)):
    env.process(ring[i].receiveMessages())


### AJOUT DE DONNEES

def testData():
        newNode.put(70)
        yield env.timeout(random.randint(1, 3))
        newNode.get(70)
        newNode.get(552)

env.process(testData())

env.run(until=env.now + 100)

for i in range(len(ring)):
    print(ring[i].id)
    ring[i].printDataIDs()

