# core/graph.py
import numpy as np
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional, Union


class Graph:
    """
    Представление неориентированного графа.
    Поддерживает: матрицу смежности, список инцидентности, список смежности, веса рёбер.
    """
    
    def __init__(
        self,
        vertex: Optional[Set[int]] = None,
        edge: Optional[Set[int]] = None,
        incidence: Optional[Set[Tuple[int, int, int]]] = None,
        weights: Optional[Dict[int, float]] = None
    ):
        self.vertex = vertex or set()
        self.edge = edge or set()
        self.incidence = incidence or set()  # {(edge_id, u, v)}
        self.weights = weights or {}         # {edge_id: weight}
        self._adjacency_list: Optional[Dict[int, Set[int]]] = None
    
    @classmethod
    def from_adjacency_matrix(cls, matrix: Union[List[List], np.ndarray]) -> 'Graph':
        """Создание графа из матрицы смежности (неориентированный, с весами)."""
        matrix = np.array(matrix)
        n = matrix.shape[0]
        vertex = set(range(n))
        edge = set()
        incidence = set()
        weights = {}
        edge_num = 0
        
        for i in range(n):
            for j in range(i, n):  # верхний треугольник для неориентированного
                w = matrix[i][j]
                if w != 0:
                    edge.add(edge_num)
                    incidence.add((edge_num, i, j))
                    weights[edge_num] = float(w)
                    edge_num += 1
        return cls(vertex, edge, incidence, weights)
    
    @classmethod
    def from_incidence_matrix(cls, matrix: Union[List[List], np.ndarray]) -> 'Graph':
        """Создание графа из матрицы инцидентности."""
        matrix = np.array(matrix)
        rows, cols = matrix.shape
        vertex = set(range(rows))
        edge = set()
        incidence = set()
        weights = {}
        
        for e in range(cols):
            endpoints = np.where(matrix[:, e] != 0)[0]
            if len(endpoints) == 2:
                u, v = int(endpoints[0]), int(endpoints[1])
                edge.add(e)
                incidence.add((e, u, v))
                # Вес = абсолютное значение (для знаковой инцидентности)
                weights[e] = abs(matrix[endpoints[0], e])
        return cls(vertex, edge, incidence, weights)
    
    @classmethod
    def from_adjacency_list(cls, adj_list: Dict[int, List[int]], 
                           weights: Optional[Dict[Tuple[int,int], float]] = None) -> 'Graph':
        """Создание графа из списка смежности {vertex: [neighbors]}."""
        vertex = set(adj_list.keys())
        edge = set()
        incidence = set()
        edge_weights = {}
        edge_num = 0
        seen = set()
        
        for v in adj_list:
            for u in adj_list[v]:
                pair = tuple(sorted((v, u)))
                if pair not in seen:
                    seen.add(pair)
                    edge.add(edge_num)
                    incidence.add((edge_num, pair[0], pair[1]))
                    if weights and pair in weights:
                        edge_weights[edge_num] = weights[pair]
                    edge_num += 1
        return cls(vertex, edge, incidence, edge_weights)
    
    @property
    def adjacency_list(self) -> Dict[int, Set[int]]:
        """Ленивое вычисление списка смежности (без весов)."""
        if self._adjacency_list is None:
            adj = defaultdict(set)
            for _, u, v in self.incidence:
                adj[u].add(v)
                adj[v].add(u)
            self._adjacency_list = dict(adj)
        return self._adjacency_list
    
    def to_adjacency_list(self) -> Dict[int, List[int]]:
        """Публичный метод: возвращает список смежности как {v: [neighbors]}."""
        return {v: sorted(list(neighbors)) for v, neighbors in self.adjacency_list.items()}
    
    def get_weighted_adjacency(self) -> Dict[int, List[Tuple[int, float]]]:
        """Возвращает {v: [(neighbor, weight), ...]} для взвешенных алгоритмов."""
        adj = defaultdict(list)
        for eid, u, v in self.incidence:
            w = self.weights.get(eid, 1.0)
            adj[u].append((v, w))
            adj[v].append((u, w))
        return {v: sorted(neighbors) for v, neighbors in adj.items()}
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Возвращает отсортированный список соседей вершины."""
        return sorted(list(self.adjacency_list.get(vertex, [])))
    
    def is_connected(self) -> bool:
        """Проверяет, связен ли граф (через BFS от произвольной вершины)."""
        if not self.vertex:
            return True
        start = next(iter(self.vertex))
        visited = set()
        from collections import deque
        queue = deque([start])
        visited.add(start)
        
        while queue:
            v = queue.popleft()
            for neighbor in self.get_neighbors(v):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited == self.vertex
    
    def to_vis_format(self) -> Dict[str, List[Dict]]:
        """Конвертация в формат vis.js: {nodes: [...], edges: [...]}."""
        nodes = [{"id": int(v), "label": str(v)} for v in sorted(self.vertex)]
        edges = []
        for eid, u, v in self.incidence:
            edge_data = {"id": int(eid), "from": int(u), "to": int(v)}
            w = self.weights.get(eid)
            if w is not None and w != 1:
                edge_data["label"] = str(int(w) if w == int(w) else w)
            edges.append(edge_data)
        return {"nodes": nodes, "edges": edges}
    
    def copy(self) -> 'Graph':
        """Возвращает глубокую копию графа."""
        return Graph(
            vertex=self.vertex.copy(),
            edge=self.edge.copy(),
            incidence=self.incidence.copy(),
            weights=self.weights.copy()
        )
    
    def __repr__(self):
        return f'Graph(V={len(self.vertex)}, E={len(self.edge)}, connected={self.is_connected()})'