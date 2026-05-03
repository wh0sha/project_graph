# core/tasks/task_0.py
from typing import Optional
from .base import Task
from ..graph import Graph

class Task0(Task):
    """Задача 0: Введение. Базовое знакомство с графом."""
    
    def __init__(self):
        super().__init__(0, "Введение",
            "Добро пожаловать! Изучите базовое представление графа: "
            "вершины (круги) и рёбра (линии). Перетаскивайте узлы, чтобы понять структуру.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        # Для вводной задачи граф фиксированный, seed не используется
        return Graph.from_adjacency_list({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    
    def get_solution(self, graph: Graph) -> dict:
        return {
            "message": "Это неориентированный граф с 3 вершинами и 3 рёбрами.",
            "stats": {"vertices": len(graph.vertex), "edges": len(graph.edge)}
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Ознакомительная задача. Переходите к следующим!"}