# core/tasks/mst_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class MSTTask(Task):
    """Задача 7: Минимальное остовное дерево (Алгоритм Прима)"""
    
    def __init__(self):
        super().__init__(7, "Минимальное остовное дерево (Прим)",
            "Найдите рёбра минимального остовного дерева (MST) графа. Алгоритм: <b>Прим</b>.")
    
    def generate_graph(self) -> Graph:
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