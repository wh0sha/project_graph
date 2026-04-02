from graph import *
from collections import deque

class Algorithms:
    def __init__(self):
        pass

    # Depth-First Search
    def dfs(graph, start_node, visited=None, path=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()

        visited.add(start_node)
        path.append(start_node)

        for new_node in graph.adjacency_list.get(start_node):
            if new_node not in visited:
                Algorithms.dfs(graph, new_node, visited, path)
        return path
    
    # Breadth-First Search
    def bfs(graph, start_node):
        pass

# ТЕСТЫ
matrix = np.array([[0, 1, 0, 0, 0], 
                   [1, 0, 0, 0, 0], 
                   [0, 0, 0, 1, 0], 
                   [0, 0, 1, 0, 1], 
                   [0, 0, 0, 1, 0]])
g = Graph.from_adjacency_matrix(matrix)
print(Algorithms.dfs(g, 4))
