# core/tasks/coloring_task.py
import random
from typing import Optional
from .base import Task
from ..graph import Graph
from ..algorithms import Algorithms

class ColoringTask(Task):
    """Задача 12: Раскраска графа (Жадный алгоритм)"""
    
    def __init__(self):
        super().__init__(12, "Раскраска графа",
            "Раскрасьте вершины графа так, чтобы смежные вершины имели <b>разные цвета</b>. "
            "Введите цвета как последовательность чисел: <code>цвет_0, цвет_1, цвет_2, ...</code>")
    
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        if seed is not None:
            rng = random.Random(seed)
            n = rng.randint(5, 7)
            adj = {v: [] for v in range(n)}
            for u in range(n):
                for v in range(u + 1, n):
                    if rng.random() < 0.4:
                        adj[u].append(v)
                        adj[v].append(u)
            if n > 1 and not any(adj[u] for u in adj):
                u, v = rng.sample(range(n), 2)
                adj[u].append(v)
                adj[v].append(u)
            return Graph.from_adjacency_list(adj)
        
        adj = {0:[1,4,2], 1:[0,2], 2:[1,3,0], 3:[2,4], 4:[3,0]}
        return Graph.from_adjacency_list(adj)
    
    def get_solution(self, graph: Graph) -> dict:
        colors = Algorithms.greedy_coloring(graph)
        # 🔹 Формируем строку-подсказку: "вершина 0 → цвет 1, вершина 1 → цвет 2, ..."
        hint_parts = [f"{v}→{c}" for v, c in sorted(colors.items())]
        return {
            "colors": colors, 
            "num_colors": max(colors.values()) if colors else 0,
            "explanation": f"Жадная раскраска: {len(set(colors.values()))} цветов",
            "example_input": ", ".join(str(colors[v]) for v in sorted(colors.keys())),
            "vertex_colors_hint": ", ".join(hint_parts)
        }
    
    def check_answer(self, graph: Graph, user_input: dict) -> dict:
        try:
            raw = user_input.get("colors", "").strip()
            if not raw:
                return {"correct": False, "feedback": "⚠️ Поле ввода пустое. Введите цвета вершин."}
            
            # Парсим: "1, 2, 1, 2, 3" → {0:1, 1:2, 2:1, 3:2, 4:3}
            values = [x.strip() for x in raw.split(",") if x.strip()]
            if not values:
                return {"correct": False, "feedback": "⚠️ Не удалось распознать числа. Пример: 1, 2, 1, 2, 3"}
                
            user_colors = {i: int(v) for i, v in enumerate(values)}
            
            # 🔹 Проверка количества
            expected_count = len(graph.vertex)
            if len(user_colors) != expected_count:
                return {
                    "correct": False, 
                    "feedback": f"⚠️ Ожидалось {expected_count} цветов (по одному для вершин 0–{expected_count-1}), а введено {len(user_colors)}.",
                    "expected_count": expected_count,
                    "example": ", ".join(str(i) for i in range(min(5, expected_count))) + ("..." if expected_count > 5 else "")
                }
            
            # 🔹 Проверка корректности раскраски
            for _, u, v in graph.incidence:
                if user_colors.get(u) == user_colors.get(v):
                    return {
                        "correct": False, 
                        "feedback": f"❌ Конфликт: вершины {u} и {v} соединены ребром, но имеют одинаковый цвет ({user_colors[u]}).",
                        "conflict_edge": (u, v),
                        "conflict_color": user_colors[u]
                    }
            
            # 🔹 Успех
            num_used = len(set(user_colors.values()))
            optimal = Algorithms.greedy_coloring(graph)
            optimal_count = len(set(optimal.values()))
            bonus = f" 🎯 Использовано {num_used} цветов" + (f" (оптимум: {optimal_count})" if num_used == optimal_count else f", можно попробовать {optimal_count}")
            
            return {
                "correct": True, 
                "feedback": f"✅ Раскраска корректна!{bonus}",
                "colors_used": num_used
            }
            
        except ValueError as e:
            return {
                "correct": False, 
                "feedback": f"⚠️ Ошибка формата: введите только целые числа через запятую. Пример: 1, 2, 1, 2, 3",
                "example": "1, 2, 1, 2, 3"
            }
        except Exception as e:
            return {"correct": False, "feedback": f"⚠️ Неизвестная ошибка: {str(e)}"}