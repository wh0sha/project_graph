# core/tasks/task_0.py
from typing import Optional
from .base import Task
from ..graph import Graph

class Task0(Task):
    """Задача 0: Введение. Только ознакомление, без проверки."""
    
    def __init__(self):
        super().__init__(0, "Введение",
            "👋 Добро пожаловать! Это ознакомительная задача. "
            "Изучите граф: перетаскивайте вершины, масштабируйте. "
            "Когда будете готовы — переходите к Задаче 1.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        return Graph.from_adjacency_list({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    
    def get_solution(self, graph: Graph) -> dict:
        return {
            "message": "✅ Это неориентированный граф с 3 вершинами и 3 рёбрами.",
            "stats": {"vertices": len(graph.vertex), "edges": len(graph.edge)},
            "tip": "💡 В задачах 1–4 вы будете вводить порядок обхода вершин (например: 0, 1, 2, 3)"
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        # 🔹 Задача 0 не проверяет ответ — всегда "информация"
        return {
            "correct": True, 
            "feedback": "🎯 Ознакомительная задача — переходите к следующей!",
            "info_only": True  # Флаг для frontend, чтобы скрыть поле ввода
        }