import numpy as np

class Graph:
    def __init__(self, vertex: set = {}, edge: set = {}, incidence: set = {}):
        self.vertex = vertex
        self.edge = edge
        self.incidence = incidence
        self.adjacency_list = {}
    
    @classmethod
    def from_adjacency_matrix(cls, matrix):
        matrix = np.array(matrix)
        n = matrix.shape[0]

        vertex = set(range(n))
        edge = set()
        incidence = set()

        edge_num = 0
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] != 0:
                    edge.add(edge_num)
                    incidence.add((edge_num, i, j))
                    edge_num += 1
        
        return cls(vertex, edge, incidence)

    @classmethod
    def from_incidence_matrix(cls, matrix):
        matrix = np.array(matrix)
        rows, cols = matrix.shape

        vertex = set(range(rows))
        edge = set()
        incidence = set()

        for i in range(rows):
            not_null = np.where(matrix[i] != 0)[0]
            
            edge.add()
            pass
    
    @classmethod
    def from_adjacency_list(cls, list):
        pass

    def __repr__(self):
        return f'G(V={self.vertex}, R={self.edge}, I={self.incidence})'

matrix = np.array([[1,1,0,0], 
                   [1,0,1,1],
                   [0,0,0,1],
                   [0,1,1,0]])
# g = Graph.from_adjacency_matrix(matrix)
for i in range(matrix.shape[0]):
    print(np.where(matrix[i] != 0))