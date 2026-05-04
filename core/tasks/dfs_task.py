# core/tasks/dfs_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class DFSTaskShow(Task):
    """Задача 1: Показать порядок обхода в глубину (DFS)"""
    
    def __init__(self):
        super().__init__(1, "DFS — Показать",
            "Найдите порядок обхода графа в глубину, начиная с вершины <b>0</b>.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 7)
            adj = {v: [] for v in range(n)}
            # 1. Гарантируем связность через случайное остовное дерево
            for v in range(1, n):
                u = rng.randint(0, v-1)
                adj[u].append(v)
                adj[v].append(u)
            # 2. Добавляем случайные дополнительные рёбра
            for _ in range(rng.randint(1, n)):
                u, v = rng.sample(range(n), 2)
                if v not in adj[u]:
                    adj[u].append(v)
                    adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        # Фиксированный граф для обратной совместимости / демо
        return Graph.from_adjacency_matrix([
            [0,1,1,0],
            [1,0,1,1],
            [1,1,0,0],
            [0,1,0,0]
        ])
    
    def get_solution(self, graph: Graph) -> dict:
        order = Algorithms.dfs(graph, start=0)
        return {"order": order, "explanation": f"Порядок DFS: {' → '.join(map(str, order))}"}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Изучите решение и подсветку вершин."}


class DFSTaskCheck(Task):
    """Задача 2: Проверить введённый порядок DFS"""
    
    def __init__(self):
        super().__init__(2, "DFS — Проверить",
            "Введите порядок обхода в глубину, начиная с вершины <b>0</b> (числа через запятую).")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 6)
            adj = {v: [] for v in range(n)}
            for v in range(1, n):
                u = rng.randint(0, v-1)
                adj[u].append(v)
                adj[v].append(u)
            for _ in range(rng.randint(1, 3)):
                u, v = rng.sample(range(n), 2)
                if v not in adj[u]:
                    adj[u].append(v)
                    adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        return Graph.from_adjacency_matrix([
            [0,1,0,1],
            [1,0,1,0],
            [0,1,0,1],
            [1,0,1,0]
        ])
    
    def get_solution(self, graph: Graph) -> dict:
        order = Algorithms.dfs(graph, start=0)
        return {
            "order": order, 
            "explanation": f"Порядок DFS: {' → '.join(map(str, order))}",
            "animation_hint": "Вершины будут подсвечиваться по порядку обхода"
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        raw = user_input.get("order", "")
        try:
            user_order = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            return {"correct": False, "feedback": "Ошибка формата. Введите числа через запятую: 0, 1, 2, 3"}
        
        return Algorithms.validate_traversal(graph, start=0, user_answer=user_order, algorithm='dfs')