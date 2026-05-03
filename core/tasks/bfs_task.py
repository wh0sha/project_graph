# core/tasks/bfs_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class BFSTaskShow(Task):
    """Задача 3: Показать порядок обхода в ширину (BFS)"""
    
    def __init__(self):
        super().__init__(3, "BFS — Показать",
            "Найдите порядок обхода графа в ширину, начиная с вершины <b>0</b>.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 7)
            adj = {v: [] for v in range(n)}
            # Остовное дерево + дополнительные рёбра
            for v in range(1, n):
                u = rng.randint(0, v-1)
                adj[u].append(v)
                adj[v].append(u)
            for _ in range(rng.randint(1, n//2)):
                u, v = rng.sample(range(n), 2)
                if v not in adj[u]:
                    adj[u].append(v)
                    adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        return Graph.from_adjacency_matrix([
            [0,1,1,0,0],
            [1,0,0,1,0],
            [1,0,0,1,1],
            [0,1,1,0,0],
            [0,0,1,0,0]
        ])
    
    def get_solution(self, graph: Graph) -> dict:
        order = Algorithms.bfs(graph, start=0)
        return {"order": order, "explanation": f"Порядок BFS: {' → '.join(map(str, order))}"}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Изучите решение и уровни обхода."}


class BFSTaskCheck(Task):
    """Задача 4: Проверить введённый порядок BFS"""
    
    def __init__(self):
        super().__init__(4, "BFS — Проверить",
            "Введите порядок обхода в ширину, начиная с вершины <b>0</b> (числа через запятую).")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 6)
            adj = {v: [] for v in range(n)}
            for v in range(1, n):
                u = rng.randint(0, v-1)
                adj[u].append(v)
                adj[v].append(u)
            for _ in range(rng.randint(1, 2)):
                u, v = rng.sample(range(n), 2)
                if v not in adj[u]:
                    adj[u].append(v)
                    adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        return Graph.from_adjacency_matrix([
            [0,1,1,0,0],
            [1,0,0,1,1],
            [1,0,0,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0]
        ])
    
    def get_solution(self, graph: Graph) -> dict:
        order = Algorithms.bfs(graph, start=0)
        return {"order": order}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        raw = user_input.get("order", "")
        try:
            user_order = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            return {"correct": False, "feedback": "Ошибка формата. Введите числа через запятую: 0, 1, 2, 3"}
        
        return Algorithms.validate_traversal(graph, start=0, user_answer=user_order, algorithm='bfs')