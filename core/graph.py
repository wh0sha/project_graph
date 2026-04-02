import numpy as np

class Graph:
    def __init__(self, vertex: set, edge: set, incidence: set):
        self.vertex = vertex
        self.edge = edge
        self.incidence = incidence
        
        self.adjacency_list = {v: set() for v in self.vertex}
        for _, v1, v2 in self.incidence:
            self.adjacency_list[v1].add(v2)
            self.adjacency_list[v2].add(v1)
    
    # Граф из матрицы смежности
    @classmethod
    def from_adjacency_matrix(cls, matrix):
        matrix = np.array(matrix)
        rows = matrix.shape[0]

        vertex = set(range(rows))
        edge = set()
        incidence = set()

        edge_num = 0
        for i in range(rows):
            for j in range(i, rows):
                if matrix[i][j] != 0:
                    edge.add(edge_num)
                    incidence.add((edge_num, i, j))
                    edge_num += 1
        
        return cls(vertex, edge, incidence)

    # Граф из матрицы идентичности
    @classmethod
    def from_incidence_matrix(cls, matrix):
        matrix = np.array(matrix).T     # Транспонируем матрицу
        rows, cols = matrix.shape

        vertex = set(range(cols))
        edge = set()
        incidence = set()

        edge_num = 0
        for i in range(rows):
            connected_v = np.where(matrix[i] != 0)[0]
            if connected_v.size != 0:
                edge.add(edge_num)
                incidence.add((edge_num, int(connected_v[0]), int(connected_v[1])))
                edge_num += 1

        return cls(vertex, edge, incidence)
    
    # Граф из списка смежности
    @classmethod
    def from_adjacency_list(cls, list):
        rows = len(list)

        vertex = set(range(rows))
        edge = set()
        incidence = set()

        edge_num = 0
        for i in range(rows):
            for j in range(len(list[i])):
                if i < list[i][j]:
                    edge.add(edge_num)
                    incidence.add((edge_num, i, list[i][j]))
                    edge_num += 1

        return cls(vertex, edge, incidence)

    # Получение степени вершины
    def get_vertex_degree(self, vertex):
        return len(self.adjacency_list[vertex])

    # Вывод графа для проверки работы
    def __repr__(self):
        return f'G(V = {self.vertex}, R = {self.edge}, I = {self.incidence})'


# # ТЕСТЫ
# # Матрица смежности
# matrix = np.array([[0,1,1,1], 
#                    [1,0,1,0],
#                    [1,1,0,1],
#                    [1,0,1,0]])
# g = Graph.from_adjacency_matrix(matrix)
# print(g)

# # Матрица инцидентности
# matrix = np.array([[1,1,1,0,0], 
#                    [1,0,0,1,0],
#                    [0,1,0,1,1],
#                    [0,0,1,0,1]])
# g = Graph.from_incidence_matrix(matrix)
# print(g)

# # Список смежности
# adj_list = [[1,2,3],
#             [0,2],
#             [0,1,3],
#             [0,2]]
# g = Graph.from_adjacency_list(adj_list)
# print(g)