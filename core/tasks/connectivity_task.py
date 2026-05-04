# core/tasks/connectivity_task.py
import re
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class ConnectivityTaskShow(Task):
    """Задача 5: Показать компоненты связности"""
    
    def __init__(self):
        super().__init__(5, "Компоненты связности — Показать",
            "Определите количество компонент связности графа и их состав.")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 8)
            adj = {v: [] for v in range(n)}
            # Генерируем случайные рёбра с низкой вероятностью, чтобы граф часто был несвязным
            for u in range(n):
                for v in range(u + 1, n):
                    if rng.random() < 0.25:
                        adj[u].append(v)
                        adj[v].append(u)
            # Гарантируем хотя бы одно ребро, если вершин > 1
            if n > 1 and not any(adj[u] for u in adj):
                u, v = rng.sample(range(n), 2)
                adj[u].append(v)
                adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        # Фиксированный граф: 3 компоненты {0,1}, {2,3,4}, {5}
        return Graph.from_adjacency_list({0: [1], 1: [0], 2: [3,4], 3: [2,4], 4: [2,3], 5: []})
    
    def get_solution(self, graph: Graph) -> dict:
        comps = Algorithms.find_connected_components(graph)
        return {
            "count": len(comps),
            "components": comps,
            "explanation": f"Найдено {len(comps)} компонент(ы): " + 
                          "; ".join(f"{{{', '.join(map(str, c))}}}" for c in comps)
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        return {"correct": True, "feedback": "Ознакомительная задача. Изучите компоненты выше."}


class ConnectivityTaskCheck(Task):
    """Задача 6: Проверить ввод компонент связности"""
    
    def __init__(self):
        super().__init__(6, "Компоненты связности — Проверить",
            "Введите компоненты связности в формате: <code>[0,1], [2,3]</code> (группы через запятую).")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 7)
            adj = {v: [] for v in range(n)}
            for u in range(n):
                for v in range(u + 1, n):
                    if rng.random() < 0.3:
                        adj[u].append(v)
                        adj[v].append(u)
            if n > 1 and not any(adj[u] for u in adj):
                u, v = rng.sample(range(n), 2)
                adj[u].append(v)
                adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        # Фиксированный граф: 2 компоненты {0,1,2}, {3,4}
        return Graph.from_adjacency_list({0: [1,2], 1: [0,2], 2: [0,1], 3: [4], 4: [3]})
    
    def get_solution(self, graph: Graph) -> dict:
        comps = Algorithms.find_connected_components(graph)
        return {"components": comps, "count": len(comps)}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            raw = user_input.get("components", "").strip()
            groups = re.findall(r'\[([^\]]+)\]', raw)
            parsed = []
            for g in groups:
                nums = [int(x.strip()) for x in g.split(',') if x.strip()]
                parsed.append(nums)
            return Algorithms.validate_components(graph, parsed)
        except Exception:
            return {"correct": False, "feedback": "Ошибка формата. Пример: [0,1], [2,3]"}