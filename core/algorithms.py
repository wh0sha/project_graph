# core/algorithms.py
import heapq
import bisect
from collections import deque, defaultdict
from typing import List, Dict, Set, Tuple, Optional
from .graph import Graph


class Algorithms:
    """
    Статические методы для алгоритмов на графах.
    Все методы принимают объект Graph и возвращают чистые данные (без побочных эффектов).
    """
    
    # ==================== ОБХОДЫ ====================
    
    @staticmethod
    def dfs(graph: Graph, start: int) -> List[int]:
        """Обход в глубину. Возвращает порядок посещения вершин."""
        visited = set()
        result = []
        
        def _dfs(v: int):
            visited.add(v)
            result.append(v)
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    _dfs(neighbor)
        
        if start in graph.vertex:
            _dfs(start)
        return result
    
    @staticmethod
    def bfs(graph: Graph, start: int) -> List[int]:
        """Обход в ширину. Возвращает порядок посещения вершин."""
        if start not in graph.vertex:
            return []
        visited = {start}
        queue = deque([start])
        result = [start]
        
        while queue:
            v = queue.popleft()
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result.append(neighbor)
                    queue.append(neighbor)
        return result
    
    @staticmethod
    def validate_traversal(graph: Graph, start: int, user_answer: List[int], 
                          algorithm: str = 'dfs') -> Dict:
        """
        Валидация ответа пользователя для DFS/BFS.
        Проверяет: полноту (все вершины), старт, и базовую корректность порядка.
        """
        if not user_answer:
            return {"correct": False, "feedback": "Пустой ответ"}
        if set(user_answer) != set(graph.vertex):
            missing = set(graph.vertex) - set(user_answer)
            extra = set(user_answer) - set(graph.vertex)
            msg = []
            if missing: msg.append(f"Не посещены: {sorted(missing)}")
            if extra: msg.append(f"Лишние вершины: {sorted(extra)}")
            return {"correct": False, "feedback": "; ".join(msg)}
        if user_answer[0] != start:
            return {"correct": False, "feedback": f"Обход должен начинаться с вершины {start}"}
        
        # Базовая проверка: для BFS — уровни, для DFS — допустимость перехода
        if algorithm == 'bfs':
            return Algorithms._validate_bfs_levels(graph, start, user_answer)
        return {"correct": True, "feedback": "Верно! ✓"}
    
    @staticmethod
    def _validate_bfs_levels(graph: Graph, start: int, user_answer: List[int]) -> Dict:
        """Строгая проверка порядка BFS по уровням."""
        from collections import deque
        visited = {start}
        queue = deque([(start, 0)])  # (vertex, level)
        levels = defaultdict(list)
        levels[0] = [start]
        
        while queue:
            v, lvl = queue.popleft()
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    levels[lvl + 1].append(neighbor)
                    queue.append((neighbor, lvl + 1))
        
        # Сопоставляем пользовательский порядок с уровнями
        user_idx = 1  # пропускаем start
        for lvl in sorted(levels.keys()):
            if lvl == 0: continue
            level_vertices = set(levels[lvl])
            user_level = set()
            while user_idx < len(user_answer) and user_answer[user_idx] in level_vertices:
                user_level.add(user_answer[user_idx])
                user_idx += 1
            if user_level != level_vertices:
                return {
                    "correct": False,
                    "feedback": f"Неверный порядок на уровне {lvl}. Ожидались: {sorted(level_vertices)}"
                }
        return {"correct": True, "feedback": "Верно! Порядок BFS корректен ✓"}
    
    # ==================== СВЯЗНОСТЬ ====================
    
    @staticmethod
    def find_connected_components(graph: Graph) -> List[List[int]]:
        """Находит все компоненты связности. Возвращает список списков вершин."""
        visited = set()
        components = []
        
        def _dfs(v: int, component: List[int]):
            visited.add(v)
            component.append(v)
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    _dfs(neighbor, component)
        
        for vertex in sorted(graph.vertex):
            if vertex not in visited:
                component = []
                _dfs(vertex, component)
                components.append(sorted(component))
        return components
    
    @staticmethod
    def count_connected_components(graph: Graph) -> int:
        """Возвращает количество компонент связности."""
        return len(Algorithms.find_connected_components(graph))
    
    @staticmethod
    def validate_components(graph: Graph, user_components: List[List[int]]) -> Dict:
        """Валидация разбиения на компоненты связности."""
        try:
            user_normalized = [sorted(c) for c in user_components]
            user_normalized = sorted(user_normalized, key=lambda x: (len(x), x[0] if x else -1))
            correct = Algorithms.find_connected_components(graph)
            correct_normalized = [sorted(c) for c in correct]
            correct_normalized = sorted(correct_normalized, key=lambda x: (len(x), x[0] if x else -1))
            
            if user_normalized == correct_normalized:
                return {"correct": True, "feedback": f"Верно! Найдено {len(correct)} компонент(ы) ✓"}
            else:
                return {
                    "correct": False,
                    "feedback": "Неверное разбиение. Проверьте связность внутри групп.",
                    "expected": correct
                }
        except Exception as e:
            return {"correct": False, "feedback": f"Ошибка формата: {str(e)}"}
    
    # ==================== ВЗВЕШЕННЫЕ АЛГОРИТМЫ ====================
    
    @staticmethod
    def prim_mst(graph: Graph, start: int = 0) -> Dict:
        """Алгоритм Прима для минимального остовного дерева."""
        if start not in graph.vertex:
            return {"edges": [], "total_weight": 0}
        
        adj = graph.get_weighted_adjacency()
        visited = {start}
        pq = []
        mst_edges = []
        
        for v, w in adj.get(start, []):
            heapq.heappush(pq, (w, start, v))
        
        while pq and len(visited) < len(graph.vertex):
            w, u, v = heapq.heappop(pq)
            if v in visited:
                continue
            visited.add(v)
            mst_edges.append({"from": u, "to": v, "weight": w})
            for next_v, next_w in adj.get(v, []):
                if next_v not in visited:
                    heapq.heappush(pq, (next_w, v, next_v))
        
        total = sum(e["weight"] for e in mst_edges)
        return {"edges": mst_edges, "total_weight": total}
    
    @staticmethod
    def dijkstra(graph: Graph, start: int = 0) -> Dict:
        """Алгоритм Дейкстры: кратчайшие пути от start до всех вершин."""
        adj = graph.get_weighted_adjacency()
        dist = {v: float('inf') for v in graph.vertex}
        prev = {v: None for v in graph.vertex}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj.get(u, []):
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
        
        return {"distances": dist, "predecessors": prev}
    
    @staticmethod
    def floyd_warshall(graph: Graph) -> Dict:
        """Алгоритм Флойд-Уоршелла: матрица кратчайших путей между всеми парами."""
        vertices = sorted(graph.vertex)
        n = len(vertices)
        idx = {v: i for i, v in enumerate(vertices)}
        dist = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
        
        adj = graph.get_weighted_adjacency()
        for u in adj:
            for v, w in adj[u]:
                dist[idx[u]][idx[v]] = min(dist[idx[u]][idx[v]], w)
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return {"matrix": dist, "vertices": vertices}
    
    # ==================== ПРЮФЕР ====================
    
    @staticmethod
    def pruefer_encode(graph: Graph) -> List[int]:
        """Кодирование дерева в последовательность Прюфера."""
        adj = {v: set() for v in graph.vertex}
        for _, u, v in graph.incidence:
            adj[u].add(v)
            adj[v].add(u)
        
        degree = {v: len(neighbors) for v, neighbors in adj.items()}
        leaves = sorted([v for v in graph.vertex if degree[v] == 1])
        sequence = []
        
        for _ in range(len(graph.vertex) - 2):
            if not leaves:
                break
            leaf = leaves.pop(0)
            neighbor = next(n for n in adj[leaf])
            sequence.append(neighbor)
            
            adj[leaf].discard(neighbor)
            adj[neighbor].discard(leaf)
            degree[neighbor] -= 1
            if degree[neighbor] == 1:
                bisect.insort(leaves, neighbor)
        return sequence
    
    @staticmethod
    def pruefer_decode(sequence: List[int], n: int) -> List[Tuple[int, int]]:
        """Декодирование последовательности Прюфера в дерево (список рёбер)."""
        if n <= 1:
            return []
        degree = [1] * n
        for x in sequence:
            if 0 <= x < n:
                degree[x] += 1
        
        leaves = [i for i in range(n) if degree[i] == 1]
        heapq.heapify(leaves)
        edges = []
        
        for u in sequence:
            if not leaves:
                break
            leaf = heapq.heappop(leaves)
            edges.append((leaf, u))
            degree[leaf] -= 1
            degree[u] -= 1
            if degree[u] == 1 and u < n:
                heapq.heappush(leaves, u)
        
        if len(leaves) >= 2:
            edges.append((leaves[0], leaves[1]))
        return edges
    
    # ==================== РАСКРАСКА ====================
    
    @staticmethod
    def greedy_coloring(graph: Graph) -> Dict[int, int]:
        """Жадная раскраска графа. Возвращает {вершина: цвет}."""
        colors = {}
        adj = {v: set(graph.get_neighbors(v)) for v in graph.vertex}
        
        for v in sorted(graph.vertex):
            used = {colors[u] for u in adj[v] if u in colors}
            c = 1
            while c in used:
                c += 1
            colors[v] = c
        return colors
    
    @staticmethod
    def validate_coloring(graph: Graph, user_colors: Dict[int, int]) -> Dict:
        """Проверка корректности раскраски: смежные вершины должны иметь разные цвета."""
        if set(user_colors.keys()) != graph.vertex:
            missing = graph.vertex - set(user_colors.keys())
            return {"correct": False, "feedback": f"Не раскрашены вершины: {sorted(missing)}"}
        
        for _, u, v in graph.incidence:
            if user_colors.get(u) == user_colors.get(v):
                return {"correct": False, "feedback": f"Конфликт: вершины {u} и {v} смежны, но цвет одинаковый"}
        
        num_colors = len(set(user_colors.values()))
        return {"correct": True, "feedback": f"Раскраска корректна! Использовано цветов: {num_colors} ✓"}