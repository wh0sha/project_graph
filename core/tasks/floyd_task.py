# core/tasks/floyd_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class FloydTask(Task):
    """Задача 9: Матрица кратчайших путей (Алгоритм Флойд-Уоршелла)"""
    
    def __init__(self):
        super().__init__(9, "Матрица кратчайших путей (Флойд-Уоршелл)",
            "Постройте матрицу кратчайших путей между всеми парами вершин.")
    
    def generate_graph(self) -> Graph:
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