# core/tasks/connectivity_task.py
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms
import re

class ConnectivityTaskShow(Task):
    """Задача 5: Показать компоненты связности"""
    
    def __init__(self):
        super().__init__(5, "Компоненты связности — Показать",
            "Определите количество компонент связности графа и их состав.")
    
    def generate_graph(self) -> Graph:
        # Граф с 3 компонентами: {0,1}, {2,3,4}, {5}
        adj = {0: [1], 1: [0], 2: [3,4], 3: [2,4], 4: [2,3], 5: []}
        return Graph.from_adjacency_list(adj)
    
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
    
    def generate_graph(self) -> Graph:
        # Граф с 2 компонентами: {0,1,2}, {3,4}
        adj = {0: [1,2], 1: [0,2], 2: [0,1], 3: [4], 4: [3]}
        return Graph.from_adjacency_list(adj)
    
    def get_solution(self, graph: Graph) -> dict:
        comps = Algorithms.find_connected_components(graph)
        return {"components": comps, "count": len(comps)}
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            raw = user_input.get("components", "").strip()
            # Извлекаем содержимое квадратных скобок
            groups = re.findall(r'\[([^\]]+)\]', raw)
            parsed = []
            for g in groups:
                nums = [int(x.strip()) for x in g.split(',') if x.strip()]
                parsed.append(nums)
            return Algorithms.validate_components(graph, parsed)
        except Exception:
            return {"correct": False, "feedback": "Ошибка формата. Пример: [0,1], [2,3]"}