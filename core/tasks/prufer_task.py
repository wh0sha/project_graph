# core/tasks/prufer_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms
import re

class PrueferEncodeTask(Task):
    """Задача 10: Кодирование дерева в последовательность Прюфера"""
    
    def __init__(self):
        super().__init__(10, "Кодирование Прюфера",
            "Дано помеченное дерево. Введите последовательность Прюфера (числа через запятую).")
    
    def generate_graph(self) -> Graph:
        # Дерево: 0-1, 0-2, 0-3, 2-4
        adj = {0:[1,2,3], 1:[0], 2:[0,4], 3:[0], 4:[2]}
        return Graph.from_adjacency_list(adj)
    
    def get_solution(self, graph: Graph) -> dict:
        seq = Algorithms.pruefer_encode(graph)
        return {"sequence": seq, "explanation": f"Код Прюфера: {seq}"}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            user_seq = [int(x.strip()) for x in user_input.get("sequence", "").split(",") if x.strip()]
        except ValueError:
            return {"correct": False, "feedback": "Ошибка формата. Пример: 0, 0, 2"}
        
        correct_seq = Algorithms.pruefer_encode(graph)
        if user_seq == correct_seq:
            return {"correct": True, "feedback": "Верно! ✓"}
        return {"correct": False, "feedback": "Неверная последовательность."}


class PrueferDecodeTask(Task):
    """Задача 11: Декодирование последовательности Прюфера в дерево"""
    
    def __init__(self):
        super().__init__(11, "Декодирование Прюфера",
            "Дана последовательность: <b>[1, 2, 2]</b>. Введите рёбра восстановленного дерева в формате <code>(u,v)</code> через запятую.")
        self.sequence = [1, 2, 2]
        self.n = 5
    
    def generate_graph(self) -> Graph:
        edges = Algorithms.pruefer_decode(self.sequence, self.n)
        adj = {i: [] for i in range(self.n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        return Graph.from_adjacency_list(adj)
    
    def get_solution(self, graph: Graph) -> dict:
        edges = Algorithms.pruefer_decode(self.sequence, self.n)
        return {"sequence": self.sequence, "edges": edges}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            raw = user_input.get("edges", "").strip()
            matches = re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*\)', raw)
            if not matches:
                return {"correct": False, "feedback": "Не найдено рёбер в формате (u,v)"}
            
            user_edges = [(int(u), int(v)) for u, v in matches]
            user_norm = sorted([tuple(sorted(e)) for e in user_edges])
            correct_edges = Algorithms.pruefer_decode(self.sequence, self.n)
            correct_norm = sorted([tuple(sorted(e)) for e in correct_edges])
            
            if user_norm == correct_norm:
                return {"correct": True, "feedback": "Дерево восстановлено верно! ✓"}
            return {"correct": False, "feedback": "Неверный набор рёбер."}
        except Exception:
            return {"correct": False, "feedback": "Ошибка формата. Пример: (0,1), (1,2), (2,3), (0,3)"}