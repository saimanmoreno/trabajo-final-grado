# diseñar una red de 6 nodos y encontrar todos los posibles 
# caminos entre un nodo origen y un nodo destino

import networkx
import matplotlib.pyplot as plt

graph = networkx.Graph()

graph.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f'])

graph.add_edges_from([
    ('a', 'b'), ('a', 'c'), ('b', 'e'), 
    ('b', 'd'), ('c', 'f'), ('a', 'f')
])

source = input('Enter the source node >> ')
target = input('Enter the target node >> ')

print('Todos los caminos posibles de nodo %s para nodo %s: ' %(source, target))
for path in networkx.all_simple_paths(graph, source, target):
    print(path)

networkx.draw(graph, with_labels=True, font_weight='bold')
plt.show()

edges = list(graph.edges())

for n in range(len(edges)):
    print(edges)

print(edges[1])