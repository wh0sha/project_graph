from core.graph import Graph
from collections import deque

class Algorithms:
    
    @staticmethod
    def dfs(graph: Graph, start: int):
        """
        Поиск в глубину (возвращает список вершин в порядке обхода)
        """
        visited = [False] * graph.num_vertices
        result = []
        
        def _dfs(v):
            visited[v] = True
            result.append(v)
            # Обходим соседей по порядку (для детерминированности)
            for i in range(graph.num_vertices):
                if graph.adj_matrix[v][i] == 1 and not visited[i]:
                    _dfs(i)
        
        _dfs(start)
        return result

    @staticmethod
    def bfs(graph: Graph, start: int):
        """
        Поиск в ширину (возвращает список вершин в порядке обхода)
        """
        visited = [False] * graph.num_vertices
        result = []
        queue = deque([start])
        visited[start] = True
        
        while queue:
            v = queue.popleft()
            result.append(v)
            for i in range(graph.num_vertices):
                if graph.adj_matrix[v][i] == 1 and not visited[i]:
                    visited[i] = True
                    queue.append(i)
        
        return result

    @staticmethod
    def count_components(graph: Graph):
        """Подсчёт компонент связности"""
        visited = [False] * graph.num_vertices
        count = 0
        
        def dfs(v):
            visited[v] = True
            for i in range(graph.num_vertices):
                if graph.adj_matrix[v][i] == 1 and not visited[i]:
                    dfs(i)
        
        for i in range(graph.num_vertices):
            if not visited[i]:
                dfs(i)
                count += 1
        
        return count