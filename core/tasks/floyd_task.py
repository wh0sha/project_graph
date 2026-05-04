# core/tasks/floyd_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class FloydTask(Task):
    """Задача 9: Матрица кратчайших путей (Алгоритм Флойд-Уоршелла)"""
    
    def __init__(self):
        super().__init__(9, "Матрица кратчайших путей (Флойд-Уоршелл)",
            "Постройте матрицу кратчайших путей между всеми парами вершин.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(4, 6)
            matrix = [[0] * n for _ in range(n)]
            
            # 1. Остовное дерево гарантирует связность графа
            for v in range(1, n):
                u = rng.randint(0, v - 1)
                w = rng.randint(1, 10)
                matrix[u][v] = w
                matrix[v][u] = w
                
            # 2. Дополнительные рёбра для альтернативных путей
            for _ in range(rng.randint(1, n)):
                u, v = rng.sample(range(n), 2)
                if matrix[u][v] == 0:
                    w = rng.randint(1, 10)
                    matrix[u][v] = w
                    matrix[v][u] = w
                    
            return Graph.from_adjacency_matrix(matrix)
        
        # Фиксированный граф для обратной совместимости
        matrix = [
            [0,3,0,7],
            [8,0,2,0],
            [5,0,0,1],
            [2,0,0,0]
        ]
        return Graph.from_adjacency_matrix(matrix)
    
    def get_solution(self, graph: Graph) -> dict:
        res = Algorithms.floyd_warshall(graph)
        return {"matrix": res["matrix"], "vertices": res["vertices"]}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Изучите итоговую матрицу расстояний."}