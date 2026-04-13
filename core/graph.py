import numpy as np
import random

class Graph:
    def __init__(self, num_vertices=0):
        """
        Инициализация графа.
        num_vertices — для совместимости с твоим бэкендом.
        """
        self.num_vertices = num_vertices  
        self.n = num_vertices            
        
        # Твоя матрица смежности (нужна для твоего бэкенда)
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        
        # Его структура данных
        self.vertex = set(range(num_vertices))
        self.edge = set()
        self.incidence = set()
        self.adjacency_list = {}

    # немного исправил твои методы
    
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
        
        graph = cls(n)
        graph.vertex = vertex
        graph.edge = edge
        graph.incidence = incidence
        graph.adj_matrix = matrix.tolist()  
        return graph

    @classmethod
    def from_incidence_matrix(cls, matrix):
        """заглишка надо будет дописать"""
        pass

    @classmethod
    def from_adjacency_list(cls, adj_list):
        """заглишка надо будет дописать"""
        pass

    def __repr__(self):
        return f'G(V={self.vertex}, E={self.edge}, I={self.incidence})'

    
    def set_matrix(self, matrix_data):
        """принимает матрицу извне"""
        if isinstance(matrix_data, np.ndarray):
            matrix_data = matrix_data.tolist()
        
        if len(matrix_data) != self.num_vertices:
            self.num_vertices = len(matrix_data)
        
        self.adj_matrix = matrix_data
        # обновляем numpy версию
        self.n = len(matrix_data)

    def generate_random(self, density=0.5):
        """генерирует случайный граф """
        n = self.num_vertices
        self.adj_matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < density:
                    self.adj_matrix[i][j] = 1
                    self.adj_matrix[j][i] = 1
        
        # обновляем его структуру
        self.vertex = set(range(n))
        self.edge = set()
        self.incidence = set()
        edge_num = 0
        for i in range(n):
            for j in range(i, n):
                if self.adj_matrix[i][j] == 1:
                    self.edge.add(edge_num)
                    self.incidence.add((edge_num, i, j))
                    edge_num += 1

    def get_degrees(self):
        """считает степени вершин """
        return [sum(row) for row in self.adj_matrix]

    def to_json(self):
        """для vis.js """
        nodes = [{"id": i, "label": str(i + 1)} for i in range(self.num_vertices)]
        edges = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] == 1:
                    edges.append({"from": i, "to": j})
        return {"nodes": nodes, "edges": edges}

    def is_eulerian(self):
        """проверка на эйлеровость"""
        degrees = self.get_degrees()
        return all(d % 2 == 0 for d in degrees)

    def is_bipartite(self):
        """проверка на двудольность (заглушка)"""
        return False