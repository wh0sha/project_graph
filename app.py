from flask import Flask, render_template, request, jsonify, session
from core.graph import Graph
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'  # Нужен для работы сессий

# Глобальная переменная для хранения текущего графа (пока так)
# В будущем лучше хранить в сессии или базе данных
current_graph = None 

@app.route('/')
def index():
    """Главная страница со списком задач"""
    tasks = [
        {"id": 0, "title": "Основные свойства (степени, связность)"},
        {"id": 1, "title": "Обход в глубину (показать)"},
        {"id": 2, "title": "Обход в глубину (проверка)"},
        # ... можно добавить остальные позже
    ]
    return render_template('index.html', tasks=tasks)

@app.route('/task/0')
def task_0():
    """Страница задачи №0"""
    global current_graph
    
    # 1. Генерируем новый граф (например, 5 вершин)
    n = random.randint(4, 8)
    current_graph = Graph(n)
    current_graph.generate_random(density=0.4)
    
    # 2. Сохраняем правильные ответы в сессию пользователя
    # Чтобы потом проверить, не подсмотрел ли он
    session['correct_degrees'] = current_graph.get_degrees()
    session['correct_euler'] = current_graph.is_eulerian()
    session['matrix'] = current_graph.adj_matrix
    
    # 3. Получаем данные для рисования
    graph_data = current_graph.to_json()
    
    return render_template('task.html', task_id=0, graph_data=graph_data)

@app.route('/api/task/0/check', methods=['POST'])
def check_task_0():
    """Проверка ответа пользователя"""
    user_data = request.json
    
    # Получаем правильные ответы из сессии
    correct_degrees = session.get('correct_degrees')
    correct_euler = session.get('correct_euler')
    
    # Сравниваем (примерно)
    user_degrees = user_data.get('degrees')
    user_euler = user_data.get('is_euler')
    
    is_correct = True
    message = "Молодец! Всё верно."
    
    # Проверка степеней
    if user_degrees != correct_degrees:
        is_correct = False
        message = "Ошибка в степенях вершин."
    
    # Проверка эйлеровости
    elif user_euler != correct_euler:
        is_correct = False
        message = "Ошибка в определении эйлеровости."
        
    return jsonify({"success": is_correct, "message": message})

if __name__ == '__main__':
    app.run(debug=True)