# core/tasks/base.py
"""Базовый абстрактный класс для всех задач практики."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..graph import Graph

class Task(ABC):
    """
    Базовый класс задачи.
    Каждый конкретный класс наследует его и реализует:
    - генерацию графа (с поддержкой seed для воспроизводимости)
    - получение решения
    - проверку пользовательского ответа
    """
    
    def __init__(self, task_id: int, title: str, description: str):
        self.task_id = task_id
        self.title = title
        self.description = description
    
    @abstractmethod
    def generate_graph(self, seed: Optional[int] = None) -> Graph:
        """
        Создаёт и возвращает граф для текущей задачи.
        
        Параметры:
            seed: Optional[int] — если указан, генерирует детерминированный граф
                                  для воспроизводимости (важно для проверки ответа)
        """
        pass
    
    @abstractmethod
    def get_solution(self, graph: Graph) -> Dict[str, Any]:
        """Возвращает эталонное решение, подсказки или пояснения для отображения."""
        pass
    
    @abstractmethod
    def check_answer(self, graph: Graph, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проверяет ответ пользователя.
        Должен возвращать dict: {"correct": bool, "feedback": str, ...}
        """
        pass
    
    def to_api_show(self, seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Формирует JSON-структуру для эндпоинта /api/task/<id>/show.
        Вызывается автоматически при запросе данных задачи.
        
        Параметры:
            seed: Optional[int] — seed для генерации графа (из сессии пользователя)
        """
        graph = self.generate_graph(seed=seed)
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "graph": graph.to_vis_format(),
            "solution": self.get_solution(graph)
        }
    
    def _get_default_seed(self) -> int:
        """Возвращает дефолтный seed для обратной совместимости."""
        return 42