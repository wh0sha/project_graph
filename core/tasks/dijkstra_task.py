# core/tasks/dijkstra_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class DijkstraTask(Task):
    """Задача 8: Кратчайшие пути (Алгоритм Дейкстры)"""
    
    def __init__(self):
        super().__init__(8, "Кратчайшие пути (Дейкстра)",
            "Найдите кратчайшие расстояния от вершины <b>0</b> до всех остальных.")
    
    def generate_graph(self) -> Graph:
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