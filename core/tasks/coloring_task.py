# core/tasks/coloring_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class ColoringTask(Task):
    """Задача 12: Раскраска графа (Жадный алгоритм)"""
    
    def __init__(self):
        super().__init__(12, "Раскраска графа",
            "Введите цвета вершин (числа через запятую, начиная с 0). Смежные вершины должны иметь разные цвета.")
    
    def generate_graph(self) -> Graph:
        # Граф C5 с хордой (требует 3 цвета)
        adj = {0:[1,4,2], 1:[0,2], 2:[1,3,0], 3:[2,4], 4:[3,0]}
        return Graph.from_adjacency_list(adj)
    
    def get_solution(self, graph: Graph) -> dict:
        colors = Algorithms.greedy_coloring(graph)
        return {"colors": colors, "num_colors": max(colors.values()) if colors else 0}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            raw = user_input.get("colors", "")
            user_colors = {i: int(x.strip()) for i, x in enumerate(raw.split(",")) if x.strip()}
            if len(user_colors) != len(graph.vertex):
                return {"correct": False, "feedback": f"Нужно ввести {len(graph.vertex)} цветов (для вершин 0-{len(graph.vertex)-1})."}
            return Algorithms.validate_coloring(graph, user_colors)
        except ValueError:
            return {"correct": False, "feedback": "Ошибка формата. Пример: 1, 2, 1, 2, 3"}