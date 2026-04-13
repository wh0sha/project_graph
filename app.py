from flask import Flask, render_template, request, jsonify, session
from core.graph import Graph
from core.algorithms import Algorithms
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'

current_graph = None

@app.route('/')
def index():
    tasks = [
        {"id": 0, "title": "Основные свойства (степени, связность)"},
        {"id": 1, "title": "Обход в глубину (показать)"},
        {"id": 2, "title": "Обход в глубину (проверка)"},
        {"id": 3, "title": "Обход в ширину (показать)"},
        {"id": 4, "title": "Обход в ширину (проверка)"},
        {"id": 5, "title": "Компоненты связности"},
    ]
    return render_template('index.html', tasks=tasks)

@app.route('/task/0')
def task_0():
    global current_graph
    
    n = random.randint(4, 8)
    current_graph = Graph(n)
    current_graph.generate_random(density=0.4)
    
    # Сохраняем правильные ответы
    session['correct_degrees'] = current_graph.get_degrees()
    session['correct_euler'] = current_graph.is_eulerian()
    session['correct_components'] = Algorithms.count_components(current_graph)
    session['matrix'] = current_graph.adj_matrix
    
    graph_data = current_graph.to_json()
    return render_template('task.html', task_id=0, graph_data=graph_data)

@app.route('/api/task/0/check', methods=['POST'])
def check_task_0():
    user_data = request.json
    
    correct_degrees = session.get('correct_degrees')
    correct_euler = session.get('correct_euler')
    correct_components = session.get('correct_components')
    
    user_degrees = user_data.get('degrees')
    user_euler = user_data.get('is_euler')
    user_components = user_data.get('components')
    
    is_correct = True
    message = "Молодец! Всё верно."
    
    if user_degrees != correct_degrees:
        is_correct = False
        message = "Ошибка в степенях вершин."
    elif user_euler != correct_euler:
        is_correct = False
        message = "Ошибка в определении эйлеровости."
    elif user_components != correct_components:
        is_correct = False
        message = "Ошибка в числе компонент связности."
    
    return jsonify({"success": is_correct, "message": message})


# === ЗАДАЧА 1: Показать DFS ===
@app.route('/task/1')
def task_1():
    global current_graph
    n = random.randint(4, 8)
    current_graph = Graph(n)
    current_graph.generate_random(density=0.4)
    
    start_vertex = random.randint(0, n-1)
    dfs_result = Algorithms.dfs(current_graph, start_vertex)
    
    # Сохраняем для проверки (если понадобится)
    session['task_1_dfs'] = dfs_result
    session['task_1_start'] = start_vertex
    
    graph_data = current_graph.to_json()
    return render_template('task_dfs_show.html', 
                          task_id=1, 
                          graph_data=graph_data,
                          start_vertex=start_vertex,
                          dfs_result=dfs_result)

# === ЗАДАЧА 2: Проверить ввод DFS ===
@app.route('/task/2')
def task_2():
    global current_graph
    n = random.randint(4, 8)
    current_graph = Graph(n)
    current_graph.generate_random(density=0.4)
    
    start_vertex = random.randint(0, n-1)
    correct_dfs = Algorithms.dfs(current_graph, start_vertex)
    
    # Сохраняем правильный ответ в сессии
    session['task_2_correct'] = correct_dfs
    session['task_2_start'] = start_vertex
    
    graph_data = current_graph.to_json()
    return render_template('task_dfs_check.html',
                          task_id=2,
                          graph_data=graph_data,
                          start_vertex=start_vertex)

@app.route('/api/task/2/check', methods=['POST'])
def check_task_2():
    user_input = request.json.get('path', [])
    correct = session.get('task_2_correct', [])
    
    # Сравниваем списки
    if user_input == correct:
        return jsonify({"success": True, "message": "✅ Верно! Это правильный обход DFS."})
    else:
        return jsonify({
            "success": False, 
            "message": "❌ Неверно. Попробуй ещё раз.",
            "correct": correct  # Можно убрать в продакшене
        })

# === ЗАДАЧА 3: Показать BFS ===
@app.route('/task/3')
def task_3():
    global current_graph
    n = random.randint(4, 8)
    current_graph = Graph(n)
    current_graph.generate_random(density=0.4)
    
    start_vertex = random.randint(0, n-1)
    bfs_result = Algorithms.bfs(current_graph, start_vertex)
    
    session['task_3_bfs'] = bfs_result
    session['task_3_start'] = start_vertex
    
    graph_data = current_graph.to_json()
    return render_template('task_bfs_show.html',
                          task_id=3,
                          graph_data=graph_data,
                          start_vertex=start_vertex,
                          bfs_result=bfs_result)

if __name__ == '__main__':
    app.run(debug=True)