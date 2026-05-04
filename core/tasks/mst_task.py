# core/tasks/mst_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class MSTTask(Task):
    """Задача 7: Минимальное остовное дерево (Алгоритм Прима)"""
    
    def __init__(self):
        super().__init__(7, "Минимальное остовное дерево (Прим)",
            "Найдите рёбра минимального остовного дерева (MST) графа. Алгоритм: <b>Прим</b>.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 7)
            matrix = [[0] * n for _ in range(n)]
            
            # 1. Строим случайное остовное дерево (гарантирует связность)
            for v in range(1, n):
                u = rng.randint(0, v - 1)
                w = rng.randint(1, 15)
                matrix[u][v] = w
                matrix[v][u] = w
                
            # 2. Добавляем случайные дополнительные рёбра с весами
            for _ in range(rng.randint(2, 4)):
                u, v = rng.sample(range(n), 2)
                if matrix[u][v] == 0:  # ребро ещё не существует
                    w = rng.randint(1, 15)
                    matrix[u][v] = w
                    matrix[v][u] = w
                    
            return Graph.from_adjacency_matrix(matrix)
        
        # Фиксированный взвешенный граф
        matrix = [
            [0,2,0,6,0],
            [2,0,3,8,5],
            [0,3,0,0,7],
            [6,8,0,0,9],
            [0,5,7,9,0]
        ]
        return Graph.from_adjacency_matrix(matrix)
    
    def get_solution(self, graph: Graph) -> dict:
        mst = Algorithms.prim_mst(graph, start=0)
        return {
            "edges": mst["edges"],
            "total_weight": mst["total_weight"],
            "explanation": f"MST вес: {mst['total_weight']}. Рёбра подсвечены на графе."
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Изучите выделенные рёбра MST."}