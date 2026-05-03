import os
import random
from flask import Flask, render_template, jsonify, request, session
from core.tasks.task_0 import Task0
from core.tasks.dfs_task import DFSTaskShow, DFSTaskCheck
from core.tasks.bfs_task import BFSTaskShow, BFSTaskCheck
from core.tasks.connectivity_task import ConnectivityTaskShow, ConnectivityTaskCheck
from core.tasks.mst_task import MSTTask
from core.tasks.dijkstra_task import DijkstraTask
from core.tasks.floyd_task import FloydTask
from core.tasks.prufer_task import PrueferEncodeTask, PrueferDecodeTask
from core.tasks.coloring_task import ColoringTask

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'graph-practice-dev-key')

# Реестр всех 13 задач (0-12) для проекта project_graph
TASKS = {
    0: Task0(),
    1: DFSTaskShow(), 2: DFSTaskCheck(),
    3: BFSTaskShow(), 4: BFSTaskCheck(),
    5: ConnectivityTaskShow(), 6: ConnectivityTaskCheck(),
    7: MSTTask(), 8: DijkstraTask(), 9: FloydTask(),
    10: PrueferEncodeTask(), 11: PrueferDecodeTask(), 12: ColoringTask()
}

def _get_task_seed(task_id: int) -> int:
    """
    Получает или генерирует seed для задачи в сессии пользователя.
    Гарантирует, что один пользователь видит один и тот же граф для одной задачи.
    """
    key = f'task_seed_{task_id}'
    if key not in session:
        session[key] = random.randint(1, 1000000)
    return session[key]

def _reset_task_seed(task_id: int) -> int:
    """Генерирует новый seed для задачи (для кнопки 'Новая задача')."""
    key = f'task_seed_{task_id}'
    session[key] = random.randint(1, 1000000)
    return session[key]

@app.route('/')
def index():
    completed = session.get('completed_tasks', [])
    return render_template('index.html', tasks=TASKS, completed=completed)

@app.route('/task/<int:task_id>')
def task_page(task_id):
    if task_id not in TASKS:
        return render_template('index.html', tasks=TASKS, error="Задача не найдена"), 404
    task = TASKS[task_id]
    # Предварительно инициализируем seed, чтобы он был готов к запросам
    _get_task_seed(task_id)
    return render_template('task_base.html', task=task, task_id=task_id)

@app.route('/api/task/<int:task_id>/show', methods=['GET'])
def api_task_show(task_id):
    if task_id not in TASKS:
        return jsonify({"error": "Task not found"}), 404
    
    seed = _get_task_seed(task_id)
    return jsonify(TASKS[task_id].to_api_show(seed=seed))

@app.route('/api/task/<int:task_id>/check', methods=['POST'])
def api_task_check(task_id):
    if task_id not in TASKS:
        return jsonify({"error": "Task not found"}), 404
    
    # 🔑 Ключевое: используем тот же seed, что и при показе задачи
    seed = _get_task_seed(task_id)
    task = TASKS[task_id]
    graph = task.generate_graph(seed=seed)
    
    user_input = request.get_json(silent=True) or {}
    result = task.check_answer(graph, user_input)
    
    if result.get("correct") and task_id not in session.get('completed_tasks', []):
        completed = session.get('completed_tasks', [])
        completed.append(task_id)
        session['completed_tasks'] = completed
        session.modified = True
    
    return jsonify(result)

@app.route('/api/task/<int:task_id>/reset', methods=['POST'])
def api_task_reset(task_id):
    """Эндпоинт для генерации нового графа (новая вариация задачи)."""
    if task_id not in TASKS:
        return jsonify({"error": "Task not found"}), 404
    
    new_seed = _reset_task_seed(task_id)
    task = TASKS[task_id]
    graph = task.generate_graph(seed=new_seed)
    
    return jsonify({
        "graph": graph.to_vis_format(),
        "solution": task.get_solution(graph),
        "seed": new_seed
    })

if __name__ == '__main__':
    app.run(debug=True)