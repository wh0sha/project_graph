# core/tasks/dijkstra_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class DijkstraTask(Task):
    """Задача 8: Кратчайшие пути (Алгоритм Дейкстры)"""
    
    def __init__(self):
        super().__init__(8, "Кратчайшие пути (Дейкстра)",
            "Найдите кратчайшие расстояния от вершины <b>0</b> до всех остальных.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(4, 6)
            matrix = [[0] * n for _ in range(n)]
            
            # 1. Остовное дерево для связности
            for v in range(1, n):
                u = rng.randint(0, v - 1)
                w = rng.randint(1, 20)
                matrix[u][v] = w
                matrix[v][u] = w
                
            # 2. Дополнительные рёбра (альтернативные пути)
            for _ in range(rng.randint(1, 3)):
                u, v = rng.sample(range(n), 2)
                if matrix[u][v] == 0:
                    w = rng.randint(1, 20)
                    matrix[u][v] = w
                    matrix[v][u] = w
                    
            return Graph.from_adjacency_matrix(matrix)
        
        # Фиксированный взвешенный граф
        matrix = [
            [0,4,0,0,0],
            [4,0,8,0,0],
            [0,8,0,7,4],
            [0,0,7,0,5],
            [0,0,4,5,0]
        ]
        return Graph.from_adjacency_matrix(matrix)
    
    def get_solution(self, graph: Graph) -> dict:
        res = Algorithms.dijkstra(graph, start=0)
        return {
            "distances": res["distances"],
            "explanation": "Расстояния от вершины 0: " + 
                          ", ".join(f"{v}→{d}" for v,d in sorted(res['distances'].items()))
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Проверьте таблицу расстояний ниже."}