import random

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # Матрица смежности (нулевая)
        self.adj_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def set_matrix(self, matrix_data):
        """Принимает матрицу извне"""
        if len(matrix_data) != self.num_vertices:
            raise ValueError("Размер матрицы не совпадает!")
        self.adj_matrix = matrix_data

    def generate_random(self, density=0.5):
        """
        Генерирует случайный неориентированный граф.
        density: вероятность появления ребра (от 0 до 1)
        """
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                # Бросаем кубик: если выпало меньше density — ставим ребро
                if random.random() < density:
                    self.adj_matrix[i][j] = 1
                    self.adj_matrix[j][i] = 1  # Симметрия для неориентированного
                else:
                    self.adj_matrix[i][j] = 0
                    self.adj_matrix[j][i] = 0
        # Диагональ всегда 0 (нет петель)
        for i in range(self.num_vertices):
            self.adj_matrix[i][i] = 0

    def get_degrees(self):
        """Считает степени вершин"""
        return [sum(row) for row in self.adj_matrix]

    def to_json(self):
        """
        Преобразует граф в формат для vis.js 
        Возвращает словарь с узлами и ребрами
        """
        nodes = [{"id": i, "label": str(i + 1)} for i in range(self.num_vertices)]
        edges = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adj_matrix[i][j] == 1:
                    edges.append({"from": i, "to": j})
        return {"nodes": nodes, "edges": edges}

    # --- Заглушки для проверки (пока простые) ---
    def count_components(self):
        """Позже заменим на нормальный алгоритм из algorithms.py"""
        # Пока возвращаем 1 для теста
        return 1 

    def is_eulerian(self):
        """Граф эйлеров, если все степени четные"""
        degrees = self.get_degrees()
        return all(d % 2 == 0 for d in degrees)

    def is_bipartite(self):
        """Заглушка: пока всегда False, потом реализуем"""
        return False 